"""Integração com o Colab: montar o Drive, definir a pasta de saída e instalar
dependências (seção 2 do SPEC).

Isolado aqui para que o resto da biblioteca rode localmente com pytest. Fora do
Colab, a base de saída é a pasta ./saida_local/.
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

PASTA_RAIZ = "KitAgroCampo"

# (módulo_de_import, pacote_pip) das dependências a garantir no Colab.
# Cresce a cada fase (geopandas, rioxarray, etc.); na Fase 0 só o docx.
_DEPENDENCIAS = [
    ("docx", "python-docx"),
]


def imprimir(msg: str) -> None:
    """print() resiliente: no Colab mostra UTF-8 (emojis); em consoles sem UTF-8
    (ex.: Windows cp1252) substitui o que não couber em vez de quebrar."""
    try:
        print(msg)
    except UnicodeEncodeError:
        import sys

        enc = (sys.stdout.encoding or "utf-8") if sys.stdout else "utf-8"
        print(msg.encode(enc, errors="replace").decode(enc))


def em_colab() -> bool:
    """True quando rodando dentro do Google Colab."""
    try:
        import google.colab  # noqa: F401

        return True
    except Exception:
        return False


def base_saida() -> Path:
    """Pasta raiz das saídas: Google Drive no Colab, ./saida_local fora dele."""
    if em_colab():
        _montar_drive()
        base = Path("/content/drive/MyDrive") / PASTA_RAIZ
    else:
        base = Path("saida_local").resolve()
    base.mkdir(parents=True, exist_ok=True)
    return base


def pasta_saida(notebook: str, nome_area: str, base: Path | None = None) -> Path:
    """<base>/<notebook>/<AAAA-MM-DD>_<nome_area>/ (criada se não existir)."""
    base = Path(base) if base is not None else base_saida()
    sub = f"{date.today():%Y-%m-%d}_{_slug(nome_area)}"
    pasta = base / notebook / sub
    pasta.mkdir(parents=True, exist_ok=True)
    return pasta


def preparar() -> Path:
    """Chamada na célula 'Preparar' dos notebooks. Retorna a base de saída."""
    _instalar_dependencias()
    base = base_saida()
    destino = "Google Drive (MyDrive/%s)" % PASTA_RAIZ if em_colab() else str(base)
    imprimir(f"✅ Pronto. As saídas vão para: {destino}")
    return base


# --- internos ---
def _montar_drive() -> None:
    from google.colab import drive  # type: ignore

    if not Path("/content/drive/MyDrive").exists():
        drive.mount("/content/drive")


def _instalar_dependencias() -> None:
    """No Colab, instala o que faltar. Local: nada (o venv já tem tudo)."""
    if not em_colab():
        return
    import importlib
    import subprocess
    import sys

    faltando = []
    for modulo, pacote in _DEPENDENCIAS:
        try:
            importlib.import_module(modulo)
        except Exception:
            faltando.append(pacote)
    if faltando:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-q", *faltando],
            check=True,
        )


def _slug(texto: str) -> str:
    texto = (texto or "area").strip().lower()
    texto = re.sub(r"[^\w\s-]", "", texto, flags=re.UNICODE)
    texto = re.sub(r"[\s_-]+", "-", texto).strip("-")
    return texto or "area"
