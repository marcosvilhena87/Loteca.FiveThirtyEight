# Importação do histórico

Origem: [marcosvilhena87/Loteca/dados](https://github.com/marcosvilhena87/Loteca/tree/main/dados).

## Executar

Depois de instalar o pacote (`python -m pip install -e .`):

```bash
python -m loteca_fivethirtyeight.importer
# Alternativamente, com os 13 CSVs salvos localmente:
python -m loteca_fivethirtyeight.importer --local-dir /caminho/para/dados
python -m pytest
```

A importação remota busca os 13 arquivos `Loteca_0001-0100.csv` a `Loteca_1201-1300.csv` da branch `main` do repositório de origem, a cada execução. Para reproduzir um conjunto de dados histórico imutável, faça download de um commit fixo ou utilize `--local-dir` e registre o hash dos arquivos.

Arquivos gerados (ignorados pelo Git): `data/loteca_normalizada.csv` e `data/relatorio_importacao.json`.

## Validação

- O separador é ponto e vírgula, com 11 colunas obrigatórias, na ordem original.
- Datas brasileiras são convertidas para ISO 8601 (AAAA-MM-DD); datas impossíveis são rejeitadas.
- Gols são inteiros não negativos; resultado deve ser `1`, `X` ou `2` e deve concordar com o placar.
- Índices `concurso` e `jogo` são inteiros positivos; `jogo` está limitado a 1–14.
- A chave de deduplicação é `(concurso, jogo)`. Duplicatas idênticas são removidas; conflitantes causam erro.
- O identificador do clube é uma limpeza textual (acentos, caixa, pontuação, espaços). **Não é uma tabela de aliases**: `S. PAULO/SP` e `SAO PAULO/SP` permanecem IDs distintos até uma etapa explícita de reconciliação.
- `sorteio` é preservado e acompanhado de um sinalizador `sorteio_indicado`. Valores `Não` e `Não Demonstrado` não são tratados como `Sim`; outras classificações não vazias ficam sinalizadas para revisão.
- Concursos com menos de 14 jogos são reportados, não preenchidos artificialmente.

O importador é **fail-fast**: interrompe ao encontrar linhas inválidas em vez de descartá-las. Ausência de arquivo ou falha de rede também interrompe o processo. O relatório não deve ser interpretado como auditoria completa de cobertura de concursos ausentes nem como validação da autenticidade dos resultados.
