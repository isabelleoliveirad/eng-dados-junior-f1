"""Regras puras de negócio para ranquear voltas de Fórmula 1."""

import math
from collections.abc import Iterable

from f1.models import Driver, Lap


def tempo_formatado(segundos: float) -> str:
    """Converte segundos para minutos:segundos.milésimos."""
    minutos, resto = divmod(segundos, 60)
    return f"{int(minutos)}:{resto:06.3f}"


def classificar_voltas(
    voltas: Iterable[Lap],
    pilotos: Iterable[Driver],
    limite: int = 5,
    apenas_melhor_por_piloto: bool = False,
) -> list[dict[str, int | float | str | None]]:
    """Retorna as voltas mais rápidas; pode restringir a uma por piloto.

    Descarta tempos nulos, não finitos, menores ou iguais a zero e pit-out laps.
    """
    if limite <= 0:
        return []

    mapa = {piloto.driver_number: piloto for piloto in pilotos}
    validas = [
        volta
        for volta in voltas
        if volta.lap_duration is not None
        and math.isfinite(volta.lap_duration)
        and volta.lap_duration > 0
        and volta.is_pit_out_lap is not True
    ]
    validas.sort(key=lambda volta: volta.lap_duration or float("inf"))

    resultado: list[dict[str, int | float | str | None]] = []
    numeros_utilizados: set[int] = set()
    for volta in validas:
        if apenas_melhor_por_piloto and volta.driver_number in numeros_utilizados:
            continue
        numeros_utilizados.add(volta.driver_number)
        piloto = mapa.get(volta.driver_number)
        nome = (
            piloto.full_name or piloto.name_acronym or f"Piloto #{volta.driver_number}"
            if piloto
            else f"Piloto #{volta.driver_number}"
        )
        duracao = float(volta.lap_duration)  # já filtrada acima
        resultado.append(
            {
                "Posição": len(resultado) + 1,
                "Piloto": nome,
                "Equipe": piloto.team_name or "Não informada" if piloto else "Não informada",
                "Número": volta.driver_number,
                "Volta": volta.lap_number,
                "Tempo": tempo_formatado(duracao),
                "Tempo (s)": round(duracao, 3),
            }
        )
        if len(resultado) >= limite:
            break
    return resultado
