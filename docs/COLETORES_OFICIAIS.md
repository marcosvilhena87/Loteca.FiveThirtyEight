# Coletores de documentos oficiais — CBF, FPF e CONMEBOL

Este módulo descobre **links de tabelas, regulamentos e súmulas** em sites institucionais. Não converte notícias em resultados estruturados; não preenche partidas oficiais automaticamente.

Execução:

    python -m loteca_fivethirtyeight.official_collectors --output reports/fontes_oficiais

É possível passar arquivo JSON com a lista de pontos de entrada:

    python -m loteca_fivethirtyeight.official_collectors --seeds data/fontes/seeds.json

Cada objeto JSON requer: organizadora (cbf/fpf/conmebol), temporada, competicao, url. Somente HTTPS e hosts oficiais autorizados são aceitos. Páginas HTML são analisadas por hyperlinks; PDF é registrado mas **não é processado como súmula**. A saída inclui documentos_oficiais.csv, fila_sumulas_documentais.csv, falhas_coleta.csv e resumo_coleta.json. O nome fila_sumulas_documentais significa *links candidatos*, não documentos lidos ou autenticados.

Depois, o módulo official_fixtures.py cruza planilhas oficiais **previamente estruturadas** com os registros históricos. Os coletores não geram automaticamente esses arquivos: PDF, estruturas JS e páginas antigas exigem parsers especializados e conferência de data/clubes/placar.

Prioridades para pesquisa histórica:
- Paulista 2002 e 2003: competições com equipes B identificadas na Loteca.
- Copinha 2018: competição de formação, portanto bloquear Elo principal.
- CBF 2009 e 2025: conferência de categorias e resultados de campeonatos nacionais.
- CONMEBOL: competições internacionais, inclusive grafias estrangeiras ambíguas.

Não considerar "documento_descoberto_nao_verificado" como prova de que determinado confronto ocorreu. Não remover bloqueios de treinamento sem verificação individual da evidência.
