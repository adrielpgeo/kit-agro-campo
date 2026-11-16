from docx import Document

from kitagro import relatorio


def test_gera_e_reabre_docx(tmp_path):
    caminho = relatorio.gerar_relatorio(
        tmp_path / "r.docx",
        titulo="Título de Teste",
        area="Fazenda X",
        notebook="00 Hello",
        versao="0.0.1",
        produtor="Fulano",
        municipio="Goiânia",
        uf="GO",
        secoes=[("Objetivo", "Corpo da seção.")],
        texto_ia="Texto técnico da IA.",
        fontes=["Fonte A"],
    )
    assert caminho.exists()

    doc = Document(str(caminho))
    textos = "\n".join(p.text for p in doc.paragraphs)
    assert "Título de Teste" in textos
    assert "Fazenda X" in textos
    assert "Goiânia / GO" in textos
    assert "Fontes e limitações" in textos
    assert relatorio.AVISO_IA in textos
    assert relatorio.DISCLAIMER in textos


def test_campos_opcionais_omitidos(tmp_path):
    caminho = relatorio.gerar_relatorio(
        tmp_path / "r.docx",
        titulo="T",
        area="A",
        notebook="00 Hello",
        versao="0.0.1",
    )
    doc = Document(str(caminho))
    textos = "\n".join(p.text for p in doc.paragraphs)
    assert "Produtor:" not in textos  # produtor não informado → não aparece
    assert "Fontes e limitações" in textos
