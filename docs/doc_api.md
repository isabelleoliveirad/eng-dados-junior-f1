# Documentação da API OpenF1

**Base URL:** `https://api.openf1.org/v1`

**Documentação oficial:** https://openf1.org/docs/

| Recurso | Filtro usado | Campos consumidos |
| --- | --- | --- |
| `GET /meetings` | `year` | `meeting_key`, `meeting_name`, `country_name`, `date_start` |
| `GET /sessions` | `meeting_key` | `session_key`, `session_name`, `meeting_key`, `date_start` |
| `GET /drivers` | `session_key` | `driver_number`, `full_name`, `name_acronym`, `team_name` |
| `GET /laps` | `session_key` | `driver_number`, `lap_number`, `lap_duration`, `is_pit_out_lap` |

Exemplos:

```text
https://api.openf1.org/v1/meetings?year=2025
https://api.openf1.org/v1/sessions?meeting_key=1234
https://api.openf1.org/v1/drivers?session_key=9158
https://api.openf1.org/v1/laps?session_key=9161
```

Os números de chaves acima são **ilustrativos**, com exceção dos exemplos da documentação oficial; use as chaves obtidas na consulta anterior.

## Tratamento de erros

- O cliente define `timeout=25` segundos por tentativa.
- Para erros HTTP transitórios, o cliente tenta novamente (429, 500, 502, 503, 504), com backoff.
- Uma resposta HTTP não bem-sucedida ou JSON em formato inesperado gera `APIError`.
- Itens individuais inválidos são ignorados na validação com Pydantic e registrados em log.
- Dados históricos são gratuitos; dados ao vivo possuem outras condições de acesso.
