# Revisão histórica de identidades — 31/10/2026

## Separação institucional

- **Bragantino / Red Bull Bragantino:** mesma linhagem institucional no registro, `BRA-SP-BRAGANTINO`. A parceria foi formalizada em 2019 e o nome Red Bull Bragantino passou a ser usado em 2020. O clube **RB Brasil** é registrado sob outro ID (`BRA-SP-RB-BRASIL`), mesmo após transferência de jogadores e estrutura. Fontes: https://www.redbullbragantino.com/br-pt/historia/historia e https://ge.globo.com/sp/vale-do-paraiba-regiao/futebol/times/bragantino/noticia/r-80-milhoes-em-reforcos-e-63percent-de-aproveitamento-anuncio-da-parceria-do-bragantino-completa-um-ano.ghtml.
- **Grêmio Novorizontino (2010):** não unificar com o extinto Grêmio Esportivo Novorizontino. ID atual `BRA-SP-NOVORIZONTINO-2010`; nenhum alias do time extinto foi habilitado sem evidência de partidas no período 2002–2026. Fonte: https://www.gremionovorizontino.com.br/wp-content/uploads/2025/01/PRESS.COPINHA-1.pdf.
- **Athletico Paranaense:** alteração de marca e grafia em dezembro de 2018, sem criação de nova identidade para o Elo. ID `BRA-PR-ATHLETICO`. Fonte: https://static.athletico.com.br/wp-content/uploads/2017/12/12105645/RelatorioAnual2018.pdf.
- **Paraná Clube:** instituição criada em 1989 pela fusão de Colorado EC e EC Pinheiros. Para Elo, `BRA-PR-PARANA` não deve ser unificado retrospectivamente com os dois predecessores. Fonte: https://paranaclube.com.br/historia/.

## Regras de segurança

As entradas com `since=2002` e `until=2026` usam a janela de estudo, não são datas de fundação. Clubes de base e equipes principais precisam de chaves separadas no futuro. O registro existente ainda não resolve todos os aliases; nenhum índice de cobertura novo foi atribuído a esta revisão sem execução.

## Arquivos

- `club_registry.csv`: identidades institucionais revisadas
- `tests/test_club_identity.py`: casos de regressão para Bragantino/RB Brasil, Novorizontino e Athletico
- GitHub Actions: https://github.com/marcosvilhena87/Loteca.FiveThirtyEight/actions/runs/41232359189

## Limitação

A lista de aliases ainda não resolvidos precisa ser extraída dos artefatos de execução `aliases_revisao_manual.csv` para resolver sistematicamente os restantes, com país, UF e categoria. Casos ainda não verificados permanecem em quarentena; **não** gerar IDs por semelhança de nomes.
