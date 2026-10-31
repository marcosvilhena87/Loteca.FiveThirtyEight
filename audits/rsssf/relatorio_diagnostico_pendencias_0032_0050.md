# Diagnóstico automático dos 71 jogos sem candidato — concursos 0032–0050

Execução GitHub Actions: https://github.com/marcosvilhena87/Loteca.FiveThirtyEight/actions/runs/41241175987

Artefatos para conferência: https://github.com/marcosvilhena87/Loteca.FiveThirtyEight/actions/runs/41241175987/artifacts/13057472006

## Resultados executados
- Caixa: 266 jogos; 192 candidatos únicos **não homologados**, 71 sem candidato e 3 sorteios bloqueados.
- Categorias provisórias dos 71: **70** `alias_ausente_ou_nao_coberto`, **1** `competicao_ausente_ou_fonte_incompleta`.
- Elo aprovado nesta execução: **zero**.
- RSSSF: 1648 registros arquivados, dos quais 1647 marcados como partidas disputadas para o matcher. Fontes de Espanha e Itália verificadas por rodada.
- Todos os jobs de teste, ingestão e diagnóstico concluíram com sucesso.

## Limitações relevantes
A classificação é heurística. O cadastro de aliases temporais ainda possui poucos clubes; `alias_ausente_ou_nao_coberto` não demonstra identidade errada, apenas incapacidade do matcher em resolver o caso. Uma competição ausente também pode gerar essa categoria. Os 71 registros permanecem pendentes, sem alteração da matriz de homologação.

O artefato inclui `diagnostico_sem_candidato_0032_0050.csv`, com concurso, jogo, equipes, data, categoria provável e evidências de confrontos próximos. Para desbloquear, classificar primeiro por competição, verificar nomes e datas na fonte original, e só então alterar o status na matriz.

## Próximas melhorias
1. Ampliar fontes para competições europeias (Inglês 2002/03), Copa do Brasil e Série C, divisões estaduais quando relevantes.
2. Expandir aliases por ID canônico e período, sem fundir homônimos ou equipes B.
3. Introduzir diagnóstico independente de aliases para filtrar casos de competição ausente.
4. Configurar totais esperados independentes e integridade por fase para Série A/B brasileiras e estaduais.
