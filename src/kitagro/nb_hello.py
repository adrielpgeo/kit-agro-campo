"""Notebook 00 "Hello" — teste de encanamento da Fase 0.

Gera um .docx de teste na pasta de saída para confirmar que a biblioteca, a
geração de relatório e a gravação no Drive funcionam de ponta a ponta. Os
notebooks reais (nb01/nb02/nb03) seguirão este mesmo padrão: uma única função
executar() chamada a partir da célula "Executar".
"""
from __future__ import annotations

from pathlib import Path

from . import __version__, ia, relatorio, setup, validate


def executar(
    *,
    nome_area: str,
    nome_produtor: str | None = None,
    base: Path | None = None,
) -> Path:
    """Gera o relatório de teste e retorna o caminho do .docx."""
    nome_area = validate.exigir_nome(nome_area)

    pasta = setup.pasta_saida("00_hello", nome_area, base=base)
    texto = ia.gerar_texto(
        "resumo_area", {"nome_area": nome_area, "produtor": nome_produtor}
    )
    caminho = relatorio.gerar_relatorio(
        pasta / "relatorio.docx",
        titulo="Kit Agro de Campo — teste de encanamento",
        area=nome_area,
        produtor=nome_produtor,
        notebook="00 Hello",
        versao=__version__,
        secoes=[
            (
                "Objetivo",
                "Este documento confirma que a geração de relatórios .docx "
                "funciona de ponta a ponta, do formulário ao arquivo salvo "
                "no Google Drive.",
            )
        ],
        texto_ia=texto,
        fontes=["Notebook de teste — nenhuma fonte de dados externa utilizada."],
    )
    setup.imprimir(f"✅ Relatório gerado:\n   {caminho}")
    return caminho
