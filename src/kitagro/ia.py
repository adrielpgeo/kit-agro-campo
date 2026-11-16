"""Geração de texto técnico com fallback de 3 níveis (seção 3.3 do SPEC).

Ordem:
  1. IA gratuita do Colab (google.colab.ai) — a implementar na Fase 4.
  2. Chave Gemini do usuário nos Segredos do Colab — a implementar na Fase 4.
  3. Template determinístico em português — SEMPRE funciona (este arquivo).

Regras do texto (valem para todos os níveis): português técnico, voz impessoal,
usar SOMENTE os números de `dados`, nunca inventar causas/doses/recomendações,
e sugerir verificação a campo quando houver anomalia. O relatório marca o texto
como "gerado automaticamente — revisar".
"""
from __future__ import annotations

from .validate import formatar_area_ha


def gerar_texto(tipo: str, dados: dict) -> str:
    """Retorna um parágrafo técnico em português.

    Tenta os níveis 1 e 2 (IA) e, em qualquer falha ou indisponibilidade,
    cai no template determinístico do nível 3.
    """
    for tentativa in (_tentar_colab_ai, _tentar_gemini):
        try:
            texto = tentativa(tipo, dados)
        except Exception:
            texto = None
        if texto:
            return texto.strip()
    return _template(tipo, dados).strip()


# --- Níveis 1 e 2: stubs até a Fase 4 (retornam None => usa o template). ---
def _tentar_colab_ai(tipo: str, dados: dict) -> str | None:
    return None


def _tentar_gemini(tipo: str, dados: dict) -> str | None:
    return None


# --- Nível 3: templates determinísticos. ---
def _template(tipo: str, dados: dict) -> str:
    gerador = _TEMPLATES.get(tipo, _template_generico)
    return gerador(dados)


def _template_resumo_area(d: dict) -> str:
    nome = d.get("nome_area") or d.get("nome") or "a área"
    produtor = d.get("produtor")
    frase = f"Documento de apoio referente a {nome}"
    if produtor:
        frase += f", de responsabilidade de {produtor}"
    frase += "."
    partes = [frase]
    if d.get("area_ha") is not None:
        partes.append(f"A área calculada é de {formatar_area_ha(d['area_ha'])}.")
    partes.append(
        "As informações foram processadas automaticamente e devem ser "
        "conferidas pelo profissional responsável antes do uso em laudo."
    )
    return " ".join(partes)


def _template_generico(d: dict) -> str:
    if not d:
        return (
            "Não há dados suficientes para gerar o texto automaticamente. "
            "Preencha as informações e gere novamente."
        )
    itens = "; ".join(f"{k}: {v}" for k, v in d.items() if v is not None)
    return (
        "Resumo gerado automaticamente a partir dos dados informados "
        f"({itens}). Confira antes de usar em laudo."
    )


_TEMPLATES = {
    "resumo_area": _template_resumo_area,
}
