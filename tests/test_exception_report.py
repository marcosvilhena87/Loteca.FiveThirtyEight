from loteca_fivethirtyeight.exception_report import summarize

def test_aliases_and_scope_priority():
    rows=[dict(categoria_excecao="alias_ausente",data_loteca="24/03/2002",
               motivo="alias nao cadastrado: INTERNACIONAL/RS, JOINVILLE/SC"),
          dict(categoria_excecao="alias_ausente",data_loteca="24/08/2002",
               motivo="alias nao cadastrado: JOINVILLE/SC")]
    src=[dict(date="2002-02-01"),dict(date="2002-05-12")]
    annotated,summary=summarize(rows,src)
    assert summary["aliases"]["JOINVILLE/SC"]==2
    assert annotated[0]["prioridade"]=="alta"
    assert annotated[1]["prioridade"]=="baixa_escopo"
    assert summary["motivos"]["alias_ausente"]==2

def test_no_sources_safe():
    annotated,summary=summarize([dict(categoria_excecao="revisao_humana",data_loteca="")],[])
    assert annotated[0]["prioridade"]=="revisao"
    assert summary["periodo_coberto"]==[None,None]
