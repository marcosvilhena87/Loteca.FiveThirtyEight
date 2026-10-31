# Incorporação internacional RSSSF — estágio de verificação (31/10/2026)

## Catálogo por fonte
| Competição | Temporada | Fonte | Estado |
|---|---|---|---|
| Espanha, La Liga | 2024/25 | https://rsssf.org/tabless/span2025.html | Página acessível; parser ainda em validação, não certificada |
| Inglaterra, Premier League | 2024/25 | https://rsssf.org/tablese/eng2025.html | Página acessível; parser 0 registros, correção pendente |
| Itália, Serie A | 2024/25 | https://rsssf.org/tablesi/ital2025.html | Página acessível; parser 0 registros, correção pendente |
| Mundial de Clubes FIFA | 2025 | https://rsssf.org/tablesf/fifa-wcc2025.html | 50 linhas extraídas, revisão pendente |
| Libertadores | 2025 | Sem página anual RSSSF validada | Quarentena de fonte |

## Logs reais
Execução https://github.com/marcosvilhena87/Loteca.FiveThirtyEight/actions/runs/41233704128 : três testes de parser passaram; Espanha retornou **518 linhas** (quantidade acima dos 380 jogos da primeira divisão, sinal claro de mistura com outra competição e motivo de quarentena), Inglaterra e Itália **0**, Mundial **50**. Corrigido o limite de primeira divisão posteriormente, aguardando nova medição. Os resultados extraídos NÃO são certificados.

## Medidas implementadas
- Arquivo `international_sources.csv` separa URLs confirmadas de fonte sem verificação e não incorpora URLs hipotéticas.
- Módulo `international_rsssf.py` extrai resultados com data, placar, competição, URL e linha para triagem.
- Workflow `rsssf-international.yml` testa e publica artefato com auditoria por página.
- Testes `test_international_rsssf.py` usam partidas representativas (Premier League, La Liga e Mundial de 2025).
- **Ainda não há identificação contextual de todos os adversários** nem incorporação automática ao matcher da Caixa ou dataset Elo; isso exige mapping por competição e validação de todas as linhas.

## Aprovação
Bloquear promoção até haver contagem válida por campeonato e temporada (380 partidas por primeira divisão em 2024/25), sem vazamento de copas ou séries inferiores, além de mapeamento dos dois clubes para IDs institucionais. Datas e placares devem corresponder à Caixa; ambiguidades de Barcelona (ESP/ECU), Juventus e Milan devem permanecer abertas até confirmação contextual.
