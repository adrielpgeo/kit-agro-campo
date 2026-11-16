"""Validações, limites e mensagens de erro amigáveis (seções 3.0 e 3.2 do SPEC).

As constantes de limite ficam aqui, juntas e fáceis de ajustar.
"""
from __future__ import annotations


class ErroUsuario(Exception):
    """Erro previsível do usuário, exibido no notebook sem traceback."""


# --- Limites por execução (seção 3.0 do SPEC). ---
MAX_FEICOES_NB03 = 500
MAX_ARQUIVO_MB_NB03 = 50

MAX_FEICOES_NB02 = 20

MAX_FEICOES_NB01 = 30
MAX_SOMA_AREA_HA_NB01 = 5_000
MAX_EXTENSAO_KM_NB01 = 50

MAX_NUMEROS_CAR = 20

# Área mínima confiável para NDVI (seção 3.2).
AREA_MIN_NDVI_HA = 1.0

# Fragmentos menores que isto são descartados por padrão (seção 3.1).
FRAGMENTO_MIN_M2 = 100


def formatar_numero(valor: float, casas: int = 2) -> str:
    """Formata no padrão brasileiro: ponto de milhar e vírgula decimal.

    >>> formatar_numero(1234.5)
    '1.234,50'
    """
    texto = f"{valor:,.{casas}f}"  # en-US: '1,234.50'
    return texto.replace(",", "\x00").replace(".", ",").replace("\x00", ".")


def formatar_area_ha(valor_ha: float) -> str:
    """Área em hectares no padrão do relatório. Ex.: '12,50 ha'."""
    return f"{formatar_numero(valor_ha, 2)} ha"


def checar_limite(qtd: int, maximo: int, *, item: str,
                  sugestao: str | None = None) -> None:
    """Levanta ErroUsuario se qtd > maximo, com mensagem clara."""
    if qtd > maximo:
        base = f"Você enviou {qtd} {item}, mas o limite por execução é {maximo}."
        extra = f" {sugestao}" if sugestao else " Divida em mais de uma execução."
        raise ErroUsuario(base + extra)


def exigir_nome(nome: str, *, campo: str = "nome da área") -> str:
    """Garante que um campo de texto obrigatório não está vazio."""
    nome = (nome or "").strip()
    if not nome:
        raise ErroUsuario(f"Preencha o {campo}.")
    return nome
