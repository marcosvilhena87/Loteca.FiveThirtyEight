# Extração eliminatórias Brasileirão 2002 — Série A e Série B

Execução completa: https://github.com/marcosvilhena87/Loteca.FiveThirtyEight/actions/runs/41242523654

## Regras
- RSSSF compacta placares ida-volta como `ClubeA 3-0 0-2 ClubeB`, correspondendo a `ClubeA 3×0 ClubeB` na ida e `ClubeB 2×0 ClubeA` na volta.
- Duas datas são interpretadas dos cabeçalhos `[Nov 24 and 27]` ou `[Nov 30 and Dec 7]` por fase.
- Preserva `phase`, `leg`, `source_url` e `source_line` em cada registro, com mandos e gols individualizados.
- Sem datas, confronto é bloqueado e registrado para revisão, sem atribuição artificial de resultados.

## Execução observada
| Competição | Antes | Depois | Eliminatórias acrescidas |
|---|---:|---:|---:|
| Série A 2002 | 327 | 341 | 14 |
| Série B 2002 | 325 | 339 | 14 |

- Testes GitHub Actions: sucesso.
- Caixa concursos 0032–0050: 266 registros; **241 candidatos únicos**, **22 sem candidato**, **3 sorteios**, zero homologações automáticas ao Elo.
- Antes da extração de eliminatórias: 235 candidatos únicos, 28 sem candidato.
- Fontes: https://www.rsssfbrasil.com/tablesae/br2002.htm e https://www.rsssfbrasil.com/tablesae/br2002l2.htm.

## Ressalvas
O status de integridade configurado nas Séries A/B não representa ainda contagem completa do calendário regular: o primeiro estágio da Série A 2002 continha 26 clubes × 25 rodadas / 2 = 325 jogos, mas o extrator genérico já recolhia 327 antes do acréscimo das eliminatórias. Precisa investigar as duas linhas suplementares e confrontar todos os 325 jogos pelos mandantes e datas. Da mesma forma, validar a cobertura e duplicidades da Série B. A extração das eliminatórias não equivale à homologação Elo; resultados administrativos devem permanecer separados.
