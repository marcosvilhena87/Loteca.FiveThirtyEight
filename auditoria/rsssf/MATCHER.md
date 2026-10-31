# Matcher RSSSF (versão inicial)
O módulo `rsssf_match.py` cruza os CSVs da Caixa com um catálogo de resultados transcritos das páginas RSSSF. **Nenhum registro original é modificado**.

## Execução
1. Prepare `manifest.csv` com colunas `competition;year;category;url` e URLs RSSSF.
2. Gere catálogo textual (em Python): `from loteca_fivethirtyeight.rsssf_match import download_catalog; from pathlib import Path; download_catalog(Path("manifest.csv"),Path("cache/rsssf"))`.
3. Execute `python -m loteca_fivethirtyeight.rsssf_match --source caminho/para/13_csvs --catalog cache/rsssf/rsssf_catalog.csv --output cache/resultado.csv`.
4. Teste com `pytest tests/test_rsssf_match.py -q`.

**Estados:** `CONFIRMADO_PRINCIPAL` (único confronto, placar e data próximos, competição principal), `OUTRA_CATEGORIA` (catalogada fora de principal), `REVISAO_DATA` (sem data verificável), `AMBIGUO` (múltiplas evidências), `PENDENTE_RSSSF` (não encontrado).

**Limitações deliberadas:** parser cobre linhas simples de resultados e datas [Feb 17], não todos os formatos da RSSSF; HTML complexo, datas de virada de ano, linhas com observações e aliases incompletos exigem revisão. Correspondências incertas nunca são automaticamente confirmadas. O catálogo deve ser ampliado/validado e o parser ajustado aos formatos de cada campeonato; nenhum percentual novo é alegado sem rodar a comparação. Resultados não confirmados não devem ser usados como exemplos de equivalência.
