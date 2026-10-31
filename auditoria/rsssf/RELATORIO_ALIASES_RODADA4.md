# Triagem de aliases — quarta rodada

## Resultado reproduzido na fila original (4.117 combinações alias/ano)
- **459** combinações com ID único cadastrado, cobrindo **1.877** aparições antes não resolvidas.
- **3.658** combinações, equivalentes a **8.080** aparições, permanecem na quarentena.
- Cobertura cadastral projetada: **27.592 / 35.672 = 77,35%** das aparições de equipes. Não é percentual de partidas confirmadas pela RSSSF nem de elegibilidade Elo.

## Evidências e limitações
- Macaé Esporte: clube identificado pela FERJ, https://www.fferj.com.br/clubes/maca-efc.
- FC Barcelona, Juventus, Liverpool FC e AC Milan possuem documentação oficial da identidade institucional, mas **BARCELONA, JUVENTUS, LIVERPOOL e MILAN sem país** continuam em quarentena, porque os nomes isolados nos CSVs não comprovam que a partida foi contra aquele clube. Ver `aliases_internacionais_candidatos.csv`.
- Qualquer resolução definitiva desses quatro depende da competição, do adversário, da data e do confronto com fonte RSSSF; não se deve inferir país a partir da popularidade da equipe.
- `OESTE/SP`, `TREZE/PB`, `AMERICANO/RJ` e demais nomes continuam aguardando identificação documentada nesta rodada.
- Os períodos operacionais do cadastro não substituem datas históricas verificadas.
- A classificação por ID é provisória. Uma partida não recebe certificação externa só porque seus dois aliases têm IDs.
- Os CSVs originais da Caixa permanecem sem alterações.

## Artefatos
- `aliases_triagem_v4.csv`: todas as combinações da fila original.
- `aliases_quarentena_v4.csv`: pendências restantes.
- `aliases_internacionais_candidatos.csv`: candidatos a identidade internacional, sem promoção automática.
