# Resolução contextual de identidades — rodada experimental (31/10/2026)

## Implementado

O novo módulo `contextual_identity.py` examina cada jogo da Caixa e exige simultaneamente:
1. **Data exata** de jogo na Caixa e na referência externa (sem data vazia);
2. **Placar exato**, com mandante/visitante preservados;
3. **Adversário previamente identificado** por ID único no cadastro canônico;
4. **Nome-base concordante** para o clube ainda não resolvido;
5. **Competição, categoria principal, URL e linha** da referência RSSSF presentes;
6. **Um só ID candidato** entre os resultados elegíveis.

Caso as condições se cumpram, o registro é emitido em `contextual_identity_review.csv` como `CANDIDATO_CONTEXTO_REVISAR`, **nunca como confirmação**. Se faltar evidência ou houver múltiplas identidades, permanece `QUARENTENA` ou `AMBIGUO_CONTEXTO`. O cadastro principal nunca é alterado por essa função.

## Limites
- Este algoritmo cria propostas de revisão; **não comprova automaticamente a identidade do clube** só por uma linha de placar.
- A hipótese de partida exclusiva ainda deve ser verificada em fontes independentes.
- O manifesto atual tem apenas fontes brasileiras. Assim, não é possível declarar resolvidos Barcelona, Juventus, Liverpool ou Milan sem anexar competições internacionais RSSSF com evidência.
- Fonte de competição e categoria é declarada no manifesto; a classificação documental continua condicionada à revisão.
- Por segurança, não há preenchimento automático de club_id e nem entrada em dataset Elo.
- Em circunstâncias com múltiplos jogos do mesmo confronto/placar/data ou sede neutra, exige-se revisão adicional.

## Evidências
- Código: `src/loteca_fivethirtyeight/contextual_identity.py`
- Testes: `tests/test_contextual_identity.py`
- Workflow: `.github/workflows/rsssf-audit.yml` (inclui exportação `contextual_identity_review.csv`)
- Execução atual: https://github.com/marcosvilhena87/Loteca.FiveThirtyEight/actions/runs/41233285882

**Apenas resultados do workflow concluído podem estabelecer contagens efetivas**. Nenhuma taxa de cobertura melhorada é alegada nesta etapa.
