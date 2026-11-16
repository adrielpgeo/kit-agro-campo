# CLAUDE.md — convenções do Kit Agro de Campo

Leia o `SPEC.md` para a visão completa. Este arquivo resume as regras práticas
que valem em todo o código.

## O produto em uma frase
3 notebooks Colab prontos para uso (não é curso). O usuário roda "Preparar",
preenche um formulário (`#@param`), roda "Executar" e recebe saídas no Google
Drive, incluindo um relatório `.docx` editável.

## Arquitetura
- Toda a lógica fica em `src/kitagro/`. Os notebooks só chamam `nbXX.executar()`.
- Funções que só existem no Colab (montar Drive, IA do Colab, formulários)
  ficam isoladas em `setup.py` e `ia.py`, **com fallback local** para rodar e
  testar no PC sem o Colab (base de saída: `./saida_local/`).
- Distribuição: a lib `kitagro` vira um repositório GitHub (público) e é
  instalada no Colab com `pip install git+https://...@vX.Y`. Até existir a
  primeira tag, o Colab instala a partir de um `.zip` no Drive.

## Regra dura: `_referencia/` é privado
- `_referencia/` contém código do Raio-X Rural (Vert3), **privado**. O repo do
  kit é **público**.
- **Nunca** importar, copiar ou colar arquivos de `_referencia/` para `src/`.
  Ao reaproveitar lógica (ex.: consulta ao SICAR na Fase 1), reescrever em
  `src/kitagro/`, não copiar.
- `_referencia/` está no `.gitignore`. Antes de qualquer commit, confirmar que
  ela não entra (`git status` / `git check-ignore _referencia`).

## Convenções geo (valem a partir da Fase 1)
- Leitura: aceitar qualquer CRS; reprojetar internamente.
- Área e perímetro: calcular em **EPSG:5880** (SIRGAS 2000 / Brazil Polyconic).
- Exportação vetorial: **EPSG:4674** (SIRGAS 2000 geográfico — padrão CAR/SIGEF).
- Área sempre em hectares, 2 casas decimais.

## Formatação e idioma
- Tudo em português. Voz impessoal nos textos técnicos.
- Números nos relatórios: padrão brasileiro (ponto de milhar, vírgula decimal).
  Use `validate.formatar_numero` / `validate.formatar_area_ha`.
- Erros previsíveis do usuário: levantar `validate.ErroUsuario(msg)`, com
  mensagem clara em português que diz **o que fazer**. No notebook, esse erro é
  exibido sem traceback.

## Texto técnico (IA)
- `ia.gerar_texto(tipo, dados)` tem 3 níveis com fallback: IA do Colab → chave
  Gemini do usuário → **template determinístico** (sempre funciona).
- A IA usa **somente** os números de `dados`; proibido inventar causas, doses ou
  recomendações agronômicas. Em anomalia, sugerir verificação a campo.
- O relatório marca o texto de IA como "gerado automaticamente — revisar".

## Relatório
- `relatorio.gerar_relatorio` monta o `.docx`: cabeçalho, seções, texto técnico
  (marcado) e seção obrigatória "Fontes e limitações" + aviso de que é material
  de apoio e não substitui vistoria.

## Fluxo ao fim de cada fase
1. Rodar `pytest` e executar `nbXX.executar()` com as fixtures em `saida_local/`.
2. Listar: o que foi feito, o que ficou pendente, o que não dá para testar
   localmente.
3. O Claude Code **não acessa o Colab**. Preparar um roteiro curto de teste e
   **esperar o autor rodar e relatar** antes de avançar de fase.
4. Só então fazer o commit da fase (confirmando que `_referencia/` ficou fora).

## Ambiente de desenvolvimento
- `.venv` com Python 3.11 local (Colab roda 3.13; piso do pacote: `>=3.10`).
- `pip install -e ".[dev]"` e `pytest` na raiz do projeto.
