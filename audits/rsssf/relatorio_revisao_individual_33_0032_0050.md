# Revisão individual das 33 exceções da Caixa — concursos 0032–0050

Execução anterior com 33 pendências: https://github.com/marcosvilhena87/Loteca.FiveThirtyEight/actions/runs/41241877018

Nova execução com Paulista B1 e Goiano: https://github.com/marcosvilhena87/Loteca.FiveThirtyEight/actions/runs/41242282824

CSV auditável com 33 linhas e URLs por partida: [revisao_classificada_33_0032_0050.csv](revisao_classificada_33_0032_0050.csv).

## Classificação dos 33 casos

- **16 casos de denominação/identidade a verificar:** 44/4–5, 45/3, 46/9 e 46/12, 47/1 (Espanha); 48/1 e 49/1 (Carioca); 49/8, 50/4, 50/9 (Paulista); 49/10–12, 50/5–6 (Mineiro). Não inferir que mero alias basta: verificar jogo na fonte.
- **16 casos de cobertura de fase/formato/fonte:** 35/13, 38/7–11 e 38/13 (Paulista B1 2002); 35/6, 35/12, 40/8, 44/1 (Série B 2002); 42/1–4 e 45/1 (Série A 2002, eliminatórias). Fonte da B1 anteriormente ausente. As eliminatórias da Série A e B têm mandos e placares compactados em ida/volta, não interpretados pelo parser regular.
- **1 competição ausente:** 50/14 Goiás 1-0 Vila Nova, em 02/02/2003. Referência comprovada: https://www.rsssfbrasil.com/tablesfq/go2003.htm, rodada 7.

**Divergência documental efetivamente comprovada de data/placar:** nenhuma das 33 nesta revisão; é importante diferenciar "não encontrou candidato" de "a Caixa contradiz a RSSSF". O status dessas linhas permanece pendente até correspondência exata verificada.

## Checagens documentais pontuais
- 35/6 Sport 3-0 CRB e 35/12 Sampaio Corrêa 1-0 XV de Novembro constam da rodada 16 da Série B 2002: https://www.rsssfbrasil.com/tablesae/br2002l2.htm.
- 42/1–4: os confrontos e primeiros placares das quartas de final da Série A estão explícitos em https://www.rsssfbrasil.com/tablesae/br2002.htm.
- 50/14 Goiás 1-0 Vila Nova: 02/02/2003, rodada 7: https://www.rsssfbrasil.com/tablesfq/go2003.htm.
- A Série B1 paulista 2002 usa a tabela de 16 clubes, 30 jogos por clube (240 partidas regulares), mais fase final: https://mail.rsssfbrasil.com/tablessz/sp2002l4.htm.

## Efeito da ampliação executada
- Fontes RSSSF no manifesto: **13**, todas aprovadas pelas verificações *configuradas*.
- Novos registros: Paulista B1 2002 **240**, Goiano 2003 **80**; não equivale a comprovação de fases finais completas.
- Caixa (266 jogos): **235 candidatos únicos**, **28 sem candidato**, **3 sorteios bloqueados**.
- Houve redução de **cinco** pendências com as duas fontes novas (de 33 para 28). Os registros que se resolveram estão no artefato de conciliação; o CSV da revisão mantém os 33 casos originais para trilha de auditoria.
- **0 entradas aprovadas automaticamente ao Elo.** Homônimos, equipes B e resultados administrativos continuam bloqueados.

## Limitações da revisão
Categorias estabelecem o principal fator de bloqueio e a fonte a consultar; não equivalem a 33 reconciliações documentais concluídas. É preciso reexecutar o diagnóstico para os 28 remanescentes e inspecionar manualmente aqueles que só têm alias provável. O extrator de fases eliminatórias deverá interpretar explicitamente as duas pernas do confronto, suas respectivas datas e eventuais decisões administrativas.
