from f1.models import Driver, Lap
from f1.processing import classificar_voltas, tempo_formatado


def test_ordenacao_e_limite():
    pilotos = [Driver(driver_number=1, full_name="Um"), Driver(driver_number=2, full_name="Dois")]
    voltas = [
        Lap(driver_number=1, lap_number=1, lap_duration=92),
        Lap(driver_number=2, lap_number=1, lap_duration=90),
        Lap(driver_number=1, lap_number=2, lap_duration=89),
    ]
    resultado = classificar_voltas(voltas, pilotos, limite=2)
    assert [x["Tempo (s)"] for x in resultado] == [89.0, 90.0]
    assert resultado[0]["Piloto"] == "Um"
    assert resultado[0]["Posição"] == 1


def test_melhor_volta_por_piloto():
    voltas = [
        Lap(driver_number=1, lap_duration=88),
        Lap(driver_number=1, lap_duration=89),
        Lap(driver_number=2, lap_duration=90),
    ]
    resultado = classificar_voltas(voltas, [], apenas_melhor_por_piloto=True)
    assert [r["Número"] for r in resultado] == [1, 2]
    assert resultado[0]["Piloto"] == "Piloto #1"


def test_ignora_tempos_invalidos_e_pit_out():
    voltas = [
        Lap(driver_number=1, lap_duration=None),
        Lap(driver_number=1, lap_duration=0),
        Lap(driver_number=1, lap_duration=-1),
        Lap(driver_number=1, lap_duration=float("nan")),
        Lap(driver_number=1, lap_duration=float("inf")),
        Lap(driver_number=1, lap_duration=80, is_pit_out_lap=True),
        Lap(driver_number=1, lap_duration=90),
    ]
    resultado = classificar_voltas(voltas, [])
    assert len(resultado) == 1
    assert resultado[0]["Tempo (s)"] == 90


def test_limite_zero():
    assert classificar_voltas([], [], limite=0) == []


def test_tempo_formatado():
    assert tempo_formatado(90.123) == "1:30.123"
    assert tempo_formatado(59.999) == "0:59.999"


def test_nome_e_equipe_do_piloto():
    piloto = Driver(driver_number=44, full_name="Piloto 44", team_name="Equipe X")
    resultado = classificar_voltas([Lap(driver_number=44, lap_duration=80)], [piloto])
    assert resultado[0]["Piloto"] == "Piloto 44"
    assert resultado[0]["Equipe"] == "Equipe X"
