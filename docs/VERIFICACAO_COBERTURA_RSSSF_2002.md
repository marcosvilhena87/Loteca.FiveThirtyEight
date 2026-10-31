# Verificação de cobertura das páginas RSSSF (31/10/2026)

Links lidos online:
- https://www.rsssf.org/tablesr/riospl02.html
- https://www.rsssf.org/tablesb/brazchampcup02.html

## Totais de referência fundamentados na estrutura das páginas

**Rio–São Paulo 2002**: 16 participantes, 15 rodadas com 8 partidas por rodada = 120 jogos na primeira fase. A mesma página registra semifinais em ida e volta (4 jogos) e finais em ida e volta (2 jogos): 126 partidas esportivas no total. **A versão atual do extrator identifica apenas as rodadas 1–15; os mata-matas estão num formato compacto com dois placares por linha e não devem ser considerados extraídos.** Total esperado do extrator atual: 120, não 126.

**Copa dos Campeões 2002**: 4 grupos de 4 clubes, 6 jogos por grupo = 24, mais quartas (4), semifinais (2), final ida e volta (2): 32 jogos. Total esperado: 32.

Esses totais são **referências apuradas a partir das páginas publicadas, não saídas de um extrator executado**.

## Bloqueios e exigências

- O ambiente de execução local não conseguiu resolver github.com; não foi possível clonar o repositório nem executar o extrator completo localmente.
- Foi adicionado workflow GitHub Actions em .github/workflows/auditoria-rsssf-2002.yml para execução e artefatos. Ao consultar a API do GitHub após o commit, total_count=0 para execuções dessa branch. Portanto, **não declarar testes ou extração como executados**.
- Os arquivos RSSSF não devem ser tratados como evidência de placar aos 90 minutos caso haja informação de prorrogação ou pênaltis.
- Na Copa, a segunda partida da final Cruzeiro 3-4 Paysandu deve armazenar separadamente os pênaltis (Paysandu venceu 3-0).
- Um confronto com alias desconhecido deve permanecer pendente, mesmo quando a data e o placar coincidirem.
- Sem CSV de extração produzido, não existe relatório de exceções real; a lista requer execução.
- Mata-matas do Rio–São Paulo exigem implementação específica e cobertura explicitamente testada.
