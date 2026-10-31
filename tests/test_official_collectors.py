from loteca_fivethirtyeight.official_collectors import allowed, classify_link, LinkParser, write

def test_whitelist_blocks_lookalikes():
    assert allowed("https://www.cbf.com.br/futebol-brasileiro", "cbf")
    assert not allowed("https://cbf.com.br.evil.test/x", "cbf")
    assert not allowed("http://www.cbf.com.br/x", "cbf")
    assert not allowed("https://example.com/", "conmebol")

def test_document_kind():
    assert classify_link("https://cbf.com.br/docs/a.pdf", "Súmula oficial") == "sumula"
    assert classify_link("https://cbf.com.br/docs/a.pdf", "Tabela detalhada") == "tabela"
    assert classify_link("https://cbf.com.br/docs/a.pdf", "Não identificado") == "indeterminado"

def test_html_parser():
    p = LinkParser()
    p.feed('<a href="/doc.pdf">Súmula de jogo</a>')
    assert p.links == [("/doc.pdf", "Súmula de jogo")]

def test_empty_report(tmp_path):
    write(tmp_path, [], [])
    assert (tmp_path / "documentos_oficiais.csv").exists()
    assert (tmp_path / "falhas_coleta.csv").exists()
    assert (tmp_path / "fila_sumulas_documentais.csv").exists()
