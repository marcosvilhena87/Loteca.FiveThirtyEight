# Auditoria externa das equipes da Loteca

## Escopo
A auditoria verifica **se cada lado utilizou o time principal**, não apenas se o clube ou o resultado existiu. Fonte de dados: `marcosvilhena87/Loteca/dados` (CSV Caixa). Processar concursos em ordem crescente; 14 jogos por concurso, dois lados por jogo.

## Regras de decisão
- **P**: profissional principal; mudanças táticas e substituições pontuais não convertem automaticamente em reserva.
- **M**: equipe mista, documentada como combinação relevante de titulares e reservas.
- **R**: equipe majoritariamente de reservas profissionais.
- **S23**: sub-23; **S20**: sub-20; **O**: outra formação identificada.
- **I**: indeterminada. É a classificação obrigatória na ausência de evidência suficiente.
- **alto**: escalação completa e comparação sazonal/documentação explícita; **medio**: reportagem ou ficha com sinais claros mas evidência incompleta; **pendente**: não comprovado.

Uma ficha técnica que confirma o placar não comprova automaticamente que a equipe era principal. Para distinguir P/M/R quando há rotações, comparar 11 iniciais com partidas anteriores e posteriores e notícias de desfalques. Nunca usar identidade do clube ou competição como prova isolada. Confrontar datas e fontes: possíveis divergências históricas devem ser registradas, não sobrescritas silenciosamente.

## Rastreabilidade
Cada linha do CSV `concursos/0001.csv` tem decisão **por lado**, evidência textual, URL e status. O registro inicial não declara pesquisa concluída para os códigos I. Preservar sempre o dado bruto, registrar mudanças em commits e acrescentar outras URLs em um arquivo de evidências por jogo se necessário. Confirmar posteriormente a identidade de Etti Jundiaí, Portuguesa e Athletico-PR como aliases históricos sem confundir clubes distintos.

## Estado da execução
Concurso 0001: 14 jogos registrados, com 28 decisões por equipe. Primeira triagem externa realizada; auditoria fina dos 11 titulares ainda incompleta na maior parte dos jogos. **Nenhum código I deve ser utilizado como P na modelagem.**

## Fontes complementares para conferência
- Concurso e placares publicados na época: https://www.folhadelondrina.com.br/opiniao/loterias-382982.html
- Flamengo x São Paulo, escalações e substituições: https://www1.folha.uol.com.br/folha/esporte/ult92u34823.shtml
- Grêmio x Joinville, ficha completa: https://www.gremiopedia.com/wiki/Ficha_T%C3%A9cnica:Gr%C3%AAmio_1_x_1_Joinville_-_16/02/2002
- Fluminense x Etti: https://www.rsssfbrasil.com/miscellaneous/Flu_2001_2006.htm

## Próxima revisão
Completar composição de Americano, Santos, São Caetano, Portuguesa, Corinthians, Cruzeiro, América-MG, Juventude, Atlético-MG, Coritiba, Figueirense, Criciúma, Athletico-PR, Bahia, Santa Cruz, Náutico, Vitória, Bangu, Etti Jundiaí, Ponte Preta e Botafogo; reavaliar equipes com classificação preliminar à luz de listas de titulares usuais.
