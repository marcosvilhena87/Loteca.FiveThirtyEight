# Ingestão e arquivo imutável por execução — RSSSF

Rode a partir da raiz do repositório:

```bash
python -m audits.rsssf.ingest_sources --manifest audits/rsssf/sources_2002_2003.json --archive data/rsssf_archive
python -m pytest tests/test_rsssf_ingest_sources.py
```

Saídas por fonte: `source.html` (HTML original), `metadata.json` (URL, SHA-256, tamanho, diagnóstico e avisos), `matches.csv` (partidas candidatas), mais `integrity_report.json` geral. Guarde o snapshot antes de substituir em novas rodadas; não considere a opção de reutilização como prova de versão atual.

**Integridade:** erro de download é explicitado; formatos sem datas reconhecidas falham; expectativa de quantidade (380 Espanha, 306 Itália) é indicador, não prova de identidade nem completude; faixas de data e duplicidades são verificadas. Páginas com mais de uma divisão ou com resultados administrativos podem exigir extratores adicionais.

**Importante:** o parser genérico lê partidas com linha de data `[Oct 5]` e `Mandante 2-1 Visitante`; ainda NÃO entende todos os formatos da RSSSF. Não usar `matches.csv` como evidência aprovada sem validação de identidade, local, competição, data e placar. Falha de integridade bloqueia qualquer promoção para Elo.

Offline/reprocessamento: `--offline`, reutilizando snapshots previamente baixados. O processo usa somente biblioteca padrão do Python, restringe hosts RSSSF e aplica limite de tamanho e timeout. Respeitar políticas de acesso e não disparar muitas requisições simultâneas.
