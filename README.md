# 🏎️ Projeto Engenharia de Dados Júnior — F1 Dashboard

Aplicação educacional que coleta dados históricos da API [OpenF1](https://openf1.org/docs/), valida informações com **Pydantic**, processa tempos de volta com Python e exibe um dashboard em **Streamlit**, com tabelas e gráficos **Plotly**.

> Este projeto é independente, didático e não é afiliado à Fórmula 1.

## O que faz

- Consulta temporadas, Grandes Prêmios e sessões.
- Obtém tempos de volta e informações dos pilotos pela API OpenF1.
- Exclui tempos nulos, inválidos e voltas de saída dos boxes.
- Mostra as 5 voltas mais rápidas (ou a melhor volta de cada piloto).
- Gera gráfico interativo e permite baixar CSV.
- Possui testes automatizados, Ruff, documentação MkDocs e CI GitHub Actions.

## Como executar no Google Colab

1. Faça upload do ZIP do projeto ou use o notebook `CRIAR_PROJETO_COLAB.ipynb` fornecido com a entrega.
2. Instale: `!pip install -r requirements-dev.txt`
3. Rode os testes: `!python -m pytest`
4. O Colab não expõe o Streamlit como um site estável; para abrir o dashboard, publique no Streamlit Community Cloud (instruções abaixo).

## Como executar no computador

Requer Python 3.12 ou superior, abaixo de 4.0.

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
python -m ruff check .
streamlit run app.py
```

Abra `http://localhost:8501`.

Alternativamente, com Poetry 2:

```bash
poetry install --with dev
poetry run pytest
poetry run streamlit run app.py
```

## Publicar no GitHub

1. Crie um repositório **público** em sua conta GitHub (ex.: `eng-dados-junior-f1`).
2. Extraia o ZIP. Envie **o conteúdo da pasta extraída**, mantendo `app.py`, `requirements.txt`, `src/`, `tests/`, `.github/` etc. Não envie somente o ZIP.
3. Veja a execução de CI em **Actions**.
4. Copie o link do **seu** repositório para entregar no formulário.

## Publicar o dashboard

1. Acesse https://share.streamlit.io/ e conecte sua conta GitHub.
2. Selecione o repositório e a branch `main`.
3. Informe o arquivo principal **`app.py`**.
4. Aguarde o deploy. O serviço instala as dependências de `requirements.txt`.

## Estrutura

```text
app.py
src/f1/{api,models,processing,dashboard}.py
tests/{test_api,test_models,test_processing}.py
requirements.txt
requirements-dev.txt
pyproject.toml
mkdocs.yml
docs/{index,doc_api,architecture}.md
.github/workflows/ci.yml
plan.md
.claude/skills/f1/SKILL.md
```

## Fonte e limites

API: https://openf1.org/docs/

A OpenF1 disponibiliza dados históricos gratuitamente desde 2023; não confunda dados históricos com telemetria ao vivo. A disponibilidade e os limites da API podem mudar. Sessões futuras ou incompletas podem não retornar voltas.

## Observação sobre a entrega

Confira o **enunciado específico da atividade Engenharia de Dados Júnior** antes de entregar. Este projeto segue a ideia de dashboard F1, mas pode não substituir outros requisitos obrigatórios de engenharia de dados (pipeline ETL, banco de dados etc.).
