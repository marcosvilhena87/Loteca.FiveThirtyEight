# Execução internacional RSSSF e cruzamento de identidades — 31/10/2026

## Resultado real da última execução
Run: https://github.com/marcosvilhena87/Loteca.FiveThirtyEight/actions/runs/41234163786

- **La Liga 2024/25:** 380 partidas extraídas; `PARSED_NEEDS_REVIEW`. Contagem correta por torneio, mas os confrontos individuais e os aliases requerem auditoria.
- **Serie A italiana 2024/25:** 380 partidas; `PARSED_NEEDS_REVIEW`. Mesma ressalva.
- **Premier League 2024/25:** apenas 362 partidas com parser restrito por rodada; `COUNT_MISMATCH_QUARANTINE`. **Não** certificada. Investigar jogos reagendados, partidas fora do cabeçalho original e limites do extrator.
- **Mundial de Clubes 2025:** 50 linhas; `PARSED_NEEDS_REVIEW`. Não certificada.
- **Libertadores 2025:** arquivo https://www.rsssf.org/sacups/copalibarg.html contém histórico de clubes argentinos, inclusive jogos de 2025, mas **não** é uma tabela anual completa. Está marcado `PARTIAL_ARCHIVE_NOT_ANNUAL`, excluído do parser principal. Tentativa de URL `sacups/copa2025.html` retornou HTTP 404; não inventar alternativa.

## Cruzamento Caixa × RSSSF
O workflow produziu **2 candidatos de revisão contextual** com ambas as identidades candidatas, competição, data exata, mandante/visitante e placar idênticos. Não publica um dataset Elo nem aprova identidades automaticamente. Os demais confrontos não obtiveram dupla correspondência no catálogo limitado de aliases.

As propostas são exportadas no artefato `international-rsssf-evidence` como `international_review.csv`, junto com `international_matches.csv` e `international_source_audit.csv`.

## Regras preventivas
- Um `club_id` dentro de `competition_scoped_aliases.csv` é específico do torneio e continua marcado como `SOURCE_REVIEW_PENDING`; não equivale a homônimo validado por documento histórico.
- `Barcelona` da La Liga não implica que `Barcelona` da Libertadores seja o mesmo clube.
- Enquanto houver `COUNT_MISMATCH_QUARANTINE`, todas as correspondências daquela fonte devem permanecer em revisão; não usar no Elo.
- Dados de clubes principal, feminino e Sub-20 nunca devem ser fundidos automaticamente.
- Validação por contagem 380 é requisito necessário, mas não suficiente.

## Código
- `src/loteca_fivethirtyeight/international_rsssf.py`: extração por rodada e prova de contagem.
- `src/loteca_fivethirtyeight/international_crosscheck.py`: identifica *ambos* os clubes com aliases de competição, e exige mesma data, placar e sentido mandante/visitante.
- `auditoria/rsssf/competition_scoped_aliases.csv`: início do registro internacional sem promoção automática.
- `.github/workflows/rsssf-international.yml`: executa validação e exporta a fila.

## Próxima correção
Adaptar a Premier League para jogos adiados, conferir linha a linha as 380 partidas da Espanha e Itália (incluindo adversários e datas), e construir um inventário da Libertadores 2025 por fontes de competições oficiais ou RSSSF verificadas. Não considerar concluída a validação internacional de todos os adversários.
