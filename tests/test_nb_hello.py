from docx import Document

from kitagro import nb_hello


def test_executar_gera_relatorio(tmp_path):
    caminho = nb_hello.executar(
        nome_area="Fazenda Teste",
        nome_produtor="Zé",
        base=tmp_path,
    )
    assert caminho.exists()
    assert caminho.name == "relatorio.docx"

    doc = Document(str(caminho))
    textos = "\n".join(p.text for p in doc.paragraphs)
    assert "Fazenda Teste" in textos


def test_executar_nome_vazio_levanta(tmp_path):
    import pytest

    from kitagro import validate

    with pytest.raises(validate.ErroUsuario):
        nb_hello.executar(nome_area="  ", base=tmp_path)
