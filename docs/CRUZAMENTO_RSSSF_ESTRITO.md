# Cruzamento estrito com fontes RSSSF

O módulo `rsssf_match.py` cruza o CSV original da Loteca com uma **extração RSSSF revisada**, sem scraping silencioso e sem atribuir competição por heurística.

Formato da extração RSSSF (`;`):
`date;home;away;home_goals;away_goals;competition;source_url`.
Uma linha significa uma partida individual efetivamente identificada na página indicada.
A identidade é baseada em aliases explícitos e auditáveis. Nomes não mapeados
são pendentes (sem fuzzy matching); equipes B ou sub-20 não são confundidas com principais.
Cada partida exige data ISO, mandante, visitante, gols, competição e URL HTTPS.
A partida só fica `confirmado` quando existe **exatamente uma correspondência**
da tupla completa, após resolução de aliases explícitos. Conflitos,
ambiguidades, duplicidades e sorteios ficam `pendente`.

Exemplo:
`python -m loteca_fivethirtyeight.rsssf_match --loteca data/cache_loteca/Loteca_0001-0100.csv --rsssf data/evidencias/rsssf_partidas_extraidas.csv --output reports/cruzamento_rsssf.csv`

Uma confirmação é **histórica de fonte nível B**, não aprovação ao Elo.
`elo_liberado` permanece `nao`. O gate de treinamento precisa ser adaptado
e revisado antes da liberação. A rotina não baixa nem extrai HTML automaticamente:
a origem precisa estar verificável, pois o formato RSSSF não é padronizado.
