import pytest

from kitagro import validate


def test_formatar_numero_padrao_brasileiro():
    assert validate.formatar_numero(1234.5) == "1.234,50"
    assert validate.formatar_numero(0) == "0,00"
    assert validate.formatar_numero(1234567.891, 3) == "1.234.567,891"


def test_formatar_area_ha():
    assert validate.formatar_area_ha(12.5) == "12,50 ha"


def test_checar_limite_dentro_do_limite():
    validate.checar_limite(5, 20, item="áreas")  # não deve levantar


def test_checar_limite_estoura():
    with pytest.raises(validate.ErroUsuario):
        validate.checar_limite(21, 20, item="áreas")


def test_exigir_nome_vazio():
    with pytest.raises(validate.ErroUsuario):
        validate.exigir_nome("   ")


def test_exigir_nome_ok():
    assert validate.exigir_nome("  Talhão 1 ") == "Talhão 1"


def test_constantes_de_limite():
    assert validate.MAX_FEICOES_NB03 == 500
    assert validate.MAX_FEICOES_NB01 == 30
    assert validate.MAX_NUMEROS_CAR == 20
