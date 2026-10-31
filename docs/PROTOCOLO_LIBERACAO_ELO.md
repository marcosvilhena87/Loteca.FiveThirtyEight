# Protocolo de liberação do Elo — fechado por padrão

Nenhum confronto da Loteca é elegível ao Elo por mera presença em CSV, alias parecido,
resultado de pesquisa, link de consulta, classificação nominal ou confiança alta.

## Registro e etapas

1. Preservar CSV original e identificar concurso+jogo.
2. Conferir equipes canônicas com UF e categoria (principal, B, base, feminino).
3. Identificar competição, temporada, data, mando e placar esportivo.
4. Abrir fonte oficial (CBF, federação, confederação, súmula ou página oficial).
5. Guardar URL específica, tipo de documento, observações e conflitos.
6. Registrar aprovação humana **explícita**, jamais inferida por um coletor.
7. Exportar somente após passar `elo_gate.assess`.

O arquivo de evidências não é substituído: permanece a trilha histórica.
`python -c "from loteca_fivethirtyeight.elo_gate import export_approved; print(export_approved('data/evidencias/competicoes_verificadas.csv','data/approved/elo_matches.csv'))"`

Para liberar: categoria=oficial_profissional; decisao_elo=liberar;
tipo_evidencia_oficial=sumula_oficial, tabela_oficial_resultado ou pagina_oficial_partida;
status_placar=oficial_confirmado ou sumula_confirmada; URL HTTPS oficial; competição,
data, identidades e observações preenchidas. Revisar divergências manualmente.
Na ausência de evidência, `bloquear`. Jogos de base e reservas ficam excluídos;
amistosos profissionais vão para base separada.

**Nota:** o código valida campos e consistência formal, não autentica se a URL
efetivamente comprova o confronto. Essa verificação exige abertura e revisão
da fonte. Nunca preencher status aprovado automaticamente com base em snippets.
