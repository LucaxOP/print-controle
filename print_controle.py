"""
Print no Controle
Tira screenshot na Steam apertando um botao (ou combinacao) no controle.
Funciona com qualquer controle que o Windows reconheca (XInput ou DirectInput),
incluindo o GameSir Nova Lite 2. Ao detectar o atalho, simula a tecla F12
(ou a tecla configurada), que e o atalho padrao de screenshot da Steam.

Uso:
  print_controle.exe              -> roda em segundo plano esperando o atalho
  print_controle.exe --descobrir  -> mostra o numero de cada botao apertado
"""
import ctypes
import json
import os
import sys
import time

# Permite ler o controle mesmo com o jogo em foco (sem isso so funciona
# com a janela do programa em primeiro plano).
os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame  # noqa: E402

PASTA = os.path.dirname(sys.executable if getattr(sys, "frozen", False) else os.path.abspath(__file__))
ARQUIVO_CONFIG = os.path.join(PASTA, "config.json")

CONFIG_PADRAO = {
    # Botoes que precisam estar apertados juntos. No modo XInput (padrao do
    # Nova Lite 2 no PC): 6 = Select/Back, 5 = RB. Use --descobrir para ver
    # os numeros do seu controle.
    "combo": [6, 5],
    # Tecla enviada. F12 e o padrao da Steam.
    "tecla": "F12",
    # Tempo minimo segurando a combinacao antes de disparar (em segundos).
    "segurar_por": 0.05,
    # Intervalo minimo entre dois prints (em segundos).
    "intervalo_minimo": 0.5,
}

# Codigos de tecla virtual e scancode do Windows.
TECLAS = {
    "F1": (0x70, 0x3B), "F2": (0x71, 0x3C), "F3": (0x72, 0x3D), "F4": (0x73, 0x3E),
    "F5": (0x74, 0x3F), "F6": (0x75, 0x40), "F7": (0x76, 0x41), "F8": (0x77, 0x42),
    "F9": (0x78, 0x43), "F10": (0x79, 0x44), "F11": (0x7A, 0x57), "F12": (0x7B, 0x58),
}


def carregar_config():
    config = dict(CONFIG_PADRAO)
    if os.path.exists(ARQUIVO_CONFIG):
        with open(ARQUIVO_CONFIG, encoding="utf-8") as f:
            config.update(json.load(f))
    else:
        with open(ARQUIVO_CONFIG, "w", encoding="utf-8") as f:
            json.dump(CONFIG_PADRAO, f, indent=2)
    config["tecla"] = config["tecla"].upper()
    if config["tecla"] not in TECLAS:
        sys.exit(f"Tecla '{config['tecla']}' nao suportada. Use uma de: {', '.join(TECLAS)}")
    if not config["combo"]:
        sys.exit("A lista 'combo' no config.json esta vazia.")
    return config


class DetectorCombo:
    """Dispara uma vez quando todos os botoes da combinacao ficam apertados."""

    def __init__(self, combo, segurar_por, intervalo_minimo):
        self.combo = set(combo)
        self.segurar_por = segurar_por
        self.intervalo_minimo = intervalo_minimo
        self.inicio = None
        self.disparou = False
        self.ultimo_disparo = -1e9

    def atualizar(self, apertados, agora):
        if not self.combo <= apertados:
            self.inicio = None
            self.disparou = False
            return False
        if self.inicio is None:
            self.inicio = agora
        if (not self.disparou
                and agora - self.inicio >= self.segurar_por
                and agora - self.ultimo_disparo >= self.intervalo_minimo):
            self.disparou = True
            self.ultimo_disparo = agora
            return True
        return False


# --- Envio de tecla (Windows SendInput) ---------------------------------

class _KEYBDINPUT(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort), ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong), ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.c_size_t)]


class _INPUT(ctypes.Structure):
    class _U(ctypes.Union):
        # O maior membro da union (MOUSEINPUT) define o tamanho da estrutura.
        _fields_ = [("ki", _KEYBDINPUT), ("_pad", ctypes.c_byte * 32)]
    _anonymous_ = ("u",)
    _fields_ = [("type", ctypes.c_ulong), ("u", _U)]


def apertar_tecla(nome):
    vk, scan = TECLAS[nome]
    keyup = 0x0002
    eventos = (_INPUT * 2)()
    for i, flags in enumerate((0, keyup)):
        eventos[i].type = 1  # INPUT_KEYBOARD
        eventos[i].ki = _KEYBDINPUT(vk, scan, flags, 0, 0)
    ctypes.windll.user32.SendInput(2, eventos, ctypes.sizeof(_INPUT))


# --- Leitura do controle ------------------------------------------------

def iniciar_pygame():
    pygame.display.init()  # necessario para receber eventos do controle
    pygame.joystick.init()


def controles_conectados():
    return [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]


def botoes_apertados(controles):
    apertados = set()
    for c in controles:
        for b in range(c.get_numbuttons()):
            if c.get_button(b):
                apertados.add(b)
    return apertados


def descobrir():
    iniciar_pygame()
    print("Aperte os botoes do controle para ver o numero de cada um.")
    print("Feche a janela ou aperte Ctrl+C para sair.\n")
    while True:
        for e in pygame.event.get():
            if e.type == pygame.JOYDEVICEADDED:
                c = pygame.joystick.Joystick(e.device_index)
                print(f"Controle conectado: {c.get_name()} ({c.get_numbuttons()} botoes)")
            elif e.type == pygame.JOYBUTTONDOWN:
                print(f"  botao {e.button}")
            elif e.type == pygame.JOYHATMOTION and e.value != (0, 0):
                print(f"  direcional {e.value} (direcional nao pode ser usado no combo)")
        time.sleep(0.01)


def rodar():
    config = carregar_config()
    iniciar_pygame()
    detector = DetectorCombo(config["combo"], config["segurar_por"], config["intervalo_minimo"])
    combo_txt = " + ".join(f"botao {b}" for b in config["combo"])
    print(f"Print no Controle rodando. Atalho: {combo_txt} -> {config['tecla']}")
    print("Deixe esta janela aberta (pode minimizar). Ctrl+C para sair.\n")

    controles = []
    while True:
        for e in pygame.event.get():
            if e.type in (pygame.JOYDEVICEADDED, pygame.JOYDEVICEREMOVED):
                controles = controles_conectados()
                nomes = ", ".join(c.get_name() for c in controles) or "nenhum"
                print(f"Controles: {nomes}")
        if detector.atualizar(botoes_apertados(controles), time.monotonic()):
            apertar_tecla(config["tecla"])
            print(time.strftime("[%H:%M:%S]"), "print!")
        time.sleep(0.01)


if __name__ == "__main__":
    try:
        if "--descobrir" in sys.argv:
            descobrir()
        else:
            rodar()
    except KeyboardInterrupt:
        pass
