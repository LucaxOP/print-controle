# Print no Controle

Tira print na Steam apertando uma combinação de botões no controle (feito pensando no GameSir Nova Lite 2, mas funciona com qualquer controle que o Windows reconheça). O programa fica rodando em segundo plano e, quando você aperta o atalho, simula a tecla **F12**, que é a tecla de screenshot padrão da Steam.

**Atalho padrão:** apertar o botão **Home**. Os jogos praticamente não usam esse botão.

## Baixar pronto (mais fácil)

A cada atualização o GitHub gera o `.exe` sozinho. Abra a aba **Actions** do repositório, clique na execução mais recente de **Gerar .exe** e baixe o arquivo `print_controle` no fim da página (precisa estar logado no GitHub). Descompacte numa pasta e pronto.

## Gerar o .exe você mesmo (opcional)

1. Instale o Python: https://www.python.org/downloads/ (marque **"Add Python to PATH"** na instalação).
2. Coloque todos os arquivos desta pasta numa pasta no seu PC, por exemplo `C:\PrintControle`.
3. Dê dois cliques em **`build_exe.bat`**. Ele baixa o que precisa e cria o `print_controle.exe` na mesma pasta.

Depois disso o Python não é mais necessário para usar o programa.

## Como usar

1. Abra o `print_controle.exe` (pode minimizar a janela).
2. Abra o jogo pela Steam.
3. Aperte o **Home**: a Steam tira o print como se você tivesse apertado F12.

Para abrir junto com o Windows, rode `iniciar_com_windows.bat` uma vez.

## Trocar o botão

1. Rode `descobrir_botoes.bat` e aperte os botões que você quer usar. Ele mostra o número de cada um.
2. Abra o `config.json` (é criado na primeira vez que o programa roda) e troque a lista `combo`. Exemplos:
   - `"combo": [10]` → Home (padrão)
   - `"combo": [8, 9]` → clicar os dois analógicos juntos
   - `"combo": [6, 5]` → Select + RB

Números no modo XInput (testado no Nova Lite 2): A=0, B=1, X=2, Y=3, LB=4, RB=5, Select=6, Start=7, L3=8, R3=9, Home=10. Os botões borboleta traseiros não aparecem nesse modo.
   - `"combo": [12]` → um botão só (se o seu controle tiver um botão extra que você não usa)
3. Feche e abra o programa de novo.

No `config.json` também dá para trocar a tecla (`"tecla": "F12"`) caso você tenha mudado o atalho de screenshot na Steam (Steam → Configurações → No jogo → Atalho de captura de tela).

## Se não funcionar

- **O programa não vê o controle:** confira se o Nova Lite 2 está no modo PC/XInput (no manual, normalmente é segurar o botão Home + X ao ligar, ou usar o dongle no modo X-input). Rode `descobrir_botoes.bat` para ver se ele aparece.
- **Os números dos botões são diferentes:** acontece no modo DirectInput/Switch. Use `descobrir_botoes.bat` e ajuste o `config.json`.
- **O print não sai em algum jogo:** alguns jogos rodando como administrador bloqueiam teclas simuladas. Nesse caso, clique com o botão direito no `print_controle.exe` → **Executar como administrador**.
- **A combinação faz outra coisa no jogo:** escolha outra com `descobrir_botoes.bat`.

## Usar os botões traseiros

No modo XInput os botões traseiros não aparecem como botões próprios para o Windows. Programe o botão traseiro (pelo software ou atalho do controle) para apertar o **Home**, se o controle permitir, e ele vira o botão de print. Em outros modos do controle, rode `descobrir_botoes.bat`: se o botão traseiro aparecer com um número próprio, coloque só esse número no `combo`.
- **Aparece um balão do Xbox "Click for Help" ao apertar o Home:** é o programa antigo "Microsoft Xbox 360 Accessories" (`XBoxStat.exe`), não este. Desative em Gerenciador de Tarefas → Inicializar → XboxStat → Desabilitar (ou desinstale em Aplicativos).
- **O jogo troca os ícones para teclado depois do print:** é porque o print é feito simulando a tecla F12. Para evitar, ative o Steam Input no jogo (Biblioteca → botão direito no jogo → Propriedades → Controle → Ativar Steam Input) e use o atalho nativo da Steam, **Home + RB**, em vez deste programa.
