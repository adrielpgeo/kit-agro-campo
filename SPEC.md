# SPEC — Kit Agro de Campo (v1)

> Especificação para implementação com o Claude Code.
> Pasta do projeto no PC: `C:\Users\LAP\projetos\infoproduto\kit-agro-campo`
> Uso: salve este arquivo como `SPEC.md` nessa pasta e peça: *"Leia o SPEC.md e implemente a Fase 0. Pare ao final da fase e me mostre os critérios de aceite."* Siga fase a fase.

---

## 1. Visão do produto

Pack de 3 notebooks Google Colab **prontos para uso** (não é curso) para agrônomos, técnicos agrícolas e assistência técnica. O usuário:

1. abre o notebook, roda a célula **Preparar**;
2. preenche um **formulário** (campos `#@param` do Colab — nenhum código visível);
3. roda a célula **Executar**;
4. recebe no Google Drive: mapas, tabelas, arquivos geo e um **relatório .docx editável** com texto técnico pronto para colar no laudo.

Notebooks:

| # | Nome | Dor que resolve |
|---|------|-----------------|
| 01 | Vigor do Talhão (NDVI) | Acompanhar a lavoura e documentar o vigor sem abrir SIG |
| 02 | Chuva e Veranico | Comprovar chuva/estiagem para Proagro, sinistro e relatório técnico |
| 03 | Arquivo do Cliente Limpo | KML/KMZ/SHP bagunçado → shapefile correto com área em ha |

**Princípios inegociáveis**
- Zero cadastro: nada de Google Earth Engine, Google Cloud ou chave paga obrigatória.
- Fontes abertas com uso comercial permitido (Sentinel-2 via STAC, CHIRPS, NASA POWER).
- Mensagens de erro em português, explicando o que fazer.
- Tudo que sai é revisável pelo profissional; o relatório marca o texto da IA como "gerado automaticamente — revisar".

---

## 2. Arquitetura

```
C:\Users\LAP\projetos\infoproduto\kit-agro-campo\
├── SPEC.md
├── CLAUDE.md                  # convenções do projeto (criar na Fase 0)
├── .gitignore                 # inclui _referencia/, .venv/, saídas de teste
├── _referencia/               # NÃO versionar — código privado de consulta
│   └── sicar/                 # código SICAR do Raio-X Rural (só leitura)
├── src/kitagro/
│   ├── __init__.py            # __version__
│   ├── setup.py               # instalação no Colab + montagem do Drive
│   ├── io_geo.py              # leitura/limpeza/exportação de arquivos do usuário
│   ├── car.py                 # consulta de imóveis no geosserviço do SICAR
│   ├── validate.py            # validações, limites e mensagens de erro amigáveis
│   ├── sentinel.py            # busca STAC, offset, máscara SCL, NDVI
│   ├── mapbiomas.py           # recorte de área agrícola (Fase 3b)
│   ├── clima.py               # CHIRPS + NASA POWER
│   ├── mapas.py               # padrão de mapas: fundo, limites, localização (seção 3.7)
│   ├── limites.py             # limites de município e UF (IBGE)
│   ├── relatorio.py           # geração do .docx (python-docx)
│   ├── ia.py                  # geração de texto com fallback
│   ├── nb01.py                # executar() do Notebook 01
│   ├── nb02.py                # executar() do Notebook 02
│   └── nb03.py                # executar() do Notebook 03
├── notebooks/
│   ├── 01_vigor_talhao.ipynb
│   ├── 02_chuva_veranico.ipynb
│   └── 03_arquivo_limpo.ipynb
├── tests/
│   ├── fixtures/              # arquivos reais e "quebrados" de propósito
│   └── test_*.py
└── pyproject.toml
```

**Distribuição:** a biblioteca `kitagro` fica num repositório GitHub e é instalada na célula Preparar com `pip install git+https://...@vX.Y`. Os notebooks fixam a versão (tag). Atualizações = nova tag + notebook atualizado no Drive compartilhado com os compradores.

**Padrão de cada notebook (3 células visíveis):**
1. `# 🔧 Preparar` — instala `kitagro`, monta o Drive, mostra "✅ Pronto".
2. `# 📝 Formulário` — só campos `#@param`, com descrição curta em cada um.
3. `# ▶️ Executar` — chama uma única função (`kitagro.nb01.executar(**params)`), mostra progresso legível e um resumo final com links das saídas.

**Pasta de saída:** `MyDrive/KitAgroCampo/<notebook>/<AAAA-MM-DD>_<nome_area>/`

**Convenções geo**
- Leitura: qualquer CRS; reprojeta internamente.
- Cálculo de área e perímetro: **EPSG:5880** (SIRGAS 2000 / Brazil Polyconic).
- Exportação vetorial: **EPSG:4674** (SIRGAS 2000 geográfico — padrão CAR/SIGEF).
- Área sempre em hectares, 2 casas decimais, vírgula decimal nos relatórios.

**Dependências:** geopandas (pyogrio), shapely ≥ 2, pystac-client, planetary-computer, odc-stac, rioxarray, xarray, matplotlib, python-docx, requests. Verificar o que já vem no Colab antes de instalar; tempo da célula Preparar < 90 s.

**Ambiente de desenvolvimento (PC Windows do autor)**
- Ambiente virtual `.venv` com a **mesma versão de Python do Colab** (verificar a versão atual do Colab antes de criar).
- Toda a lógica fica em `src/kitagro/` e roda localmente com `pytest`; os notebooks só chamam `nbXX.executar()`. Assim o Claude Code testa quase tudo sem o Colab.
- Funções do Colab (montar Drive, `google.colab.ai`, formulários) ficam isoladas em `setup.py` e `ia.py`, com fallback local (pasta `saida_local/` no lugar do Drive).
- O repositório GitHub é criado na Fase 0, com orientação passo a passo (o autor é iniciante em Git/GitHub). Até existir a primeira tag, o Colab pode instalar a biblioteca por um `.zip` no Drive.

---

## 3. Módulos transversais

### 3.0 Entrada de áreas (comum aos 3 notebooks)
Todo notebook oferece no formulário `fonte_area`:
- **"Arquivo"** — upload ou caminho no Drive (formatos em 3.1);
- **"Número(s) do CAR"** — campo de texto aceitando um ou mais números separados por vírgula ou quebra de linha (módulo `car.py`, seção 3.5).

**Geometrias aceitas:** polígonos e multipolígonos; linhas fechadas são convertidas em polígono. Pontos e linhas abertas são descartados e listados no relatório ("3 pontos e 1 linha aberta foram ignorados"). Se não sobrar nenhum polígono → `ErroUsuario`.

**Múltiplas feições:** permitidas. Cada feição = uma área de análise (talhão ou imóvel), identificada pelo campo de nome do arquivo (`Name` no KML) ou numerada automaticamente (`Area_01`, `Area_02`…).

**Limites por execução (constantes em `validate.py`, fáceis de ajustar):**

| Notebook | Máx. feições | Outros limites | Motivo |
|----------|--------------|----------------|--------|
| 03 Arquivo Limpo | 500 | arquivo ≤ 50 MB | só geometria, é leve |
| 02 Chuva | 20 | — | agrupa áreas no mesmo pixel CHIRPS (~5 km) para não repetir download |
| 01 NDVI | 30 | soma das áreas ≤ 5.000 ha; extensão total ≤ 50 km | volume de imagens no Colab gratuito |
| CAR (qualquer notebook) | 20 números | — | estabilidade do geosserviço do SICAR |

Acima do limite: mensagem clara sugerindo dividir em mais de uma execução.

### 3.1 `io_geo.py` — leitura robusta
Aceitar: `.kml`, `.kmz`, `.zip` com shapefile, `.shp` (+ arquivos irmãos), `.geojson`, `.gpkg`, `.parquet` (GeoParquet).
- KMZ: descompactar e ler o `doc.kml`; ler **todas as camadas/pastas** do KML.
- Remover coordenada Z.
- `LineString` fechada (comum em KML desenhado como "caminho") → converter em polígono.
- Geometria inválida → `shapely.make_valid`; descartar pedaços não poligonais resultantes.
- Explodir multipartes quando o usuário pedir "manter talhões separados".
- Remover duplicatas exatas e fragmentos < 100 m² (parametrizável).
- Shapefile sem `.prj`: inferir CRS pelo intervalo das coordenadas (graus → EPSG:4674; metros → testar UTM 21S–25S e escolher a zona cujo centroide cai no Brasil) e **avisar** o usuário da suposição.
- Retornar sempre `(GeoDataFrame, lista_de_correções)`; cada correção é uma frase em português para o relatório.

### 3.2 `validate.py`
Exceção própria `ErroUsuario(msg)`, exibida sem traceback no notebook. Exemplos:
- "Não encontrei nenhum polígono no arquivo. Ele pode ter só pontos ou linhas abertas."
- "A área tem 0,4 ha. Com pixels de 10 m, o resultado de NDVI fica pouco confiável abaixo de 1 ha."
- "A área está fora do Brasil. Confira se latitude e longitude não estão invertidas."
- Limite de área para o NB01: 5.000 ha por execução.

### 3.3 `ia.py` — texto técnico com fallback
`gerar_texto(tipo: str, dados: dict) -> str`, em três níveis, nessa ordem:
1. IA gratuita embutida no Colab (`google.colab.ai`), se disponível — **verificar a API atual na implementação**;
2. chave Gemini do próprio usuário nos Segredos do Colab (opcional);
3. **template determinístico** em português (sempre funciona, sem IA).

Regras do prompt:
- Português técnico, voz impessoal, 1 a 2 parágrafos.
- Usar **somente** os números de `dados`; proibido inventar causas, doses ou recomendações agronômicas fechadas.
- Quando houver anomalia, sugerir **verificação a campo**, não diagnosticar.
- Citar a fonte dos dados ao final.

### 3.4 `relatorio.py`
Gera `.docx` com: cabeçalho (nome da área, produtor, data, notebook e versão), seções do notebook, figuras, tabelas, texto técnico (marcado "gerado automaticamente — revisar"), seção **Fontes e limitações** (créditos obrigatórios: "Contém dados Copernicus Sentinel modificados [ano]", citação CHIRPS, NASA POWER) e aviso de que o documento é material de apoio e não substitui vistoria.

### 3.5 `car.py` — imóvel direto do SICAR
**Reaproveitar o código de consulta ao geosserviço do SICAR já desenvolvido para o Raio-X Rural**, que está em `_referencia/sicar/`. Ler esse código, extrair só a parte de consulta do CAR e implementar em `src/kitagro/car.py`, adaptado ao Colab. **Nunca importar nem copiar arquivos de `_referencia/` para `src/`**, e `_referencia/` deve estar no `.gitignore` (o repositório do kit é público; o Raio-X Rural não).
- Normalizar o número: aceitar com ou sem pontos, maiúsculas/minúsculas, espaços. Validar o padrão `UF-CódigoIBGE(7 dígitos)-32 caracteres hexadecimais`; número inválido → mensagem dizendo qual está errado, sem parar os demais.
- Consultar cada CAR com tentativas (3 retries, espera crescente) e timeout; **testar cedo se o geosserviço responde a partir do Colab** (IPs do Google podem ser bloqueados ou limitados).
- Trazer junto, quando o serviço fornecer: situação do cadastro, área declarada, município, módulos fiscais. Levar ao relatório e comparar área declarada vs. calculada (EPSG:5880).
- CAR não encontrado ou serviço fora do ar → seguir com os demais e listar os que falharam; se todos falharem, sugerir baixar o shapefile na Consulta Pública do SICAR e usar a opção "Arquivo".
- Retornar `GeoDataFrame` no mesmo padrão de `io_geo.ler_arquivo` (campo `nome` = número do CAR).
- **Fora do escopo aqui:** qualquer cruzamento com camadas de restrição (é o Raio-X Rural).

### 3.6 Exportação vetorial (`io_geo.exportar`)
Formulário com uma caixa de seleção por formato (o Colab não tem seleção múltipla): `saida_shp` (padrão marcado), `saida_gpkg`, `saida_geojson`, `saida_geoparquet`, `saida_kml`. Pelo menos um obrigatório.
- Todos em EPSG:4674, mesmos atributos.
- **Shapefile:** zipado; nomes de campo com até 10 caracteres (definir nomes curtos fixos: `nome`, `area_ha`, `perim_m`, `car`, `zona`); codificação UTF-8 com `.cpg`.
- **GeoJSON:** EPSG:4674 declarado no arquivo e aviso no relatório de que alguns programas assumem WGS84 (diferença prática desprezível para área).
- **GeoParquet:** `GeoDataFrame.to_parquet`; nota no relatório de que abre no QGIS recente e em Python/Databricks.
- **GeoPackage:** uma camada por tipo de saída (ex.: `areas`, `zonas_vigor`).


### 3.7 Padrão de mapas (`mapas.py` + `limites.py`)
**Vale para todo mapa ou visualização de área nos 3 notebooks.**

**Limites políticos (sempre presentes)**
- Município(s) e UF que contêm as áreas, via **API de Malhas do IBGE** (malha mais recente; **verificar o endpoint atual na implementação**). Baixar só a UF necessária, com municípios, e guardar em cache na sessão.
- Identificar município e UF por interseção espacial (ou pelo código IBGE contido no número do CAR).
- No mapa principal: contorno do município em linha tracejada e rótulo com o nome; UF quando couber na extensão.
- **Mapa de localização** em cada figura principal (canto inferior): Brasil com a UF destacada e a UF com o município destacado. É o padrão de laudo técnico.
- Município e UF também entram no cabeçalho do relatório e nas tabelas.

**Mapa de fundo (escolha do usuário)**
Campo de formulário `mapa_base` com as opções:

| Opção | Fonte | Observação |
|-------|-------|------------|
| Satélite (Sentinel-2) — **padrão** | Composição recente sem nuvem gerada pelo `sentinel.py` | Licença livre, 10 m; disponível a partir da Fase 3 |
| Satélite alta resolução | Esri World Imagery (tiles) | Resolução submétrica na maior parte do Brasil |
| Claro | CARTO Positron (tiles) | — |
| Escuro | CARTO Dark Matter (tiles) | — |
| Sem fundo | Fundo liso + grade de coordenadas | Sempre funciona, sem internet extra |

Regras:
- **Implementar todas as opções da tabela.** Usar `contextily` (ou equivalente) para os tiles; deixar os provedores numa lista configurável em `mapas.py`, para trocar ou acrescentar um provedor sem mexer no resto.
- **Instrução de uso ao usuário:** cada notebook com mapa tem, logo acima do formulário, uma célula de texto curta: "Os mapas de fundo de satélite de alta resolução, claro e escuro vêm de provedores externos (Esri, CARTO), cada um com seus próprios termos de uso. Ao usar esses fundos em trabalhos comerciais, confira os termos do provedor. As opções 'Satélite (Sentinel-2)' e 'Sem fundo' não têm essa restrição." O mesmo aviso aparece, em uma linha, na seção "Fontes e limitações" do relatório quando um desses fundos for usado.
- Atribuição obrigatória do provedor no canto do mapa e na seção "Fontes e limitações" do relatório.
- Se o provedor falhar (rede, limite), cair automaticamente para "Sem fundo" e avisar, sem interromper a execução.
- Ajustar o estilo dos elementos ao fundo: contornos claros sobre satélite e escuro; contornos escuros sobre claro.
- Elementos fixos em todo mapa: escala gráfica, norte, legenda, grade de coordenadas (graus decimais), título, data e "Datum: SIRGAS 2000".
- Exportar PNG em 300 dpi, tamanho adequado para página A4 do relatório.

**Campos de formulário comuns** (nos notebooks com mapa): `mapa_base` (lista acima) e `rotular_municipios` (checkbox, padrão marcado).

---

## 4. Notebook 03 — Arquivo do Cliente Limpo *(construir primeiro)*

**Formulário**
- `fonte_area`: "Arquivo" | "Número(s) do CAR" (seção 3.0)
- `arquivo` ou `numeros_car`
- `nome_area` (texto)
- `modo`: "Manter talhões separados" | "Unir tudo em um polígono"
- `remover_fragmentos_m2` (padrão 100)
- `mapa_base`, `rotular_municipios` (seção 3.7)
- Formatos de saída: caixas `saida_shp`, `saida_gpkg`, `saida_geojson`, `saida_geoparquet`, `saida_kml` (seção 3.6)

**Processamento:** `io_geo.ler_arquivo` → limpeza → checagem de sobreposição entre talhões (reportar área sobreposta em ha, não corrigir automaticamente) → área e perímetro (EPSG:5880) → centroide (lat/long em graus decimais e GMS) → zona UTM.

**Saídas**
- Arquivos vetoriais nos formatos escolhidos (seção 3.6), EPSG:4674, campos `nome`, `area_ha`, `perim_m` (+ `car` quando a fonte for o CAR)
- `tabela_areas.csv` (inclui área declarada no CAR vs. calculada, quando aplicável)
- `mapa.png`: polígonos com rótulos de nome e área, no padrão da seção 3.7 (limites, localização, fundo escolhido).
  - **Fase 1:** opções "Claro", "Escuro", "Satélite alta resolução" e "Sem fundo".
  - **Fase 3:** entra a opção "Satélite (Sentinel-2)", que passa a ser o padrão.
- `relatorio.docx`: áreas, coordenadas, lista de correções feitas e um resumo em linguagem simples (IA) para enviar ao produtor

**Critérios de aceite**
- Lê todas as fixtures, incluindo: KMZ com pastas aninhadas, KML com linha fechada, SHP sem `.prj` em UTM 22S, polígono com auto-interseção, arquivo com pontos misturados.
- Área calculada difere < 0,1% de referência conhecida (comparar com uma área do SIGEF ou CAR).
- Tempo total < 60 s para até 50 talhões.

---

## 5. Notebook 02 — Chuva e Veranico

**Formulário**
- `entrada`: "Coordenada" | "Arquivo" | "Número(s) do CAR" — com áreas, usa o centroide de cada uma; áreas no mesmo pixel CHIRPS compartilham a série e o relatório informa isso
- `latitude`, `longitude` (graus decimais), `arquivo` ou `numeros_car`
- `data_inicio`, `data_fim`
- `data_plantio` (opcional — habilita contagem em dias após plantio)
- `cultura` (lista: soja, milho, trigo, arroz, feijão, outra)
- `limiar_dia_seco_mm` (padrão 1,0)
- `duracao_min_veranico_dias` (padrão 10 — parametrizável para seguir o critério do laudo)
- `mapa_base`, `rotular_municipios` (seção 3.7)

**Dados**
- **Chuva diária:** CHIRPS (0,05°). Ler só o pixel de interesse dos COGs diários via leitura por janela HTTP. **Verificar na implementação** a versão atual (v2 ou v3), a URL e a latência dos dados finais vs. preliminares; marcar dias preliminares no relatório.
- **Normal climatológica:** CHIRPS mensal 1991–2020 do mesmo pixel.
- **Temperatura:** NASA POWER API diária (`T2M_MAX`, `T2M_MIN`), mesmo ponto.
- **Fallback de chuva** para os dias mais recentes ainda sem CHIRPS: NASA POWER `PRECTOTCORR`, sinalizado como fonte diferente.

**Processamento**
- Série diária, acumulado do período e por mês.
- Anomalia mensal (% em relação à normal 1991–2020).
- Veranicos: sequências de dias com chuva < limiar e duração ≥ mínimo; para cada um, início, fim, duração e, com plantio informado, intervalo em dias após o plantio.
- Contagem de dias com Tmax ≥ 35 °C no período (limiar parametrizável).

**Saídas**
- `grafico_chuva.png`: barras diárias + linha do acumulado + acumulado normal esperado
- `tabela_mensal.csv`, `tabela_veranicos.csv`, `serie_diaria.csv`
- `mapa_localizacao.png`: ponto(s) ou área(s) analisados, com o quadrado do pixel CHIRPS (~5 km) desenhado, no padrão da seção 3.7
- `relatorio.docx`, com o texto técnico (IA) no formato de parágrafo para Proagro/sinistro/relatório

**Limitações a declarar no relatório:** estimativa por satélite, resolução de cerca de 5 km, não substitui pluviômetro local nem a vistoria do agente; material de apoio.

**Critérios de aceite**
- Para um ponto e período conhecidos (ex.: estiagem 2021/22 no RS), o acumulado bate com o CHIRPS consultado manualmente.
- Detecção de veranico testada com série sintética de resultado conhecido.
- Tempo total < 2 min para 1 safra (≈ 180 dias).

---

## 6. Notebook 01 — Vigor do Talhão (NDVI)

**Formulário**
- `fonte_area`: "Arquivo" (talhões — recomendado) | "Número(s) do CAR"
- `arquivo` ou `numeros_car`
- `nome_produtor`, `nome_talhao`, `cultura`
- `so_area_agricola` (checkbox; **marcado por padrão quando a fonte é o CAR**)
- `data_inicio`, `data_fim` (safra atual)
- `comparar_safra_anterior` (checkbox — mesmas datas, ano anterior)
- `nuvem_max_cena` (padrão 60%)
- `cobertura_valida_min` (padrão 70% dos pixels do talhão)
- `num_zonas` (padrão 3)
- `mapa_base`, `rotular_municipios` (seção 3.7) — nos mapas de NDVI e de zonas o fundo aparece só fora das áreas analisadas
- Formatos de saída das zonas de vigor: caixas `saida_shp`, `saida_gpkg`, `saida_geojson`, `saida_geoparquet`, `saida_kml` (seção 3.6)

**Regra para entrada pelo CAR (módulo `mapbiomas.py`):** o polígono do CAR é o imóvel inteiro (mata, APP, pasto, sede). Com `so_area_agricola` marcado, recortar a área de análise pelas classes agrícolas do MapBiomas Coleção mais recente (lavouras temporárias e perenes; **conferir os códigos de classe e a forma de acesso aos rasters da coleção vigente na implementação**), vetorizar e usar cada bloco agrícola ≥ 5 ha como uma área de análise. Desmarcado: analisar o imóvel inteiro e avisar no relatório que o NDVI mistura usos diferentes. Mostrar no relatório o mapa da área agrícola usada, para o profissional conferir.

**Dados:** Sentinel-2 L2A via STAC do **Planetary Computer** (`sentinel-2-l2a`, assinatura com `planetary_computer.sign`). Alternativa de contingência: Earth Search (AWS). Bandas B04, B08, SCL, a 10 m.

**Tratamentos obrigatórios**
1. **Offset de reflectância:** para cenas com `s2:processing_baseline` ≥ 04.00 (a partir de 25/01/2022), subtrair 1000 dos números digitais antes de escalar por 10000. Teste unitário obrigatório com cenas antes e depois da mudança.
2. **Máscara de nuvem (SCL):** manter só as classes 4 (vegetação), 5 (solo exposto) e 6 (água); descartar sombra, nuvens, cirros, saturados e sem dado.
3. **Filtro por talhão:** descartar a data se a cobertura válida dentro do talhão for menor que `cobertura_valida_min`.
4. Mesma data em tiles diferentes → mosaicar antes de calcular.

**Processamento**
- Série temporal por talhão: NDVI médio, P10 e P90 por data válida.
- Curva da safra atual vs. anterior, alinhadas por dia da safra.
- Data de pico (máximo NDVI médio) e última imagem válida.
- **Zonas de vigor:** NDVI mediano da janela do pico (±15 dias), classificado em `num_zonas` quantis (baixo / médio / alto); vetorizar, suavizar levemente e calcular a área de cada zona em ha.
  - Nomear como "zonas de vigor da safra", **nunca** "zonas de manejo" (estas exigem histórico de várias safras).
- Diferença de NDVI entre a última imagem e a imagem equivalente da safra anterior (se houver).

**Saídas**
- `serie_ndvi.csv`, `grafico_serie.png`
- `mapa_ndvi_pico.png`, `mapa_ndvi_ultima.png`
- Zonas de vigor nos formatos escolhidos (seção 3.6, EPSG:4674, campos `nome`, `zona`, `area_ha`) + `mapa_zonas.png` + tabela de área por zona
- `ndvi_pico.tif` (GeoTIFF para uso em SIG)
- `relatorio.docx` com o diagnóstico (IA): comportamento da curva, comparação com a safra anterior, áreas de menor vigor em ha e % e sugestão de verificação a campo nessas manchas

**Critérios de aceite**
- Talhão de 100 ha, 1 safra, roda em < 4 min num Colab gratuito.
- NDVI médio de uma data conferido manualmente no Copernicus Browser (diferença < 0,02).
- Mensagem clara quando não há nenhuma imagem válida no período.

---

## 7. Fases de construção (ciclos pequenos)

| Fase | Entrega | Pronto quando |
|------|---------|---------------|
| 0 | Estrutura do repo, `CLAUDE.md`, `setup.py`, `validate.py`, `relatorio.py` (docx básico), `ia.py` com template determinístico | Notebook "hello" gera um .docx no Drive num Colab limpo |
| 1 | `io_geo.py` + exportação multiformato + `car.py` + `limites.py` + `mapas.py` (padrão 3.7, sem Sentinel) + NB03 completo + fixtures | Critérios de aceite do NB03; 5 números de CAR reais de UFs diferentes retornam no Colab |
| 2 | `clima.py` + NB02 | Critérios de aceite do NB02 |
| 3 | `sentinel.py` + NB01 (entrada por arquivo) + opção de fundo "Satélite (Sentinel-2)" em todos os mapas | Critérios de aceite do NB01 |
| 3b | Entrada pelo CAR no NB01 com recorte agrícola MapBiomas | 3 imóveis reais com lavoura + mata: áreas agrícolas recortadas conferem visualmente |
| 4 | IA nos três níveis + revisão dos textos | Textos revisados por você em 3 casos reais por notebook |
| 5 | Empacotamento: vídeos curtos de uso, Drive de entrega, tag v1.0 | Um agrônomo de fora roda os 3 sem sua ajuda |

**Regra para o Claude Code ao fim de cada fase:**
1. Rodar `pytest` localmente e executar `nbXX.executar()` com as fixtures, gravando em `saida_local/`.
2. Listar o que foi feito, o que ficou pendente e o que não pôde ser testado localmente.
3. **O Claude Code não acessa o Colab.** Preparar um roteiro curto de teste no Colab (o que abrir, o que preencher, o que conferir na saída) e **esperar o autor rodar e relatar o resultado**. Só avançar de fase depois desse retorno.
4. Fazer commit da fase com mensagem descritiva (confirmando antes que `_referencia/` não entra no commit).

---

## 8. Fora do escopo da v1
- Cruzamentos com embargos, TI, UC, PRODES (pertencem ao Raio-X Rural / Vert3).
- Google Earth Engine (licença comercial e cotas).
- Zonas de manejo multi-safra, recomendação de adubação, produtividade estimada.
- Interface fora do Colab (Streamlit, desktop).
