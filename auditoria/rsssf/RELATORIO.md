# Auditoria RSSSF da Loteca — levantamento inicial (31/10/2026)

## Escopo e resultado

- Fonte preservada: 13 arquivos CSV originais de `marcosvilhena87/Loteca/dados`, lidos sem alteração.
- Concursos 1–1274; **17.836 jogos**; 14 jogos por concurso.
- **7 jogos ( 0.0392% )** com confirmação direta documentada na RSSSF nesta etapa: concurso 1, jogos 1–4 e 12–14, Torneio Rio–São Paulo 2002, https://www.rsssfbrasil.com/tablesr/rjsp2002.htm.
- **17829 jogos ainda sem confirmação documental individual RSSSF (99.9608%)**; a ausência de confirmação *não é evidência de jogo inexistente nem de categoria inferior*.
- **2 partidas com nomes contendo explicitamente 'Sub 20'**: indício de competição de base, ainda sem verificação externa da competição.
- **92 registros sem data de jogo** (não equivale a jogo inválido).
- **0** registros repetidos pelo identificador concurso+jogo; **0** resultados 1/X/2 incompatíveis com os placares preenchidos; **0** concursos incompletos.

## Metodologia e limites

A confirmação exige evidência documental individual da RSSSF de confronto, placar e contexto de competição principal; variantes de grafia e divergência de data serão registradas separadamente. A evidência de uma competição de primeira equipe não comprova o elenco escalado. Sem evidência externa suficiente, o estado é `PENDENTE_PESQUISA`. O classificador `INDICIO_CATEGORIA_BASE` baseia-se somente na denominação do CSV e não é verificação externa. Não transformar estes pendentes em confirmados apenas porque as colunas e o placar são coerentes.

## Resumo por arquivo

| CSV | Jogos | RSSSF confirmados | Pendentes | Indícios base | Data ausente |
|---|---:|---:|---:|---:|---:|
| Loteca_0001-0100.csv | 1400 | 7 | 1393 | 0 | 11 |
| Loteca_0101-0200.csv | 1400 | 0 | 1400 | 0 | 3 |
| Loteca_0201-0300.csv | 1400 | 0 | 1400 | 0 | 13 |
| Loteca_0301-0400.csv | 1400 | 0 | 1400 | 1 | 5 |
| Loteca_0401-0500.csv | 1400 | 0 | 1400 | 0 | 5 |
| Loteca_0501-0600.csv | 1400 | 0 | 1400 | 0 | 10 |
| Loteca_0601-0700.csv | 1400 | 0 | 1400 | 0 | 16 |
| Loteca_0701-0800.csv | 1400 | 0 | 1400 | 1 | 23 |
| Loteca_0801-0900.csv | 1400 | 0 | 1400 | 0 | 6 |
| Loteca_0901-1000.csv | 1400 | 0 | 1400 | 0 | 0 |
| Loteca_1001-1100.csv | 1400 | 0 | 1400 | 0 | 0 |
| Loteca_1101-1200.csv | 1400 | 0 | 1400 | 0 | 0 |
| Loteca_1201-1300.csv | 1036 | 0 | 1036 | 0 | 0 |

## Indícios de base
- Concurso 393, jogo 1: FLUMINENSE/RJ/Sub 20 x CRUZEIRO/MG - SUB 20 (1-1), domingo, 13/12/2009.
- Concurso 781, jogo 7: TUBARÃO/SC SUB 20 x FLUMINENSE/RJ/Sub 20 (3-2), sábado, 06/01/2018.

## Próximas validações

1. Extrair e indexar as tabelas RSSSF por competição/ano, com sua URL, categoria e identificação de rodada.
2. Resolver aliases por equipe e estado/país, preservando grafias originais; proibir matching apenas por placar.
3. Correspondência por confronto, placar, ano e proximidade temporal, com classificação explícita de divergências.
4. Revisão manual dos ambíguos, inclusive registros sem data, antes da inclusão em modelos Elo ou backtests.

## Arquivos gerados

- `rsssf_jogos_status.csv`: inventário integral de 17836 jogos com a evidência disponível e o estado da auditoria;
- `rsssf_resumo_por_arquivo.csv`: totais e percentuais calculáveis por arquivo;
- `rsssf_excecoes.csv`: lista de 94 ocorrências de dados incompletos e indícios de base (podem coexistir no mesmo jogo).

**Importante:** trata-se de um levantamento completo de integridade da base e uma auditoria RSSSF ainda parcial. Não alegamos conferência RSSSF para os outros 17829 jogos.
