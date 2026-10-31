# Execução real RSSSF × Caixa — concursos 0032–0050
Data da execução: 2026-10-31.

- Workflow: https://github.com/marcosvilhena87/Loteca.FiveThirtyEight/actions/runs/41240959900
- Artefato: https://github.com/marcosvilhena87/Loteca.FiveThirtyEight/actions/runs/41240959900/artifacts/13057671093
- Estado do GitHub Actions: **success**; testes e ingestão executados.
- HTML RSSSF baixados: 8/8; fontes sem divergência nas verificações implementadas: 8/8.
- RSSSF extraído: 1648 linhas, entre as quais **1 resultado administrativo**, excluído de jogos disputados no motor de comparação.
- Caixa: 266 registros (concursos 0032–0050).
- 192 candidato único para revisão, 71 sem candidato, 3 sorteios bloqueados, **0 aprovações automáticas ao Elo**.

| Fonte RSSSF | Extraídos | Verificação |
|---|---:|---|
| Brasileiro Série A 2002 | 327 | Sem contagem independente por rodada |
| Brasileiro Série B 2002 | 325 | Sem contagem independente por rodada |
| Primeira Divisão Espanhola 2002/03 | 380 | 38 rodadas × 10 jogos; sem duplicatas detectadas |
| Serie A italiana 2002/03 | 306 | 34 rodadas × 9 resultados; 305 partidas disputadas + Como 0×2 Udinese (administrativo, 18/12/2002) |
| Carioca 2003 | 64 | Sem contagem independente |
| Paulista 2003 | 103 | Sem contagem independente |
| Mineiro 2003 | 78 | Sem contagem independente |
| Brasiliense 2003 | 65 | Sem contagem independente |

A aprovação automática para o Elo permanece desabilitada. Os 192 candidatos únicos **não equivalem a 192 partidas homologadas**: requerem revisão documental e validação temporal da identidade dos clubes. Os 71 sem correspondência podem refletir aliases insuficientes, outras competições, diferenças na data ou formatos não extraídos.

Limitação: `integrity=pass` fora das ligas espanhola e italiana não atesta completude da temporada porque as expectativas quantitativas independentes ainda não foram configuradas. Na Itália o resultado administrativo conta para a integridade, mas é excluído do confronto como partida jogada. A Caixa mantém seu próprio histórico de sorteios.
