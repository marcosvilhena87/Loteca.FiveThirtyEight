# Premier League 2002/03 — extração corrigida e conciliação executada

Data: 31/10/2026

Execução: https://github.com/marcosvilhena87/Loteca.FiveThirtyEight/actions/runs/41241877018

## Integridade da Premier League
- Fonte: https://www.rsssf.org/tablese/eng03.html
- Extração anterior: 683 registros, com outras competições.
- Extração corrigida: **380 partidas, 38 rodadas, 10 partidas por rodada**, sem divergências nas verificações configuradas.
- Correção: truncar a seção da rodada 38 no cabeçalho `Final Table:`, evitando capturar FA Cup e demais divisões.

## Conciliação Caixa (concursos 0032–0050)
- 266 jogos da Caixa.
- 230 candidatos únicos para revisão documental (antes: 223).
- 33 sem candidato (antes: 40).
- 3 sorteios bloqueados.
- Zero homologações automáticas ao Elo.

## Cobertura histórica
- 11 fontes, 11 com `integrity=pass` pelas verificações implementadas.
- 2312 entradas RSSSF, incluindo uma decisão administrativa, que permanece fora das 2311 partidas usadas para comparação.
- Apesar do status técnico, as ligas brasileiras e estaduais ainda carecem de contagem esperada independente por fase.

## Próxima auditoria
- Revisar as 33 pendências individualmente; seu diagnóstico automático classifica 32 como alias ausente/cobertura insuficiente e 1 como competição incompleta.
- Os 230 candidatos não são homologados para Elo; confirmar identidade, data, placar e competição na referência primária.
