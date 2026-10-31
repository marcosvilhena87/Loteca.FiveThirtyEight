# Auditoria externa de partidas da Loteca

Objetivo: identificar competição e categoria das partidas nos 13 CSVs de Loteca/dados, com fontes rastreáveis e prevenção de vazamento no Elo.

## Uso

Instale o projeto em modo editável (pip install -e .) e execute:

    python -m loteca_fivethirtyeight.external_audit --output reports/auditoria_externa
    pytest -q tests/test_external_audit.py

Sem SERPER_API_KEY, a rotina baixa os CSVs e gera exceções e links de pesquisa, mas **não faz pesquisa externa**. Para pesquisar de fato, configure a variável de ambiente SERPER_API_KEY, obtida em https://serper.dev (serviço sujeito a cotas e preços):

    python -m loteca_fivethirtyeight.external_audit --max-searches 100 --pause 1.5

Arquivos de saída: auditoria_completa.csv, excecoes.csv, resumo.json e RELATORIO.md.

## Governança

- Sem evidência externa confiável, elegivel_elo=nao.
- Busca orgânica só conta como correspondência se informar times, data, placar e competição.
- Um snippet não basta para aprovar jogo principal.
- Sorteios são críticos; duplicidades por concurso+jogo são críticas.
- Exclusões de base/feminino/reservas requerem ao menos dois domínios externos concordantes.
- Busca negativa não prova categoria de base.
- Identificação de clube exige futura resolução de aliases históricos, inclusive UF; nomes semelhantes não são identidade.
- Separar resultado esportivo de resultado lotérico.
- Não guardar tokens no Git. O relatório é uma triagem reproduzível, não uma certificação automática de todos os jogos.

Próximo passo: integrar súmulas e tabelas oficiais de CBF/federações e adicionar revisão humana auditável para liberar cada partida ao Elo.
