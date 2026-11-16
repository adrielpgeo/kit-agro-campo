# Roteiro de teste no Colab — Fase 0

Objetivo: confirmar que o notebook "hello" instala o `kitagro`, monta o Drive e
gera um `.docx` num Colab limpo. **Só você consegue fazer este teste** (o Claude
Code não acessa o Colab).

Tempo estimado: ~5 minutos.

## Antes de começar
Você vai usar 2 arquivos que estão no projeto, na pasta
`C:\Users\LAP\projetos\infoproduto\kit-agro-campo`:

- `dist\kitagro-0.0.1-py3-none-any.whl`  ← o pacote
- `notebooks\00_hello.ipynb`             ← o notebook

## Passo 1 — Subir o pacote no Drive
1. Abra o Google Drive (mesma conta que você usará no Colab).
2. Crie as pastas: **KitAgroCampo** → dentro dela **_pacote**.
   (Caminho final: `MyDrive/KitAgroCampo/_pacote/`.)
3. Faça upload do arquivo `kitagro-0.0.1-py3-none-any.whl` para dentro de
   `_pacote`.

> Dica: o nome do arquivo precisa bater com o da célula "Preparar". Se mudar,
> ajuste a linha do `pip install` no notebook.

## Passo 2 — Abrir o notebook no Colab
1. Em https://colab.research.google.com → **Arquivo → Fazer upload de notebook**.
2. Envie `00_hello.ipynb`.
   (Ou: suba o `.ipynb` para o Drive e abra com o Google Colab.)

## Passo 3 — Rodar
1. Rode a célula **🔧 Preparar**.
   - Autorize o acesso ao Drive quando pedir.
   - Esperado ao final: `✅ Pronto — kitagro 0.0.1`.
2. Rode a célula **📝 Formulário** (pode deixar os valores de exemplo).
3. Rode a célula **▶️ Executar**.
   - Esperado: `✅ Relatório gerado:` seguido de um caminho dentro de
     `MyDrive/KitAgroCampo/00_hello/...`.

## Passo 4 — Conferir a saída
1. No Drive, abra
   `MyDrive/KitAgroCampo/00_hello/<data>_fazenda-modelo/relatorio.docx`.
2. Confirme que o documento tem:
   - Título "Kit Agro de Campo — teste de encanamento";
   - Cabeçalho com Área, Produtor, Data, Notebook e Versão;
   - Seção "Objetivo";
   - Seção "Resumo técnico" com o aviso "⚠ Texto gerado automaticamente — revisar";
   - Seção "Fontes e limitações" com o disclaimer.

## O que me relatar
- A célula Preparar terminou em menos de ~90 s? (anote o tempo aproximado)
- Apareceram os dois `✅`?
- O `.docx` abriu e tinha as seções acima?
- Qualquer mensagem de erro (copie o texto).

Com esse retorno eu fecho a Fase 0: criamos o repositório no GitHub (passo a
passo) e eu faço o commit da fase.
