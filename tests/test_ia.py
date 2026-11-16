from kitagro import ia


def test_resumo_area_contem_nome_e_area():
    texto = ia.gerar_texto("resumo_area", {"nome_area": "Talhão 1", "area_ha": 10.0})
    assert "Talhão 1" in texto
    assert "10,00 ha" in texto


def test_resumo_area_com_produtor():
    texto = ia.gerar_texto("resumo_area", {"nome_area": "Sítio X", "produtor": "José"})
    assert "José" in texto


def test_tipo_desconhecido_usa_generico():
    texto = ia.gerar_texto("inexistente", {"x": 1})
    assert texto.strip()


def test_sem_dados_nao_quebra():
    assert ia.gerar_texto("resumo_area", {}).strip()
    assert ia.gerar_texto("inexistente", {}).strip()
