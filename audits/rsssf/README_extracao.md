# Extratores RSSSF e validação de execução

O módulo `extract_rounds.py` processa páginas RSSSF HTML **salvas localmente**. Serve para Brasileiro A/B 2002, Espanha e Itália 2002/03, estaduais 2003 quando adotam rodadas no formato `[Oct 5]` e placar `Time 2-1 Team`. Algumas tabelas usam outras estruturas; os casos não extraídos exigem parser especializado. Não completar placares por inferência.

Exemplo:
```bash
python -m audits.rsssf.extract_rounds --html br2002.html --year 2002 --competition "Brasileirão Série A 2002" --source-url https://www.rsssfbrasil.com/tablesae/br2002.htm --out rsssf_matches.csv
python -m audits.rsssf.reconcile_auto --caixa audits/rsssf/caixa_0032_0050.csv --rsssf rsssf_matches.csv --aliases audits/rsssf/aliases_temporais.csv --out candidatos.csv
```

Fontes-alvo:
- https://www.rsssfbrasil.com/tablesae/br2002.htm
- https://www.rsssfbrasil.com/tablesae/br2002l2.htm
- https://www.rsssf.org/tabless/span03.html
- https://www.rsssf.org/tablesi/ital03.html
- https://www.rsssfbrasil.com/tablesr/rj2003.htm

### Limitação da execução
O ambiente não conseguiu recuperar os HTML RSSSF diretamente por DNS. Foi executado um teste real de correspondência com 10 linhas selecionadas de resultados transcritos das fontes RSSSF e 10 linhas Caixa; 10 candidatos únicos, sem liberação para Elo. Isso **não é execução integral dos 266 jogos**. Para um relatório exaustivo, arquivar as páginas de todas as competições e executar extratores; conferir a quantidade de partidas e os resultados por rodada antes da homologação.
