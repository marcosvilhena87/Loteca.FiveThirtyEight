# Avanço da triagem de aliases — rodada 2 (31/10/2026)

## Escopo e resultados
A fila original de 4.117 combinações alias+ano (9.957 aparições sem ID) foi reprocessada contra o registro expandido.
- **163 combinações** da fila passaram a resolver **um ID único provisório**, correspondentes a **1.113 aparições**.
- **3.954 combinações** (**8.844 aparições**) seguem em quarentena.
- A cobertura cadastral calculada com a base original é **26.828 / 35.672 aparições = 75,21%**. Essa porcentagem é de identidade cadastral, NÃO de confirmação RSSSF nem de partidas aptas ao Elo.
- Esta rodada incorporou 11 aliases/cadastros prioritários e o histórico Ituiutaba→Boa Esporte; manteve grafias internacionais sem país e homônimos em quarentena.
- A triagem da fila é completa, mas a investigação individual de todos os 3.954 restantes não está concluída.

## Evidências documentais
- Tombense/MG, clube de Tombos: https://tombense.com.br/
- Brusque/SC, distinto das agremiações Carlos Renaux e Paysandu que participaram de sua origem: https://brusquefutebolclube.com.br/o-clube/
- Amazonas/AM criado em **2019**, não compartilhar rating com clubes anteriores de Manaus: https://amazonasfc.com.br/site/pagina/historia/
- Icasa/CE: **ADRC Icasa fundada em 2002**, distinta do antigo Icasa EC; proibir mesclar ratings automaticamente: https://www.futebolcearense.com.br/2011/clube.asp?id=43
- Marília/SP: https://www.macoficial.com/o-clube
- Portuguesa de Desportos/SP: https://www.portuguesa.com.br/institui%C3%A7%C3%A3o
- ABC/RN: https://abcfc.com.br/historia/
- Ituiutaba/Boa Esporte: identidade histórica com alteração de nome em 2011: https://boaesporte.com.br/institucional-boa/

## Cautelas
As faixas 2002–2026 em registros recentemente introduzidos são janelas operacionais, **não prova anual de atuação**, e dependem de confronto com competição e elenco para uso no Elo. A entrada do Icasa não autoriza a união da antiga instituição extinta com a associação fundada em 2002. Novos IDs não devem ser considerados certificação por ano sem pesquisa específica. O cadastro canônico resolve identidade nominal, não a classe (profissional, Sub-20, feminino, seleções).

## Entregáveis
- `aliases_triagem_v2.csv`: classificação integral da fila com IDs provisórios.
- `aliases_quarentena_v2.csv`: 3.954 combinações pendentes.
- `club_registry.csv`: identidades e aliases atualizados.

## Próxima etapa
Separar os clubes estrangeiros por país e os homônimos brasileiros por UF/cidade com evidências; adicionar campo de **classe da equipe** antes da certificação Elo. Rever transições, novas entidades e casos com grafia aproximada manualmente.
