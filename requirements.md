### Requisitos Básicos

1. Automatização do Comando /bump:
- O comando /bump é liberado para ser usado a cada 2 horas e serve para manter o servidor de Discord ativo no Disboard;
- A liberação do uso do comando é avisada pelo próprio bot do Discord (gatilho).

2. Estatísticas de Canais:
- Analisar canais menos utilizados:
    - última mensagem há x dias;
    - quantidade total de mensagens do dia;
- Reportar o relatório com dados:
    - dos canais que podem ser deletados por inativadade;
    - dos canais mais utilizados;
    - de possíveis melhorias que podem ser aplicadas (usando IA integrada). 

3. Comando /battle:
- Criação de um comando /battle, que sorteia 2 usuários para um duelo de X1 valendo uma premiação;
- A premiação pode ser configurada com /prizePool: inserindo um texto descritivo da premiação;
- O bot sorteará 2 usuários aleatórios que:
    - Estejam ativos no dia do sorteio (mensagem ou call no servidor naquele dia)'
    - Que possuam o mesmo cargo dentre os abaixo (essa é a classificação de habilidade):
        - @🎴ㅤÉpico
        - @🀄ㅤLenda 
        - @🌗ㅤMítico 
        - @🌗ㅤHonra 
        - @🌓ㅤGlória 
        - @🌒ㅤImortal 
- Ambos os usuários serão marcados em um chat específico setado em /battleChat;
- Ambos os usuários precisão reagir à mensagem com um emoji para confirmar o X1;
- Se um dos usuários não aceitar em x minutos (configurado com /setTime), o bot enviará uma mensagem (configurada em /messageRun);
- Caso ambos aceitarem dentro do tempo limite, uma mensagem avisará o embate (messageBattle).