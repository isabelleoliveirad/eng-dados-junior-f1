# Arquitetura

```text
OpenF1 (API REST)
       |
       v
src/f1/api.py        -> HTTP, retries, status, JSON
       |
       v
src/f1/models.py     -> validação Pydantic
       |
       v
src/f1/processing.py -> filtros, ordenação, ranking
       |
       v
src/f1/dashboard.py  -> Streamlit, Plotly, CSV
       |
       v
app.py               -> ponto de entrada do Streamlit
```

O dashboard utiliza `st.cache_data(ttl=3600)` nas quatro consultas para reduzir chamadas repetidas.

A função `classificar_voltas` é **pura**, permitindo testes sem acessar a internet.

A opção **melhor volta de cada piloto** impede a repetição de pilotos; se desmarcada, retorna as cinco voltas mais rápidas da sessão, mesmo que pertençam ao mesmo piloto.

O processo de CI executa Ruff, Pytest e MkDocs, mas **não publica automaticamente o Streamlit**.
