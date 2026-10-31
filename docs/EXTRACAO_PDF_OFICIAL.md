# Extrator de documentos PDF oficiais

Extrai camada de texto com PyMuPDF por página. Para cada página, preserva URL ou URI local, SHA-256 do PDF, número de página, candidato de mandante/visitante/placar, categoria textual, identificador e data quando inequívocos.

Instalação:

    pip install -e . pytest

Execução para PDF local:

    python -m loteca_fivethirtyeight.pdf_evidence --pdf documento.pdf --organizadora fpf --temporada 2018 --competicao Copinha --output reports/extracao_pdf

Execução para URL oficial:

    python -m loteca_fivethirtyeight.pdf_evidence --url https://www.cbf.com.br/documento.pdf --organizadora cbf --temporada 2025 --competicao Serie_A

A coleta remota só aceita HTTPS de domínios oficiais cadastrados. Limites: 20 MB e 300 páginas. A saída separa extracao_documental.csv, candidatos_confronto.csv, fila_revisao_pdf.csv e resumo_pdf.json.

## Limites importantes

- O extrator usa **heurística textual**, não reconhece automaticamente a configuração de tabelas, linhas, mandos, clubes ou placares em todos os modelos de PDF.
- PDF digitalizado sem texto vai à fila de revisão; OCR não é aplicado automaticamente.
- Uma página com vários confrontos vai à fila de revisão para evitar pareamento errado.
- A detecção de categoria, data e ID de partida só usa menções inequívocas; ausência de detecção não é confirmação de principal.
- URL, PDF e texto extraído **não equivalem à certificação de súmula**. Uma revisão por confronto precisa verificar conteúdo, organizadora, categoria, data, placar, aliases e documento.
- **Nenhuma partida é liberada ao Elo** nesta etapa.
- Próxima integração: regras específicas para layouts oficiais de FPF, CBF e CONMEBOL, importação de tabelas reais e correspondência temporal com Loteca.
