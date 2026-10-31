# Auditoria RSSSF — incremento conservador de cobertura (31/10/2026)

## Comparação de execuções GitHub Actions

| Métrica | Anterior | Atual (commit 3288e68) |
|---|---:|---:|
| Jogos da Caixa processados | 17.836 | 17.836 |
| Linhas RSSSF extraídas | 2.346 | 2.726 |
| Correspondências automáticas candidatas | 926 | 961 |
| Não correspondentes | 16.910 | 16.875 |
| Percentual de correspondência | 5,19% | 5,39% |
| Testes Python aprovados | 8 | 8 |

Nova fonte: Série A brasileira 2018 (https://www.rsssfbrasil.com/tablesae/br2018.htm). Foi introduzida proteção de identidade: se ambos os clubes têm estado /UF, os estados devem coincidir; nomes homônimos selecionados, quando não têm UF em ambos os lados, não são confirmados.

A execução 41231202595 registrou 2.726 registros extraídos e 961 candidatos, sem erros na suíte de oito testes (https://github.com/marcosvilhena87/Loteca.FiveThirtyEight/actions/runs/41231202595). Uma execução posterior (41231224478) inclui dois testes adicionais de homônimos.

**Atenção:** não são 961 jogos individualmente certificados nem 961 partidas de primeira equipe comprovadas por revisão humana. A extração é baseada em formatos simples de resultados e pode conter linhas espúrias; a identidade de clubes com siglas, mudança de nome ou grafias diferentes ainda precisa de inventário completo, bem como amostragem manual de falsos positivos. Não transferir automaticamente estes resultados para o dataset Elo.

## Pendências
- Ampliar o catálogo além das dez páginas atuais, priorizando competições e temporadas observadas na Caixa; verificar cada URL individualmente antes de adicioná-la.
- Exigir inspeção de amostra de correspondências e falsas rejeições por tipo de fonte, e validar datas para temporadas transanuais.
- Preservar UF em IDs canônicos e distinguir equipes principais, seleções, Sub-20, reservas e futebol feminino.
- Gerar relatório por fonte (jogos parseados, candidatos e taxa de aceitação) e quarentena de colisões, sem alterar os CSVs originais.
