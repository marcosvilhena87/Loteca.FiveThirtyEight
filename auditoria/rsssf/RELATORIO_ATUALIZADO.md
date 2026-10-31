# Auditoria RSSSF — atualização 31/10/2026

## Status verificado
Foram lidas as 13 fontes CSV (17.836 jogos, concursos 1–1274). A lista de evidências manuais expandiu-se de sete para **dez jogos diretamente documentados** na RSSSF, isto é, **0,0561%** (10/17.836). Outros **17.826 jogos (99,9439%)** continuam sem confirmação individual; não inferir que sejam inválidos. Os três jogos novos são concurso 1175 jogo 10 Flamengo 1–1 Internacional; concurso 1179 jogo 9 Grêmio 0–2 Flamengo; e concurso 1207 jogo 10 Santos 0–6 Vasco, todos na Série A 2025.

## Cobertura RSSSF
O manifesto contém agora **sete páginas externas de cinco temporadas/competições distintas**: Rio–São Paulo, Sul–Minas, Nordeste e Série A de 2002, além da Série A de 2024, 2025 e 2026. São URLs verificadas como existentes; **cobertura de catálogo não significa processamento bem-sucedido de partidas**. O nome do manifesto antigo foi mantido por compatibilidade, embora contenha temporadas adicionais.

## Outras categorias e divergências
- **2 jogos com indício explícito de Sub-20** (concursos 393 e 781); ainda aguardam prova RSSSF da competição. Não classificar como confirmados pela RSSSF.
- **92 datas de jogo vazias** nos CSVs originais. São pendências de completude, não divergências externas comprovadas.
- **0 divergências internas** entre placar e resultado 1/X/2, e **0** duplicações de concurso+jogo.
- Nenhuma divergência externa adicional foi formalmente comprovada neste lote de 3 jogos.
- A página RSSSF 2026 contém jogos ainda não realizados (placar '-'), e formato de apresentação com tabs e datas completas. Deve haver filtragem de partidas futuras e adaptação do parser antes de uso em produção.

## Execução e limitações
Foi melhorado o parser de linhas simples RSSSF em fonte pré-formatada e a lógica inicial de matching foi mantida com tolerância de 3 dias, identificação de competição e estados de ambiguidade. **Não foi possível executar uma coleta em lote do site RSSSF neste ambiente, nem uma suíte pytest completa**; assim, não há alegação de cobertura ou taxa de acerto do parser em sete páginas. A evidência de dez partidas foi obtida por comparação direta dos CSVs com páginas RSSSF publicamente acessíveis, documentada em `evidencias_verificadas.csv`.

Os CSVs originais no repositório Loteca não foram alterados. Este relatório não substitui a execução completa do pipeline e não deve ser tratado como liberação para o modelo Elo.
