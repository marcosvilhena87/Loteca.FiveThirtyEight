# Validação de fontes e IDs canônicos — 31/10/2026

## O que está automatizado
- Gerador de 200 candidatas (8 famílias × 25 anos) obtidas de anos observados nos 13 CSVs.
- Validação HTTP concorrente de até 200 URLs, registrando `URL_REACHABLE_UNREVIEWED`, `URL_UNAVAILABLE_OR_ERROR` ou `CANDIDATE_NOT_VERIFIED`.
- Um HTTP 200 **não valida** competição, resultados nem classificação principal. URLs verificadas não entram automaticamente no manifesto de fontes RSSSF.
- Registro inicial `club_registry.csv` contendo `club_id`, `country`, `region`, alias, `since`, `until`.
- Resolvedor `club_identity.resolve`: aliases correspondem somente dentro do período histórico; nome sem região ambíguo retorna `None`; região conflitante impede identidade.
- Testes adicionais para aliases, nomes homônimos e validade temporal.
- A integração dos IDs canônicos ao matcher geral ainda exige aumentar o registro; **o matcher atual permanece com filtros conservadores anteriores**.

## Limitações
As oito famílias iniciais não são um mapa completo dos campeonatos efetivamente disputados pela Loteca. Os padrões de URL podem ser inexistentes e devem ser descobertos/confirmados, não inferidos. UF é metadado de identidade, não parte do nome; clubes sem UF e internacionais precisam de registro manual/país/competição. O intervalo 1900–2100 em aliases estáveis é um valor inicial convencional e **não comprova fundação ou continuidade institucional**. Mudanças de identidade (cisão, fusão, renomeação) precisam de referências históricas antes de serem aprovadas.

## Critério de promoção de fonte
(1) URL acessível; (2) nome da competição/ano/categoria conferidos; (3) parser produz linhas corretas em amostra representativa; (4) confrontos confirmados por ID canônico e placar; (5) datas e diferenças de formatos verificadas; (6) aprovação manual/documentada. Somente então incluir URL no manifesto operacional.

## Evidência
Workflow: https://github.com/marcosvilhena87/Loteca.FiveThirtyEight/actions/runs/41231839086
Arquivos gerados no artefato `rsssf-audit-evidence` (se o workflow terminar com sucesso). A execução anterior tinha 1.000 correspondências candidatas/17.836 jogos e não é contagem de validação manual.
