# Triagem 3 — clubes internacionais e homônimos (31/10/2026)

A fila original de 4.117 combinações alias/ano foi reprocessada integralmente contra o cadastro revisado.

| Indicador | Resultado |
|---|---:|
| Combinações agora com ID único no cadastro | 447 |
| Aparições agora com ID único (dentro da fila original) | 1.834 |
| Combinações em quarentena | 3.670 |
| Aparições em quarentena | 8.123 |
| Total de aparições de equipe nos 17.836 jogos | 35.672 |
| Cobertura cadastral projetada | 27.549 / 35.672 = 77,23% |

A expressão 'ID único' indica resolução cadastral provisória e não confirmação independente da partida por RSSSF, categoria ou competição. Os números são recálculos sobre a mesma fila original de aliases/ano, não uma medição atual da taxa de matches RSSSF.

Foram acrescentadas oito entradas separando país e estado: Real Madrid (ESP), Manchester United (ENG), Brasil de Pelotas/RS, Ferroviária/SP, Mogi Mirim/SP, River/PI, Salgueiro/PE e São Bernardo/SP. **Barcelona** não foi registrado sem desambiguação por país e competição. Períodos 2002-2026 são janelas operacionais; não representam necessariamente todas as temporadas de atuação.

Fontes institucionais verificadas para as entidades internacionais:
- https://www.realmadrid.com/en-US/the-club/history/football/first-team/
- https://ir.manutd.com/company-information/history.aspx

A correspondência por ID com homônimos no Brasil continua sujeita a validação contextual; a presença de UF na Caixa é condição útil, mas não prova por si só que o resultado RSSSF é da equipe correta.

## Entregáveis
- `aliases_triagem_v3.csv`: fila integral classificada
- `aliases_quarentena_v3.csv`: 3.670 casos pendentes
- `club_registry.csv`: cadastro de IDs atualizado
- `tests/test_club_identity.py`: regressões de países, estados e Barcelona não resolvido

Teste automatizado no GitHub Actions: https://github.com/marcosvilhena87/Loteca.FiveThirtyEight/actions/runs/41232889365

**Não liberar dados ao Elo:** apenas os confrontos com identidades de ambos os lados comprovadas, competição principal e evidência de resultado/data devem ser considerados para certificação.
