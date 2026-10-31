# Extratores RSSSF especializados — 2002

As páginas são texto HTML antigo (frequentemente codificação Windows-1252) e usam cabeçalhos por rodada/fase, datas entre colchetes e resultados linha a linha. O extrator `rsssf_extractors.py` foi criado para:

- Rio–São Paulo 2002: https://www.rsssf.org/tablesr/riospl02.html
- Copa dos Campeões 2002: https://www.rsssf.org/tablesb/brazchampcup02.html

## Utilização

```bash
python -m loteca_fivethirtyeight.rsssf_extractors --competition all --output data/evidencias/rsssf_2002_extraido.csv
python -m loteca_fivethirtyeight.rsssf_match --loteca data/cache_loteca/Loteca_0001-0100.csv --rsssf data/evidencias/rsssf_2002_extraido.csv --output reports/cruzamento_rsssf_2002.csv
pytest -q tests/test_rsssf_extractors.py tests/test_rsssf_match.py
```

Para testes sem internet: `--competition rio_sp_2002 --input-html caminho/pagina.html` (equivalente Copa dos Campeões).

Extração inclui data, mando, clubes, placar, competição, URL, fase, rodada/grupo e nível B. Resultados de pênaltis em parênteses **não são convertidos** em novo jogo ou em resultado aos 90 minutos.

**Controle de qualidade**: erro se não extrair partidas, se duplicar confronto idêntico ou se a competição for desconhecida. A estrutura RSSSF muda conforme a página; revisar exceções e comparar totais publicados antes de aceitar lote. Os testes com trechos reais foram escritos; execução em CI ainda pendente.

A correspondência obtida é apenas evidência histórica. Não altera `elo_gate` nem libera jogos ao Elo automaticamente. O módulo `rsssf_match` exige aliases explícitos para ambos os clubes e arquiva divergências para revisão.
