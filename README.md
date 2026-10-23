# Print no Controle

Tira print na Steam apertando uma combinação de botões no controle (feito pensando no GameSir Nova Lite 2, mas funciona com qualquer controle que o Windows reconheça). O programa fica rodando em segundo plano e, quando você aperta o atalho, simula a tecla **F12**, que é a tecla de screenshot padrão da Steam.

**Atalho padrão:** segurar **Select (Back) + RB** juntos.

## Como instalar (uma vez só)

1. Instale o Python: https://www.python.org/downloads/ (marque **"Add Python to PATH"** na instalação).
2. Coloque todos os arquivos desta pasta numa pasta no seu PC, por exemplo `C:\PrintControle`.
3. Dê dois cliques em **`build_exe.bat`**. Ele baixa o que precisa e cria o `print_controle.exe` na mesma pasta.

Depois disso o Python não é mais necessário para usar o programa.

## Como usar

1. Abra o `print_controle.exe` (pode minimizar a janela).
2. Abra o jogo pela Steam.
3. Segure **Select + RB**: a Steam tira o print como se você tivesse apertado F12.

Para abrir junto com o Windows, rode `iniciar_com_windows.bat` uma vez.

## Trocar o botão

1. Rode `descobrir_botoes.bat` e aperte os botões que você quer usar. Ele mostra o número de cada um.
2. Abra o `config.json` (é criado na primeira vez que o programa roda) e troque a lista `combo`. Exemplos:
   - `"combo": [6, 5]` → Select + RB (padrão)
   - `"combo": [8, 9]` → apertar os dois analógicos juntos
   - `"combo": [12]` → um botão só (se o seu controle tiver um botão extra que você não usa)
3. Feche e abra o programa de novo.

No `config.json` também dá para trocar a tecla (`"tecla": "F12"`) caso você tenha mudado o atalho de screenshot na Steam (Steam → Configurações → No jogo → Atalho de captura de tela).

## Se não funcionar

- **O programa não vê o controle:** confira se o Nova Lite 2 está no modo PC/XInput (no manual, normalmente é segurar o botão Home + X ao ligar, ou usar o dongle no modo X-input). Rode `descobrir_botoes.bat` para ver se ele aparece.
- **Os números dos botões são diferentes:** acontece no modo DirectInput/Switch. Use `descobrir_botoes.bat` e ajuste o `config.json`.
- **O print não sai em algum jogo:** alguns jogos rodando como administrador bloqueiam teclas simuladas. Nesse caso, clique com o botão direito no `print_controle.exe` → **Executar como administrador**.
- **O Select + RB faz outra coisa no jogo:** escolha outra combinação, por exemplo os dois analógicos (`[8, 9]`).
