# Homologação técnica da conciliação Caixa × RSSSF — 31/10/2026

Execução efetiva GitHub Actions: https://github.com/marcosvilhena87/Loteca.FiveThirtyEight/actions/runs/41244300120

## Caso documental 0048/01
- Caixa: Vasco da Gama 1×0 América-RJ, **18/01/2003**.
- RSSSF: Vasco da Gama 1×0 América-RJ, **16/01/2003**, https://www.rsssfbrasil.com/tablesr/rj2003.htm.
- Fontes independentes contemporâneas ou com histórico identificável confirmam 18/01/2003:
  - https://www.netvasco.com.br/news/noticias07/9957.shtml (ficha técnica completa).
  - https://www.bolanaarea.com/estaduais_rj_2003.htm (primeira rodada; 18/01 às 16h).
  - https://mprais.netvasco.com.br/vasco/2003rj.html (registro do clube).
- Decisão: **`data_rsssf_divergente_documentada`**. Manter a data original da fonte e a da Caixa; vinculação excepcional documentada, sujeita a homologação humana, sem mudança no HTML nem liberação Elo.

## Auditoria estrita dos 266 registros
- 30 `evidencia_estrita_para_revisao`: linha RSSSF única, nomes com IDs canônicos determinados, datas e placares coincidentes.
- 232 `identidade_incompleta`: os aliases existentes ainda não atribuem IDs inequívocos aos dois lados; similaridade textual não basta.
- 1 `data_rsssf_divergente_documentada`: Vasco × América (0048/01).
- 3 `sorteio_bloqueado`.
- **0 elegíveis automaticamente ao Elo**. Mesmo os 30 exigem revisão documental formal antes da promoção.

A matriz individual `audit_candidates.csv` e o resumo `audit_summary.json` estão arquivados nos artefatos da execução. O código em `audits/rsssf/audit_candidates.py` valida a linha-fonte, competição, data, placar e IDs canônicos; gera estado de evidência distinto de elegibilidade Elo.

## Próximas ações
1. Construir um catálogo explícito de participantes por temporada e competição, associando cada nome RSSSF e Caixa a IDs canônicos, com intervalos temporais, sem unir América-RJ/MG, Botafogo-RJ/SP, XV Piracicaba/Caraguatatuba, Guarani/Guarany ou equipes B.
2. Reexecutar a auditoria estrita e só homologar após prova documental de cada identificação, preservando evidências e responsáveis.
3. Conferir datas e placares por fonte independente nos casos marcados para revisão.
