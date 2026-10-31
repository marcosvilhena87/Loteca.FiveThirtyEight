# Semântica dos resultados

Dados da Loteca são distintos de resultados em campo.
- `lottery_symbol`: resultado 1X2 registrado pela Caixa; em `lottery_draw=True`, não implica placar esportivo.
- `home_90/away_90`: gols após tempo regulamentar, incluindo acréscimos.
- `home_extra/away_extra`: gols **adicionais** marcados na prorrogação (não o total acumulado).
- `home_penalties/away_penalties`: conversões da disputa por pênaltis.
- `result_90`: resultado que pode servir ao modelo 1X2 após passar pela auditoria externa.
- `knockout_winner`: vencedor do confronto considerando prorrogação e, se houve, pênaltis.

`elo_90_eligible` verifica apenas a semântica local; **não aprova evidências nem identidades**.
O treinamento exige também o gate externo de `elo_gate.py`; nenhum destes módulos, por si, pode liberar dados.

Exemplos de 2002:
- Suécia x Senegal: 1-1 em 90 minutos; 1-2 após prorrogação -> extra 0-1.
- Coreia x Itália: 1-1 em 90 minutos; 2-1 após prorrogação -> extra 1-0.
- Espanha x Irlanda: 1-1 aos 90; 1-1 após prorrogação; 3-2 nos pênaltis.
Não transformar decisão na prorrogação em resultado 1X2 dos 90 minutos.
