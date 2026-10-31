# Cadastro histórico e cruzamento oficial por temporada

Inventário real: 17.836 registros e 1.118 grafias distintas de equipes extraídas dos 13 CSVs originais. O arquivo data/aliases/nomes_observados.csv lista cada grafia e frequência, em status pendente_validacao_historica. **Não se trata de 1.118 identidades de clubes certificadas.** O resolver identity.py trabalha com aliases pontuais e não executa fusões aproximadas de nomes.

## Tabelas oficiais

Coloque exports CSV (UTF-8; delimitador ponto e vírgula), um por temporada/competição, em data/official_fixtures/. Colunas obrigatórias:

temporada;data_iso;mandante_id;visitante_id;gols_mandante;gols_visitante;competicao;categoria;fonte_tabela_url;fonte_sumula_url

Exemplos de categorias: principal masculino, sub20 masculino, feminino, reserva. A origem deve ser URL HTTPS da federação/confederação. O projeto **não fabrica tabelas ou súmulas oficiais**, e não presume que uma URL representa uma súmula válida.

Executar:

    python -m loteca_fivethirtyeight.official_fixtures --output reports/conferencia_oficial

Saídas:
- conferencia_tabelas.csv: cada partida da Loteca com status de cruzamento.
- fila_sumulas_ausentes.csv: casos sem documento individual localizado ou sem correspondência oficial.
- fila_sumulas_nao_verificadas.csv: há link declarado, mas ainda não foi inspecionado.
- fila_divergencias.csv: placares divergentes, aliases pendentes, datas vazias ou ambiguidades.
- aliases_por_partida.csv: IDs e categorias provisórias por confronto.
- resumo_tabelas.json: totais auditáveis.

## Política de segurança

Todos os jogos têm elegivel_elo=nao; mesmo uma tabela coincidente ainda exige verificar a fonte e a natureza oficial de cada jogo. O inventário de aliases contém rótulos ainda não normalizados, inclusive nomes que não fornecem UF. A atualização histórica deve ser feita com fonte, temporada e decisões revisáveis.

Sem exports oficiais carregados, a execução gera fila de pendências, **não** afirma que partidas foram verificadas contra tabelas reais.

Fontes recomendadas: CBF (https://www.cbf.com.br), federações estaduais, CONMEBOL (https://www.conmebol.com) e federações estrangeiras. Preferir tabelas originais e súmulas, anotando URLs permanentes e data de consulta.
