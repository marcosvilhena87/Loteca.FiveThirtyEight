# Evidências internacionais — rodada de cruzamento com a Caixa (31/10/2026)

## Partidas encontradas em tabelas RSSSF da temporada 2024/25
- Concurso 1187 jogo 1: Barcelona 4–3 Real Madrid em 11/05/2025, na página https://rsssf.org/tabless/span2025.html (Round 35, May 11).
- Concurso 1191 jogo 7: Liverpool 1–1 Crystal Palace em 25/05/2025, na página https://rsssf.org/tablese/eng2025.html (Round 38, May 25).

As duas partidas foram conferidas quanto a mandante, visitante, resultado, data e competição, e incluídas em `internacionais_revisao_documental.csv`. A identidade institucional é uma **proposta**: o arquivo não altera `club_registry.csv` nem fornece uma licença para atualizar o Elo.

## Estratégia operacional
- O índice RSSSF internacional precisa incluir fontes por **temporada encerrada**, pois a temporada 2024/25 usa o índice 2025. Não assumir que o ano da partida é o ano inicial da temporada.
- `BARCELONA` sem país não deve ser resolvido globalmente: há também Barcelona SC do Equador, evidenciado por jogos da própria Caixa contra adversários da Libertadores.
- Para avançar uma partida da fila, exigir identificação da competição, fonte RSSSF específica, data real, placar exato, adversário e orientação de mandante/visitante. Para uma identidade institucional, o contexto geográfico do campeonato é essencial.
- Manter categorias (principal, base, feminino) separadas e assinalar divergências de horário/datas e fontes que não permitem identificar a equipe.
- `CANDIDATO_CONTEXTO_REVISAR` e `REVISAO_DOCUMENTAL` não equivalem à certificação humana final.
- Os 278 jogos com pelo menos um dos aliases Barcelona, Juventus, Liverpool ou Milan foram localizados nos snapshots da Caixa; **não são 278 partidas confirmadas na RSSSF**.

## Próxima ampliação de catálogo
Registrar fontes RSSSF de primeira divisão de Espanha, Inglaterra e Itália, além de Libertadores e Mundial de Clubes, com validação de parser e normalização de apelidos antes de disponibilizar seus resultados ao matcher.
