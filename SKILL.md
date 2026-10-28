---
name: f1
description: Orientações de manutenção do dashboard F1 educacional.
---

# Skill — Manutenção do projeto F1

Ao modificar o projeto:

1. Leia o `README.md`, o `plan.md` e `docs/doc_api.md`.
2. Nunca invente campos ou endpoints da API; confira https://openf1.org/docs/.
3. Mantenha requisições HTTP em `src/f1/api.py` e regras puras em `src/f1/processing.py`.
4. Não coloque tokens, senhas ou chaves reais no repositório.
5. Acrescente testes para cada regra corrigida.
6. Execute `python -m pytest`, `python -m ruff check .` e `python -m mkdocs build --strict`.
7. Atualize a documentação ao alterar o comportamento.
8. Seja explícito quando um endpoint não retornar dados ou quando ocorrer erro de rede.
