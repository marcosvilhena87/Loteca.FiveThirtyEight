# Conciliador RSSSF (candidatos, não homologação)

Ferramenta independente para conciliar os 266 registros dos concursos 0032–0050 com linhas RSSSF *já extraídas e revisadas*.

## Entradas
- Caixa: CSV original com campos `concurso;jogo;data_jogo;equipe_1;equipe_2;gols_1;gols_2;sorteio`.
- RSSSF: CSV `date;home;away;home_goals;away_goals;competition;source_url`.
- Aliases temporais: `alias,canonical_id,valid_from,valid_to` (vírgulas). Lista de exemplo **não exaustiva**, deve ser validada.

```bash
python -m audits.rsssf.reconcile_auto --caixa dados_0032_0050.csv --rsssf rsssf_matches.csv --aliases audits/rsssf/aliases_temporais.csv --out candidatos_0032_0050.csv
python -m pytest tests/test_rsssf_reconcile_auto.py
```

O pipeline é conservador: busca ±1 dia, exige placar exato e ordem dos mandos, resolve aliases com período de validade, ordena candidatos e bloqueia sorteios. **Mesmo candidato único não significa confirmado**, e `elo_eligible` fica `nao` até revisão humana. Outros casos sem candidato podem ser divergências reais de data/placar e exigem busca ampliada.

A extração HTML da RSSSF **ainda não está integrada** porque cada tabela possui estrutura própria; o CSV RSSSF precisa ser preparado antes de executar o matcher. Não confundir o arquivo de candidatos com um conjunto auditado para treino.
