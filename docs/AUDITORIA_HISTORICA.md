# Auditoria de dados históricos — 31/10/2026

Fonte: [Loteca/dados](https://github.com/marcosvilhena87/Loteca/tree/main/dados), branch `main`.

## Inspeção real dos 13 CSVs

| Indicador | Resultado |
|---|---:|
| Arquivos lidos | 13 |
| Linhas de partidas | 17.836 |
| Concursos distintos | 1.274 (1 a 1274) |
| Partidas por concurso | 14 em todos os 1.274 |
| Duplicatas `(concurso, jogo)` | 0 |
| Divergências entre resultado 1X2 e placar | 0 |
| Linhas com quantidade de colunas diferente de 11 | 0 |
| Grafias originais de equipe | 1.118 |
| Identificadores após remoção de acentos/pontuação/espaços | 1.111 |
| `sorteio = SIM` | 92 |
| `sorteio = Não` | 12.916 |
| `sorteio = Não Demonstrado` | 4.828 |

**Importante:** os números acima vieram da leitura dos arquivos reais, e não apenas da execução de fixtures de testes. Não constituem verificação independente da autenticidade dos dados. O arquivo `Loteca_1201-1300.csv` termina no concurso 1274, portanto não se deve inferir cobertura até 1300.

## Grupos de variações textuais

Os seguintes sete grupos se unem com normalização mecânica, sem inferir equivalência entre equipes distintas:

- `SAO  CAETANO/SP` / `SAO CAETANO/SP`
- `P. DESPORTOS/SP` / `P.  DESPORTOS/SP`
- `JI PARANA` / `JI-PARANA`
- `LETÔNIA` / `LETONIA`
- `UNIAO S.JOAO/SP` / `UNIAO S JOAO/SP`
- `NOVA VENECIA/ES` / `NOVA VENÉCIA/ES`
- `PALMEIRAS B/SP` / `PALMEIRAS-B/SP`

**Pendente de curadoria:** abreviações como `S. PAULO/SP` versus `SAO PAULO/SP`, denominações históricas, clubes homônimos de diferentes estados, equipes B e seleções. Não mesclar esses grupos por distância de edição. O arquivo de auditoria lista grafias que merecem revisão.

## Reprodução

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
python -m pytest
python -m loteca_fivethirtyeight.audit
# ou com download imutável dos 13 arquivos:
python -m loteca_fivethirtyeight.audit --local-dir /caminho/para/dados
```

Saída: `data/auditoria_historica.json` (ignorada pelo Git). O comando detecta interrupções de concursos, chaves repetidas, jogos ausentes e datas invertidas. Não aplica fusões baseadas em semelhança de nomes.

## Portões antes do Elo

1. Curar aliases não triviais com lista explícita versionada e evidências de identidade.
2. Excluir ou modelar em categoria separada os 92 resultados indicados como sorteio.
3. Congelar snapshot de origem com SHA dos 13 arquivos e validar cronologia, incluindo possibilidade de dados corrigidos posteriormente.
4. Definir divisão temporal treino/teste e teste de ausência de vazamento.

Nenhum Elo ou backtest foi iniciado nesta etapa.
