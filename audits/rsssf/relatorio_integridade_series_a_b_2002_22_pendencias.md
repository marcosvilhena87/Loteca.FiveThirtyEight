# Auditoria de cobertura regular Série A e B 2002 — execução 31/10/2026

Workflow com auditoria fail-closed: https://github.com/marcosvilhena87/Loteca.FiveThirtyEight/actions/runs/41242996929

## Identificação dos dois falsos jogos da Série A
Na extração anterior, a regex interpretava metadados detalhados das finais como resultado:
- `Date: 17:00 (local time), Dec 8th`
- `Date: 17:00 (local time), Dec 15th`

Ambos foram identificados no relatório de frequências como um par artificial `date` versus `local time dec 8th/15th`. **Não são jogos nem divergências da RSSSF**. A correção restringe a extração regular à seção anterior a `Quarterfinals` e extrai eliminatórias em rotina independente.

## Série A — resultado validado
- 325 partidas regulares distintas entre pares de equipes.
- 26 equipes identificadas, cada qual com exatamente 25 jogos, sem nenhum par duplicado ou ausente.
- 8 jogos de quartas de final, 4 semifinais, 2 finais.
- **339 partidas/placares, sendo 325 + 14.**
- Nenhuma duplicidade por par regular identificada.

## Série B — resultado validado
- 325 partidas regulares distintas entre pares de equipes.
- 26 equipes identificadas, cada qual com exatamente 25 jogos, sem nenhum par duplicado ou ausente.
- 8 jogos de quartas de final, 4 semifinais, 2 finais.
- **339 partidas/placares, sendo 325 + 14.**
- Nenhuma duplicidade por par regular identificada.

As duas contagens são exigidas como invariantes no GitHub Actions; eventual regressão causa falha do job. Os arquivos `brazil_2002_fixture_audit.json` e `integrity_report.json` estão no artefato da execução.

## Reavaliação real dos 266 jogos da Caixa
- 241 candidatos únicos para revisão, 22 ainda sem candidato e três sorteios bloqueados.
- Não houve mudança na correspondência causada pela remoção dos dois falsos jogos.
- **Nenhuma homologação Elo automática.**

### 22 pendências, agrupadas por provável origem da fonte
- Série B 2002 (3): 35/6, 35/12, 40/8.
- Paulista B1 2002 (3): 35/13, 38/10, 38/13.
- Espanhol 2002/03 (6): 44/4, 44/5, 45/3, 46/9, 46/12, 47/1.
- Carioca 2003 (2): 48/1, 49/1.
- Paulista 2003 (3): 49/8, 50/4, 50/9.
- Mineiro 2003 (5): 49/10, 49/11, 49/12, 50/5, 50/6.

Essa categorização por fonte **não é diagnóstico confirmado** de alias, placar ou data. Os 22 continuam sujeitos à revisão de identidade, documentação, data e cobertura de fases específicas. O registro 46/12 permanece especialmente suspeito de diferença de calendário/fonte, mas não foi estabelecida divergência factual.

## Próxima prioridade
1. Tratar aliases pontuais e localizar cada resultado RSSSF desses 22 jogos, com data.
2. Conferir jogos da Série B e Paulista B1 que estão na RSSSF mas escapam ao matcher por formato textual.
3. Não promover candidatos ao Elo sem revisão documental e sem status distinto para jogos administrativos.
