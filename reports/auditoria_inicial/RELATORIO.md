# Auditoria estática inicial — 31/10/2026

Fonte: 13 CSVs da branch main de marcosvilhena87/Loteca/dados.
**Atenção:** análise estrutural efetivamente executada; pesquisa esportiva integral e validação individual de 17.836 confrontos NÃO foram executadas.

## Resultados confirmados por leitura completa dos CSVs
- Registros: 17836
- Concursos distintos: 1274
- Intervalos não representados: 1275, 1276, 1277, 1278, 1279, 1280, 1281, 1282, 1283, 1284, 1285, 1286, 1287, 1288, 1289, 1290, 1291, 1292, 1293, 1294, 1295, 1296, 1297, 1298, 1299, 1300
- Jogos com sorteio='SIM': 92 (bloquear Elo)
- Registros com marcador explícito B/base/feminino no nome por heurística: 14 (revisão)
- Duplicidades concurso+jogo: 0
- Resultados 1X2 incompatíveis com placar numérico: 0

## Exceções prioritárias

| Concurso | Jogo | Mandante | Visitante | Motivo |
|---:|---:|---|---|---|
| 13 | 5 | DEPORTIVO | REAL MADRID | Sorteio; data_jogo vazia |
| 20 | 1 | SANTA CRUZ/PE | NAUTICO/PE | Sorteio; data_jogo vazia |
| 24 | 14 | MONTENEGRO/SP | PONTE PRETA B/SP | Sorteio; data_jogo vazia |
| 25 | 13 | ATLETICO/PB | CAMPINENSE/PB | Sorteio; data_jogo vazia |
| 31 | 8 | AMERICA/MG | SAO RAIMUNDO/AM | Sorteio; data_jogo vazia |
| 38 | 12 | FERNANDOPOLIS/SP | GUARULHOS/SP | Sorteio; data_jogo vazia |
| 43 | 1 | REAL MADRID | SEVILLA | Sorteio; data_jogo vazia |
| 44 | 13 | TORINO | ATALANTA | Sorteio; data_jogo vazia |
| 56 | 13 | AMERICA/SP | PONTE PRETA/SP | Sorteio; data_jogo vazia |
| 56 | 14 | GREMIO/RS | CAXIAS/RS | Sorteio; data_jogo vazia |
| 57 | 8 | PONTE PRETA/SP | MARILIA/SP | Sorteio; data_jogo vazia |
| 136 | 8 | SANTA CRUZ/PE | ITUANO/SP | Sorteio; data_jogo vazia |
| 137 | 11 | SAO  CAETANO/SP | PARANA/PR | Sorteio; data_jogo vazia |
| 152 | 10 | ATHLETICO/PR | PARANAVAI/PR | Sorteio; data_jogo vazia |
| 204 | 8 | REMO/PA | ANANINDEUA/PA | Sorteio; data_jogo vazia |
| 205 | 9 | SANTA CRUZ/PE | SPORT/PE | Sorteio; data_jogo vazia |
| 207 | 3 | JUAZEIRO/BA | VITORIA/BA | Sorteio; data_jogo vazia |
| 207 | 9 | COLO COLO/BA | FLUMINENSE/BA | Sorteio; data_jogo vazia |
| 227 | 9 | BRASILIENSE/DF | MARILIA/SP | Sorteio; data_jogo vazia |
| 249 | 3 | AMERICANO/RJ | FLAMENGO/RJ | Sorteio; data_jogo vazia |

## Categoria de equipe — casos selecionados
- Concurso 20, jogo 11: PALMEIRAS B/SP x JABOTICABAL/SP; domingo, 23/06/2002 — **bloqueado até confirmação**.
- Concurso 21, jogo 7: OESTE/SP x PALMEIRAS-B/SP; domingo, 30/06/2002 — **bloqueado até confirmação**.
- Concurso 24, jogo 13: CORINTHIANS B/SP x GUACUANO/SP; domingo, 21/07/2002 — **bloqueado até confirmação**.
- Concurso 24, jogo 14: MONTENEGRO/SP x PONTE PRETA B/SP; data ausente — **bloqueado até confirmação**.
- Concurso 25, jogo 5: PONTE PRETA B/SP x JOSEENSE/SP; domingo, 28/07/2002 — **bloqueado até confirmação**.
- Concurso 26, jogo 11: ELOSPORT/SP x PONTE PRETA B/SP; domingo, 04/08/2002 — **bloqueado até confirmação**.
- Concurso 26, jogo 12: CORINTHIANS B/SP x SC PAULISTA/SP; domingo, 04/08/2002 — **bloqueado até confirmação**.
- Concurso 81, jogo 13: SAO PAULO B/SP x NACIONAL/SP; domingo, 07/09/2003 — **bloqueado até confirmação**.
- Concurso 81, jogo 14: SANTO ANDRE/SP x SAO CAETANO B/SP; domingo, 07/09/2003 — **bloqueado até confirmação**.
- Concurso 393, jogo 1: FLUMINENSE/RJ/Sub 20 x CRUZEIRO/MG - SUB 20; domingo, 13/12/2009 — **bloqueado até confirmação**.
- Concurso 637, jogo 14: CONFIANCA/SE x BOCA JUNIOR/SE; domingo, 25/01/2015 — **bloqueado até confirmação**.
- Concurso 685, jogo 11: ITABAIANA/SE x BOCA JUNIOR/SE; domingo, 24/01/2016 — **bloqueado até confirmação**.
- Concurso 697, jogo 6: CONFIANCA/SE x BOCA JUNIOR/SE; domingo, 17/04/2016 — **bloqueado até confirmação**.
- Concurso 781, jogo 7: TUBARÃO/SC SUB 20 x FLUMINENSE/RJ/Sub 20; sábado, 06/01/2018 — **bloqueado até confirmação**.

## Evidências externas obtidas
- CAIXA, regras oficiais: sorteio define o resultado lotérico de jogo que não ocorreu na janela; resultado sorteado não é placar esportivo. https://loterias.caixa.gov.br/Paginas/regras-sorteios.aspx
- CAIXA, Loteca: modalidades nacionais, estaduais e regionais; a apuração por sorteio não substitui partida disputada. https://loterias.caixa.gov.br/Paginas/Loteca.aspx
- RSSSF Brasil, Paulista Série B-2 2002: Ponte Preta B (Ponte Preta Sumaré) é identificada explicitamente como equipe B, e Montenegro consta como desistente; documentação histórica não equivale a súmula oficial. https://www.rsssfbrasil.com/tablessz/sp2002l5.htm

## Política de liberação
Nenhum jogo foi liberado por esta auditoria. Necessário cruzar competição + categoria + jogo + data com fonte oficial, dar identidade de clube e registrar o URL e método da validação. Não interpretar 'Não Demonstrado' como 'Não' confirmado.

## Pesquisa externa direcionada — achados documentados

1. **Concurso 24, jogo 14 (2002)**: Montenegro/SP x Ponte Preta B/SP. Campo sorteio='SIM', sem data de jogo. A RSSSF Brasil identifica a equipe Ponte Preta Sumaré como **equipe B** da Ponte Preta e registra que os jogos envolvendo Montenegro foram cancelados. **Bloqueio definitivo para Elo de equipes principais quanto a este registro**, por sorteio e categoria B. Confiança alta para bloqueio; fonte histórica secundária para identidade: https://www.rsssfbrasil.com/tablessz/sp2002l5.htm
2. **Concurso 781, jogo 7 (06/01/2018)**: Tubarão-SC 3x2 Fluminense-RJ. Partida da Copa São Paulo de Futebol Júnior (Copinha), competição Sub-20, confirmada por cobertura contemporânea com data e placar. **Excluir Elo principal**. Fontes independentes: https://www.lance.com.br/fluminense/fluminense-perde-virada-para-tubarao-fica-vice-lideranca-grupo.html e https://www.opovo.com.br/esportes/futebol/times/fluminense/2018/01/amp/fluminense-e-surpreendido-na-copinha-pelo-tubarao-sc.html
3. **Concursos 20, 21, 24, 25, 26 e 81**: múltiplas entradas com Palmeiras B, Corinthians B, Ponte Preta B, São Paulo B ou São Caetano B; **revisão e exclusão preventiva do Elo principal**. Algumas partidas ainda requerem conferência individual em fontes oficiais.
4. **Concurso 393, jogo 1 (13/12/2009)**: Fluminense Sub-20 x Cruzeiro Sub-20 (1x1); indicação explícita de base no CSV; **excluir preventivamente** até identificação de competição e confirmação externa do confronto.
5. **Marcador Boca Junior/SE** não é sinônimo de categoria júnior: o filtro simples gerou falso positivo e deve ser aprimorado.

### Hierarquia probatória
- CAIXA confirma apenas natureza lotérica do sorteio (https://loterias.caixa.gov.br/Paginas/regras-sorteios.aspx).
- Fonte oficial organizadora (CBF, Federação Paulista, CONMEBOL etc.) é desejável para certificar campeonato e categoria. Não foram obtidas súmulas oficiais das partidas históricas exemplificadas acima.
- RSSSF e imprensa contemporânea sustentam a triagem histórica, mas não devem ser relatadas como súmulas oficiais.

**Status final:** varredura estrutural integral dos 17.836 registros concluída; pesquisa externa direcionada nos casos citados; NÃO foi realizada pesquisa individual externa de todos os jogos por indisponibilidade de credencial de busca em lote. Nenhuma partida é liberada ao Elo.
