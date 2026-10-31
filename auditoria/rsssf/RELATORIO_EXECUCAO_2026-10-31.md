# Execução integral do matcher RSSSF — 31/10/2026

## Resultados verificados pelo GitHub Actions

Execução [41231041932](https://github.com/marcosvilhena87/Loteca.FiveThirtyEight/actions/runs/41231041932) — **sucesso**. O pipeline instalou dependências, executou os testes (8 passed), carregou os 13 CSVs de snapshot e produziu artefatos.

| Medida | Quantidade |
|---|---:|
| Jogos da Caixa processados | 17.836 |
| Registros RSSSF extraídos das 9 URLs do manifesto | 2.346 |
| Candidatos classificados automaticamente como CONFIRMADO_PRINCIPAL | 926 |
| PENDENTE_RSSSF | 16.910 |
| Proporção de candidatos com correspondência | 5,1917% |
| Proporção sem correspondência | 94,8083% |
| Testes automatizados aprovados | 8 |

**Interpretação correta:** o matcher comparou **todos os 17.836** jogos, mas o catálogo RSSSF ainda cobre somente **9 páginas**; os 926 são correspondências *automáticas candidatas*, não jogos submetidos individualmente a revisão humana. O total auditado externamente e individualmente permanece distinto.

## Métodos e restrições

Normalização determinística de nomes, igualdade exata de mandante e visitante no mesmo sentido, placar exato, ano aproximado e janela de data de 3 dias. Ocorrências múltiplas ou ausência de data devem receber revisão. O parser aceita linha simples com placar, datas abreviadas entre colchetes, espaços/tabs e anotação de campo neutro. **Não é um parser universal**: pode omitir jogos em páginas HTML estruturadas, e os aliases ainda não estão completos. Nomes homônimos de estados diferentes demandam ajuste adicional para evitar falsos positivos.

Foram identificados previamente **2 jogos com indicação de Sub-20** pela Caixa e **92 datas de jogo vazias**; esta execução não acrescentou certificações RSSSF dessas categorias. O pipeline gerou `rsssf_catalog.csv` e `resultado.csv` em um artefato do GitHub Actions. Dados originais permanecem intocados no repositório de origem; os 13 snapshots usados na branch são cópias destinadas exclusivamente à auditoria.

## Evidência da execução

- Workflow: https://github.com/marcosvilhena87/Loteca.FiveThirtyEight/actions/runs/41231041932
- Artefato: `rsssf-audit-evidence` (ver página da execução, seção Artifacts).
- Manifesto: `auditoria/rsssf/manifest_2002.csv`
- Código: `src/loteca_fivethirtyeight/rsssf_match.py`

## Bloqueios para cobertura de 2002–2026

É preciso indexar fontes estaduais das 27 unidades federativas, séries nacionais, copas regionais, torneios internacionais e futebol de seleções, por ano. Além disso, tratar temporadas que atravessam dezembro/janeiro, datas incompletas, mudanças de nome, diferentes competições de mesmo time/placar, ocorrências de clubes homônimos em estados distintos e páginas RSSSF sem linhas de placar parseáveis. A medição 5,1917% deve ser vista como **cobertura parcial do catálogo atual**, não como proporção final de partidas de primeira equipe.
