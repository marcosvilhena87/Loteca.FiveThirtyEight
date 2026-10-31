# Loteca.FiveThirtyEight

Projeto aberto em Python para previsões probabilísticas de partidas de futebol (1X2) e avaliação de estratégias para a Loteca.

> **Estado:** estrutura inicial. Nenhum modelo foi calibrado nem validado em dados históricos. Previsões não garantem premiação.

## Estrutura

```text
src/loteca_fivethirtyeight/  # biblioteca Python
tests/                      # testes automatizados
data/                       # dados locais (CSV grandes não versionados)
requirements.txt            # dependências
pyproject.toml              # configuração do pacote e pytest
.gitignore                  # exclusões do Git
```

## Instalação

Requer Python 3.10 ou superior.

```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell:
# .venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Executar os testes

```bash
python -m pytest
```

## Exemplo

```python
from loteca_fivethirtyeight import normalize_1x2, multiclass_brier

probabilidades = normalize_1x2(0.50, 0.30, 0.20)
print(probabilidades)          # (0.5, 0.3, 0.2)
print(multiclass_brier(probabilidades, 0))  # resultado 0 = mandante, 1 = empate, 2 = visitante
```

## Próximas etapas

1. Definir esquema de dados (concursos, confrontos, datas e resultados).
2. Implementar baseline histórico e Elo com validação temporal sem vazamento de informação.
3. Calibrar probabilidades 1X2 e medir Brier score, log loss e calibração.
4. Simular concursos por Monte Carlo com sementes reproduzíveis.
5. Otimizar cartões com restrições configuráveis para secos e duplos.

## Notas

O nome homenageia a abordagem de previsão estatística do FiveThirtyEight; este é um projeto independente e não afiliado à marca.


## Importação dos dados históricos

O importador pode buscar diretamente os 13 CSVs públicos de [Loteca/dados](https://github.com/marcosvilhena87/Loteca/tree/main/dados). Nenhum arquivo histórico é copiado para este repositório.

```bash
python -m loteca_fivethirtyeight.importer
# ou com os CSVs armazenados localmente:
python -m loteca_fivethirtyeight.importer --local-dir /caminho/para/dados
```

Os resultados são salvos em `data/loteca_normalizada.csv` e as estatísticas da importação em `data/relatorio_importacao.json`, ambos ignorados pelo Git. Veja [a documentação de importação](docs/IMPORTACAO.md) para regras de normalização, validação de datas, placares e duplicidades.
