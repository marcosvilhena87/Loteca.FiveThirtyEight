# Triagem integral dos aliases da Loteca — 31/10/2026

## Escopo e resultados
- Foram analisados os 13 arquivos de snapshot da Caixa (17.836 jogos, 35.672 aparições de equipes), sem editar as fontes.
- Na triagem original pelo cadastro anterior, **25.715 aparições** tinham ID encontrado, e **9.957 aparições** não tinham ID, em **4.117 combinações de nome original + ano**.
- Após acrescentar 9 registros de aliases com pesquisa documental, **42 combinações/ano**, cobrindo **419 aparições**, passaram a resolver um único ID no cadastro.
- **4.075 combinações/ano**, totalizando **9.538 aparições**, seguem em quarentena. Portanto não é correto afirmar que todos os nomes foram resolvidos.
- O status `RESOLVIDO_DOCUMENTADO` no CSV de triagem significa **resolução mecânica única pelo registro cadastrado**: exige revisão das datas de validade e da categoria para a certificação histórica.
- Cobertura cadastral projetada após a triagem: 26.134 / 35.672 aparições (**73,26%**); não confundir com cobertura RSSSF validada nem com liberação para Elo.

## Evidências e decisões institucionais
- Grêmio Barueri foi renomeado Grêmio Prudente em 2010 e retornou a Barueri em 2011; **o Sport Club Barueri e outras agremiações de Barueri permanecem IDs separados**. Federação Paulista: https://futebolpaulista.com.br/Noticias/Detalhe.aspx?Noticia=15175; cobertura da mudança: https://ge.globo.com/futebol/times/gremio-prudente/noticia/2011/05/gremio-prudente-volta-para-barueri.html
- O estatuto do Sampaio Corrêa (MA) registra nome institucional e sede. As abreviações `SAMP CORREA/MA` e `SAMPAIO CORREA/MA` receberam o mesmo ID. https://www.sampaiocorreafc.com.br/wp-content/uploads/2023/11/1.-Estatuto-de-Sampaio-Correa-2023-Registrado.pdf
- Ipatinga FC iniciou transferência de sede e nome para Betim no fim de 2012; a mesma chave institucional para IPATINGA até 2012 e BETIM ESPORTE em 2013 requer verificação de datas exatas de jogos na transição. https://ge.globo.com/mg/grande-minas-vales/futebol/times/ipatinga/noticia/2012/11/mais-um-time-itinerante-no-brasil-ipatinga-esta-de-mudanca-para-betim.html
- `RB BRAGANTINO/SP` foi associado ao mesmo ID cadastrado de Red Bull Bragantino; RB Brasil permanece distinto.
- Aliases com nomes de equipes de base, clubes homônimos ou estados não demonstrados **não foram convertidos automaticamente em identidades profissionais**.

## Entregáveis
- `aliases_revisao_manual_consolidado.csv` — lista inicial completa, antes destas 9 entradas.
- `aliases_triagem_completa.csv` — classificação posterior de todas as 4.117 combinações da fila.
- `aliases_quarentena.csv` — 4.075 entradas que ainda carecem de evidência suficiente.
- `club_registry.csv` — registro canônico atualizado.

## Método e limitação
A triagem usa alias normalizado + UF explícita + ano dentro do intervalo registrado. Não usa fuzzy matching para promover desconhecidos. As datas iniciais de alguns aliases são janelas operacionais e não comprovação do ano exato da denominação. Para os 9.538 usos remanescentes, é necessário ampliar pesquisa de identidades com fontes oficiais, federações, RSSSF e documentação histórica. Nenhuma porcentagem de confirmação RSSSF ou precisão do Elo foi inferida deste levantamento.
