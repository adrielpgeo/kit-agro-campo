"""Geração do relatório .docx (seção 3.4 do SPEC). Versão básica da Fase 0.

Fases seguintes acrescentam figuras, tabelas e os créditos de dados específicos
(Sentinel/CHIRPS/NASA POWER) conforme o notebook.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path

from docx import Document

AVISO_IA = "⚠ Texto gerado automaticamente — revisar antes de usar em laudo."
DISCLAIMER = (
    "Este documento é material de apoio ao trabalho técnico e não substitui "
    "vistoria a campo nem a avaliação do profissional responsável."
)


def gerar_relatorio(
    caminho,
    *,
    titulo: str,
    area: str,
    notebook: str,
    versao: str,
    produtor: str | None = None,
    municipio: str | None = None,
    uf: str | None = None,
    data: date | None = None,
    secoes: list[tuple[str, str]] | None = None,
    texto_ia: str | None = None,
    fontes: list[str] | None = None,
) -> Path:
    """Monta e salva o .docx. Retorna o caminho do arquivo gerado."""
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    data = data or date.today()

    doc = Document()
    doc.add_heading(titulo, level=0)

    # Cabeçalho (seção 3.4): identifica a área, o produtor, a data e a versão.
    cabecalho = [
        ("Área", area),
        ("Produtor", produtor),
        ("Município/UF", _municipio_uf(municipio, uf)),
        ("Data", data.strftime("%d/%m/%Y")),
        ("Notebook", notebook),
        ("Versão do kitagro", versao),
    ]
    for rotulo, valor in cabecalho:
        if not valor:
            continue
        p = doc.add_paragraph()
        p.add_run(f"{rotulo}: ").bold = True
        p.add_run(str(valor))

    # Seções de conteúdo.
    for sec_titulo, corpo in (secoes or []):
        doc.add_heading(sec_titulo, level=1)
        doc.add_paragraph(corpo)

    # Texto técnico (IA), sempre marcado como gerado automaticamente.
    if texto_ia:
        doc.add_heading("Resumo técnico", level=1)
        doc.add_paragraph().add_run(AVISO_IA).italic = True
        doc.add_paragraph(texto_ia)

    # Fontes e limitações (obrigatória).
    doc.add_heading("Fontes e limitações", level=1)
    for fonte in (fontes or []):
        doc.add_paragraph(fonte, style="List Bullet")
    doc.add_paragraph(DISCLAIMER)

    doc.save(str(caminho))
    return caminho


def _municipio_uf(municipio: str | None, uf: str | None) -> str | None:
    if municipio and uf:
        return f"{municipio} / {uf}"
    return municipio or uf
