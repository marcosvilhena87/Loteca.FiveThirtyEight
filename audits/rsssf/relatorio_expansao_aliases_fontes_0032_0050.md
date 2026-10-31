# Ampliação de aliases e fontes — execução auditável de 31/10/2026

Workflow final: https://github.com/marcosvilhena87/Loteca.FiveThirtyEight/actions/runs/41241609817

Artefatos com HTML, integridade, diagnóstico e candidatos: https://github.com/marcosvilhena87/Loteca.FiveThirtyEight/actions/runs/41241609817/artifacts/13057632052

## Resultados observados
- Cadastro: 37 linhas adicionais de aliases históricos, sujeitos a revisão de identidade e limites temporais.
- Fontes: 8 → 11. Adicionadas Premier League Inglaterra 2002/03, Brasileiro Série C 2002 e Cearense 2003.
- Downloads: 11/11.
- Fonte inglesa: **não homologada**, 683 linhas versus 380 previstas; extrator confundiu divisões. Excluída preventivamente da conciliação e diagnóstico.
- Série C 2002: 188 linhas candidatas; Cearense 2003: 96.
- Dados RSSSF **de fontes com integridade configurada aprovada**: 1931 partidas de campo para confronto.
- Caixa: 266 registros. **223 candidatos únicos para revisão, 40 sem candidato, 3 sorteios bloqueados, zero homologações Elo.**
- Diagnóstico de 40 sem candidato: 38 aliases ausentes ou cobertura insuficiente, 2 casos em competição ausente ou fonte incompleta, categorias heurísticas não comprovadas.
- Ponto de partida antes desta expansão: 192 candidatos únicos e 71 sem candidato. Redução conservadora de **31 pendências** sem usar a fonte inglesa reprovada.

## Bloqueios
1. Resolver a segmentação da Premiership inglesa, exigindo 38 rodadas × 10 partidas, antes de incluir a fonte.
2. `integrity=pass` das competições brasileiras significa apenas aprovação das verificações atualmente configuradas, **não prova de cobertura completa**.
3. Auditar as 40 exceções individualmente, identificar campeonatos restantes, revisar aliases e incompatibilidades de data/placar.
4. Revisar manualmente os 223 candidatos antes de converter qualquer status em partida elegível ao Elo.

A matriz de homologações não foi alterada por estes candidatos. Histórico da Caixa original preservado.
