# Cobertura integral da auditoria (13 CSVs)

Execute `python -m loteca_fivethirtyeight.coverage --output reports/cobertura_integral.csv`.
O comando baixa os CSVs originais de `Loteca/dados`, registra **todas as linhas** com
chave, data, nomes, placar e origem; gera também resumo JSON. Requer rede e acesso ao
repositório original. Inicialmente, sem arquivo de revisões, tudo é `pendente`.

Estados: `confirmado` = fonte externa examinada e competição/categoria comprovadas;
`rejeitado` = evidência comprova inadequação para o modelo principal;
`pendente` = não há provas suficientes. Nenhum desses estados libera Elo por si só.

Para acrescentar revisão humana, forneça `--reviews caminho/revisoes.csv`
com `concurso;jogo;estado;competicao;categoria;fonte_oficial;status_placar;revisor;justificativa`.
A URL deve apontar para documento específico, e o revisor deve confirmar o teor
do documento, não somente o título/snippet. Não preencher confirmações em massa por
heurística, falta de termos 'sub-20' ou semelhança de nome. Atualização incremental,
preservando a origem. Não há validação automática da autenticidade das URLs.

O arquivo do Elo é gerado exclusivamente pelo módulo `elo_gate` após revisão
explícita, identidade canônica validada e resolução dos conflitos.
