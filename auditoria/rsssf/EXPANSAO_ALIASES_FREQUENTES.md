# Expansão do registro canônico — lote de frequência 1

Em 31/10/2026 foram contadas as ocorrências de nomes de equipes nas 13 fontes originais da Loteca, para orientar a fila de trabalho. O conjunto inicial do cadastro foi expandido por 47 aliases de clubes brasileiros, priorizando nomes com maior frequência e a indicação explícita de UF nos registros da Caixa.

## Regras e cautelas
- `club_id` mantém país (`BRA`) e UF. Estados diferentes nunca devem ser unificados pelo mesmo alias.
- `since=2002` / `until=2026` nas **novas entradas** é somente a janela de utilização desta auditoria; não constitui prova de nome legal estável, data de fundação ou continuidade institucional. Histórico de renomeações continua sujeito a comprovação.
- Homônimos sem UF permanecem em quarentena. Outras categorias (Sub-20, reservas, feminino e seleções), sem chave separada de categoria, não estão autorizadas como equipes profissionais masculinas por essas entradas.
- Uma grafia da Caixa normalizada não é, isoladamente, prova de que a RSSSF esteja se referindo ao mesmo clube: a partida ainda deve passar por confirmação de competição, placar e data.
- Fontes RSSSF utilizadas como referência de identidade: https://www.rsssfbrasil.com/tablesae/br2024.htm e https://www.rsssfbrasil.com/tablesae/br2025.htm. Elas corroboram identidades das equipes participantes de 2024 e 2025, mas **não** verificam por si sós os 47 registros em todas as temporadas.
- Casos especialmente dependentes de pesquisa histórica: BRAGANTINO/SP vs Red Bull Bragantino, NOVORIZONTINO/SP e variantes históricas, PARANA/PR, ATHLETICO/PR. Não declarar automaticamente continuidade ou identidade sob outros nomes.

## Evidência técnica
Alteração: `auditoria/rsssf/club_registry.csv`.
Teste de regressão: `tests/test_club_identity.py`, casos Atlético/MG e Atlético/GO, Botafogo/PB, Botafogo sem UF, São Caetano.
Execução: https://github.com/marcosvilhena87/Loteca.FiveThirtyEight/actions/runs/41232217892

## Próximas prioridades
1. Extrair do artefato `aliases_revisao_manual.csv` a fila restante, com frequência por ano e exemplos de jogos.
2. Separar nome normalizado, identidade de clube, categoria da equipe e mudança institucional em tabelas próprias.
3. Auditar as 200 URLs candidatas quanto a conteúdo de competição e ano, além do simples retorno HTTP.
4. Medir diferenças entre a cobertura ingênua e por IDs, sem transformar candidatos automáticos em confirmações humanas.
