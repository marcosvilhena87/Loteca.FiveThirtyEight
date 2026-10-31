# Índice RSSSF por temporada — execução de 31/10/2026

## Execução validada
GitHub Actions: https://github.com/marcosvilhena87/Loteca.FiveThirtyEight/actions/runs/41231381110 (sucesso).
- 10 testes pytest aprovados.
- 17.836 registros originais processados.
- 200 URLs candidatas geradas (8 famílias de competições × 25 temporadas, 2002–2026). **Nenhuma das 200 URLs é considerada verificada só pela geração de um padrão**.
- 11 URLs explícitas em manifesto de fontes já catalogadas, incluindo Série A 2010 e 2018.
- 3.142 linhas de placar extraídas das URLs do manifesto.
- 1.000 correspondências automáticas candidatas, equivalentes a **5,61%** de 17.836; 16.835 pendentes; 1 pendência de revisão de data.
- Comparação anterior: 961 candidatos; incremento líquido de +39 candidatos ao adicionar a fonte de 2010.

## Interpretação, qualidade e escopo
`CONFIRMADO_PRINCIPAL` no resultado.csv significa **candidato de alta especificidade algorítmica** (confronto, gols e data), não revisão documental individual nem validação do elenco efetivo. As 200 fontes candidatas `CANDIDATE_NOT_VERIFIED` permanecem isoladas: não são extraídas ou usadas pelo matcher. Testar URLs em lote requer verificação independente do tipo de competição, categoria, formato de resultados e identificação de clubes.

O algoritmo rejeita conflitos explícitos de UF para clubes com o mesmo nome e mantém pendências em casos sem identidade estadual suficiente para homônimos conhecidos. Uma inspeção manual amostral e revisão de aliases continuam obrigatórias antes de liberar qualquer saída para o modelo Elo.

## Próximo ciclo
1. Validar HTTP e formato de cada candidato; não presumir que os padrões de URL são universalmente corretos.
2. Montar cobertura por grupo e ano com a contagem de jogos relevantes da Caixa, não apenas número de fontes.
3. Expandir o registro canônico para clube + UF/país + intervalo histórico de nome, em vez de eliminar UF na chave.
4. Criar relatório de precisão por amostragem estratificada, incluindo exemplos negativos e divergências.
