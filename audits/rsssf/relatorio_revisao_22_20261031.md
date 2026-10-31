# Revisão individual dos 22 confrontos restantes — RSSSF × Caixa (31/10/2026)

**Workflow efetivamente executado:** https://github.com/marcosvilhena87/Loteca.FiveThirtyEight/actions/runs/41243751290

**Artefato (snapshots, candidatos e diagnóstico):** https://github.com/marcosvilhena87/Loteca.FiveThirtyEight/actions/runs/41243751290/artifacts/13058645293

**Matriz individual dos 22 jogos:** [revisao_22_resultado_20261031.csv](revisao_22_resultado_20261031.csv)

## Resultado mensurado
- Caixa: 266 jogos dos concursos 0032–0050.
- 262 candidatos únicos **para revisão documental**, 3 sorteios bloqueados, 1 divergência de data a investigar.
- Dos 22 casos inicialmente sem candidato: **21 obtiveram candidato único**, **1 permaneceu sem candidato** devido à tolerância de data de ±1 dia.
- **Nenhuma aprovação automática ao Elo.** A unicidade do matcher não equivale a homologação documental.
- 13 fontes RSSSF, 13 com sucesso nas verificações programadas, 2658 registros extraídos (1 administrativo excluído do matcher).

## Evidências e causas técnicas por grupo
1. Série B 2002: 35/6 Sport–CRB; 35/12 Sampaio Corrêa–XV Piracicaba; 40/8 Sport–Fortaleza. A competição possui dois clubes denominados XV de Novembro em fontes distintas; a identidade deve ser contextualizada. Fonte: https://www.rsssfbrasil.com/tablesae/br2002l2.htm
2. Paulista B1 2002: 35/13 Guaratinguetá–Tupã; 38/10 Tupã–Mauaense; 38/13 XV Caraguatatuba–Rio Claro. O HTML contém nomes com acentuação degradada; o alias corrompido foi tratado apenas dentro da B1 paulista, sem junção ao XV de Piracicaba. Fonte: https://mail.rsssfbrasil.com/tablessz/sp2002l4.htm
3. Espanhol 2002/03: 44/4–5, 45/3, 46/9, 46/12, 47/1. A RSSSF usa nomes abreviados (Racing, Rayo, Betis, Celta, Madrid), resolvidos pelo contexto da competição. Fonte: https://www.rsssf.org/tabless/span03.html
4. Carioca 2003: 48/1 Vasco da Gama–América e 49/1 Vasco–Botafogo. O alias Vasco está identificado, porém 48/1 tem **divergência documental de datas**. Fonte: https://www.rsssfbrasil.com/tablesr/rj2003.htm
5. Paulista 2003: 49/8 Guarani–União Barbarense; 50/4 Internacional de Limeira–São Paulo; 50/9 Palmeiras–União Barbarense. RSSSF usa União Agrícola e Internacional. Fonte: https://www.rsssfbrasil.com/tablessz/sp2003.htm
6. Mineiro 2003: 49/10–12 e 50/5–6. Resultados com notas de público (`Att:`) foram interpretados incorretamente como parte do nome da equipe visitante; o extrator foi corrigido, com aliases estaduais restritos. Fonte: https://www.rsssfbrasil.com/tablesfq/mg2003.htm

## Única pendência documental residual: concurso 0048, jogo 01
- Caixa: **sábado, 18/01/2003**, Vasco da Gama **1×0** América-RJ.
- RSSSF (primeira rodada do Carioca): **quinta-feira, 16/01/2003**, Vasco da Gama **1×0** América-RJ.
- Placar, mando e clubes coincidem; diferença de **dois dias** supera a regra conservadora do conciliador (±1).
- **Não** alterar a data da Caixa nem aceitar automaticamente a partida: registrar `divergencia_data_documentada`, pesquisar documentação independente do jogo e só então homologar o vínculo.

## Política de segurança
As correções de aliases não substituem revisão da identidade e do placar; clubes homônimos permanecem distintos (XV de Piracicaba e XV de Caraguatatuba; América-MG e América-RJ; Atlético-MG e Atlético de Madrid). A elegibilidade Elo para todos os novos vínculos segue `nao`.
