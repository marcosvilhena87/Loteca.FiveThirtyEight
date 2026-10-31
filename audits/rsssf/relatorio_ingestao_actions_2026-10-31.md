# Resultado da ingestão RSSSF no GitHub Actions — 31/10/2026

- Execução: https://github.com/marcosvilhena87/Loteca.FiveThirtyEight/actions/runs/41240304825
- Status: **success** (workflow de testes e extração).
- Artefato HTML, CSV e metadata: https://github.com/marcosvilhena87/Loteca.FiveThirtyEight/actions/runs/41240304825/artifacts/13057460914
- Fontes: 8, downloads falhos: 0, linhas candidatas extraídas: 3729.
- **Aprovações Elo por esta execução: zero**.

| Fonte | Linhas extraídas | Esperado | Diagnóstico |
|---|---:|---:|---|
| Brasileiro Série A 2002 | 324 | Não estabelecido | Sem validação de cobertura |
| Brasileiro Série B 2002 | 325 | Não estabelecido | Sem validação de cobertura |
| Espanhol 2002/03 | 470 | 380 | FALHA, 90 linhas extras |
| Italiano 2002/03 | 2300 | 306 | FALHA, 1994 linhas extras |
| Carioca 2003 | 64 | Não estabelecido | Sem validação de cobertura |
| Paulista 2003 | 103 | Não estabelecido | Sem validação de cobertura |
| Mineiro 2003 | 78 | Não estabelecido | Sem validação de cobertura |
| Brasiliense 2003 | 65 | Não estabelecido | Sem validação de cobertura |

A palavra `pass` em `integrity_report.json` significa somente aprovação **das checagens implementadas**, não completude histórica. O parser atual processa páginas inteiras, inclusive possíveis divisões e seções adicionais, e pode atribuir datas erradas a jogos em formatos não suportados. Os CSVs gerados são **candidatos**, não fatos homologados.

## Próximas correções
1. Restringir extração por seção e divisão, sobretudo Espanha e Itália.
2. Definir quantitativos esperados por fase e competição, inclusive fases finais.
3. Detectar jogos sem data, cabeçalhos de classificação, vitórias administrativas e prorrogações.
4. Validar cada confronto de 0032–0050 pela data, mandante, visitante e placar; não aprovar por similaridade isolada.
