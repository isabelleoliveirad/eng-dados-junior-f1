from unittest.mock import Mock

import pytest
import requests

from f1.api import APIError, OpenF1Client


def criar_cliente(payload, status_error=None):
    resposta = Mock()
    resposta.json.return_value = payload
    if status_error:
        resposta.raise_for_status.side_effect = status_error
    sessao = Mock()
    sessao.get.return_value = resposta
    return OpenF1Client(session=sessao), sessao


def test_meetings_valida_e_filtra_itens_incorretos():
    cliente, sessao = criar_cliente([
        {"meeting_key": 12, "meeting_name": "GP Exemplo", "country_name": "Brasil"},
        {"meeting_name": "Sem identificador"},
    ])
    meetings = cliente.meetings(2025)
    assert len(meetings) == 1
    assert meetings[0].meeting_name == "GP Exemplo"
    sessao.get.assert_called_once_with(
        "https://api.openf1.org/v1/meetings", params={"year": 2025}, timeout=25
    )


def test_sessions():
    cliente, _ = criar_cliente([{"session_key": 56, "session_name": "Race"}])
    assert cliente.sessions(12)[0].session_key == 56


def test_drivers():
    cliente, _ = criar_cliente([{"driver_number": 44, "full_name": "Piloto A"}])
    assert cliente.drivers(56)[0].driver_number == 44


def test_laps():
    cliente, _ = criar_cliente([{"driver_number": 44, "lap_number": 3, "lap_duration": 89.5}])
    assert cliente.laps(56)[0].lap_duration == 89.5


def test_resposta_nao_e_lista():
    cliente, _ = criar_cliente({"error": "Falha"})
    with pytest.raises(APIError, match="esperada lista JSON"):
        cliente.meetings(2025)


def test_erro_http():
    cliente, _ = criar_cliente([], requests.HTTPError("429 Too Many Requests"))
    with pytest.raises(APIError, match="Falha ao consultar"):
        cliente.meetings(2025)


def test_json_invalido():
    cliente, sessao = criar_cliente([])
    sessao.get.return_value.json.side_effect = ValueError("JSON inválido")
    with pytest.raises(APIError):
        cliente.meetings(2025)


def test_erro_conexao():
    cliente, sessao = criar_cliente([])
    sessao.get.side_effect = requests.ConnectionError("sem rede")
    with pytest.raises(APIError):
        cliente.meetings(2025)
