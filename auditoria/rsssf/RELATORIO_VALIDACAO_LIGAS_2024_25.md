# Auditoria integral das ligas internacionais 2024/25 — 31/10/2026

## Evidência executada
GitHub Actions: https://github.com/marcosvilhena87/Loteca.FiveThirtyEight/actions/runs/41234904460

**7 testes aprovados**. O arquivo `international-rsssf-evidence` inclui `international_matches.csv`, `international_source_audit.csv`, `league_integrity_summary.csv`, `league_integrity_issues.csv` e `international_review.csv`.

| Campeonato 2024/25 | RSSSF extraídas | Confrontos distintos com ID mandante e visitante | Clubes identificados | Inconsistências estruturais |
|---|---:|---:|---:|---:|
| La Liga | 380 | 380 | 20 | 0 |
| Premier League | 380 | 380 | 20 | 0 |
| Serie A italiana | 380 | 380 | 20 | 0 |

Critérios de verificação: jogo datado, sentido mandante/visitante, ID canônico único por equipe no âmbito do campeonato, sem confronto repetido, sem autojogo, **19 jogos em casa e 19 fora para cada um dos 20 clubes**. Conjunto de 380 partidas com estrutura completa em cada liga.

## Correções específicas
- **Premier League:** 18 jogos não extraídos em rodadas alternadas por largura fixa e apenas um espaço entre a grafia longa `Wolverhampton` e o placar. A regex passou a aceitar um espaço. O resultado subiu de **362 para 380**.
- **Espanha:** páginas com codificações legadas geravam nomes truncados por erro de charset (e.g., Atlético, Alavés, Leganés). O download tenta a codificação da resposta e usa Latin-1 como fallback. A auditoria identificou os 20 clubes.
- **Itália:** a página RSSSF registra **Fiorentina–Inter abandonado em 1/12/2024 e retomado em 6/2/2025**, com anotações próximas a Lecce–Juventus. O parser deixou de interpretar o resultado parcial na nota como jogo e eliminou notas agregadas ao nome do adversário; mantém a data/placar válidos do jogo concluído.
- **IDs:** foram cadastrados aliases específicos do campeonato para os 60 participantes e corrigida a duplicação do identificador Liverpool.

Fontes RSSSF:
- https://rsssf.org/tabless/span2025.html
- https://rsssf.org/tablese/eng2025.html
- https://rsssf.org/tablesi/ital2025.html

## Correspondência com a Loteca
A comparação exige mandante e visitante individualmente identificados, data exata, resultado 1X2 expresso pelo placar, competição específica e proveniência RSSSF. Nesta execução, **79 candidatos** cumpriram a correspondência estrita com o conjunto de aliases cadastrado. Todos têm status `REVIEW_ONLY_UNVERIFIED_ALIAS`; nenhuma nova partida foi automaticamente promovida a dataset Elo.

## Nível de validação
**Completada:** extração e auditoria de integridade estrutural dos **1.140 confrontos** das três ligas em 2024/25.
**Ainda não completada:** verificação manual independente de cada placar em uma segunda fonte e revisão final de todos os 79 candidatos da Caixa. Os aliases contextuais derivam da lista RSSSF e das variantes Caixa, permanecendo sob `SOURCE_REVIEW_PENDING`, não são certificação histórica para todas as temporadas.

O Mundial de Clubes 2025 ainda registra 50 linhas extraídas, sem cobertura completa validada; Libertadores segue com fonte parcial, não anual.
