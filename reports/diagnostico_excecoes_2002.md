# Diagnóstico das 1.329 exceções — Execução GitHub Actions 41228977833

## Proveniência
- Execução: https://github.com/marcosvilhena87/Loteca.FiveThirtyEight/actions/runs/41228977833
- Artefato: `rsssf-2002-auditoria` (ID 13052728234)
- Arquivos inspecionados: `cruzamento_0001_0100.csv` (1.400 linhas) e `rsssf_extraido.csv` (158 linhas).
- Fonte: somente Rio–São Paulo 2002 (126 jogos) e Copa dos Campeões 2002 (32 jogos).

## Quantificação rigorosa

| Situação reportada pelo algoritmo | Registros |
|---|---:|
| Confirmado historicamente pelo cruzamento exato | 71 |
| Pendente — alias ausente ou identidade ambígua | 943 |
| Pendente — nenhuma correspondência estrita | 375 |
| Pendente — sorteio lotérico | 11 |
| **Total Loteca 1–100** | **1.400** |

### Detalhamento das 375 sem correspondência

Comparando a **data exata** de cada registro com as datas dos 158 confrontos extraídos:

- **362** estão em datas nas quais **nenhum** jogo das duas competições aparece na RSSSF extraída. Não existe fundamento para chamar isso de divergência de placar ou de data; são, em geral, outras competições ou períodos.
- **13** estão em datas com pelo menos um jogo de uma das competições, mas não coincidem com os confrontos extraídos. Isso não comprova divergência de placar: pode ser simplesmente uma outra competição.
- **0 discrepâncias individuais de placar ou datas confirmadas nesta classificação**, pois tal conclusão exige confronto entre o mesmo mandante, visitante e competição, depois de resolver os aliases.

### Os 943 bloqueios por alias

É número de **jogos**, não quantidade de clubes sem alias. A falta de pelo menos um identificador faz o cruzador encerrar a tentativa antes de procurar o confronto. Mesmo que o jogo fosse de outra competição, o algoritmo reportaria `alias ausente ou identidade ambígua`.

Nomes recorrentes que merecem catalogação por entidade, estado e categoria: Internacional/RS, Figueirense/SC, Juventude/RS, Coritiba/PR, Paraná/PR, Criciúma/SC, Fortaleza/CE, Santa Cruz/PE, Joinville/SC, Vila Nova/GO, América/MG.

**Não adicionar aliases indiscriminadamente para inflar a taxa de confirmação**: o conjunto fonte contém apenas duas competições, e a resolução deve continuar distinguindo homônimos, seleções, equipes B e de base.

### 11 sorteios

Cada placar lotérico continua dissociado de placar esportivo. Sem fonte para o jogo ocorrido em campo, não gerar resultado 1X2 para o Elo.

## Ações recomendadas

1. Adicionar diagnóstico `fora_do_escopo_da_competicao_extraida` antes de etiquetar uma divergência de placar. Um erro de correspondência não é necessariamente erro de registro.
2. Expandir os extratores às competições que cobrem os meses e os clubes pendentes (Sul-Minas, Nordeste, estaduais e Série A).
3. Criar aliases canônicos aprovados e com distinção de estado/categoria, preservando em relatório as variantes observadas em cada fonte.
4. Produzir divergências de **placar** apenas quando **data, mandante, visitante e competição** coincidirem. Produzir divergência de **data** apenas quando **mandante, visitante, placar e competição** coincidirem, com verificação de múltiplos encontros na temporada.
5. Manter `elo_liberado=nao` para todas as exceções e para correspondências que ainda não passaram pelo gate final.

Este relatório deriva de artefatos de execução, não de estimativa.
