# Kit Agro de Campo

Pack de 3 notebooks Google Colab **prontos para uso** para agrônomos, técnicos
agrícolas e assistência técnica. O usuário abre o notebook, roda "Preparar",
preenche um formulário, roda "Executar" e recebe no Google Drive mapas, tabelas,
arquivos geo e um **relatório .docx editável**.

| # | Notebook | Dor que resolve |
|---|----------|-----------------|
| 01 | Vigor do Talhão (NDVI) | Acompanhar a lavoura e documentar o vigor sem abrir SIG |
| 02 | Chuva e Veranico | Comprovar chuva/estiagem para Proagro, sinistro e relatório |
| 03 | Arquivo do Cliente Limpo | KML/KMZ/SHP bagunçado → shapefile correto com área em ha |

Fontes abertas com uso comercial permitido (Sentinel-2 via STAC, CHIRPS,
NASA POWER). Sem cadastro pago obrigatório.

## Para desenvolvedores

Toda a lógica fica em `src/kitagro/` e roda localmente com `pytest`. Os notebooks
apenas chamam `nbXX.executar()`.

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -e ".[dev]"
pytest
```

Estrutura, convenções e fases de construção: veja `SPEC.md` e `CLAUDE.md`.

Licença: MIT (veja `LICENSE`).
