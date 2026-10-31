import fitz
import pytest
from loteca_fivethirtyeight.pdf_evidence import read_pdf, safe_pdf, export

def pdf_text(text):
    doc=fitz.open()
    page=doc.new_page()
    if text:
        page.insert_text((60,80),text)
    data=doc.tobytes()
    doc.close()
    return data

def metadata():
    return dict(organizadora="fpf",temporada="2018",competicao="Copinha",
                documento_url="https://futebolpaulista.com.br/exemplo.pdf")

def test_pdf_and_provenance(tmp_path):
    rows=read_pdf(pdf_text("FLUMINENSE 1 x 2 TUBARAO"),metadata())
    assert rows[0]["pagina"]=="1"
    assert len(rows[0]["sha256"])==64
    assert rows[0]["status"]=="candidato_extraido"
    export(rows,tmp_path)
    assert (tmp_path/"candidatos_confronto.csv").exists()

def test_scanned_pdf_goes_to_review():
    assert read_pdf(pdf_text(""),metadata())[0]["status"]=="pagina_sem_texto"

def test_reject_fake_pdf():
    with pytest.raises(ValueError):
        safe_pdf(b"not a pdf")

def test_multiple_games_for_manual_review():
    text="FLUMINENSE 1 x 2 TUBARAO\nPALMEIRAS 3 x 1 SANTOS"
    assert read_pdf(pdf_text(text),metadata())[0]["status"]=="multiplos_confrontos_na_pagina"
