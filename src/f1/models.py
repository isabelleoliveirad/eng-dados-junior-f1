"""Modelos para validar as respostas da API OpenF1."""

from pydantic import BaseModel, ConfigDict


class F1Model(BaseModel):
    model_config = ConfigDict(extra="ignore")


class Meeting(F1Model):
    meeting_key: int
    meeting_name: str
    year: int | None = None
    country_name: str | None = None
    date_start: str | None = None


class SessionInfo(F1Model):
    session_key: int
    session_name: str
    meeting_key: int | None = None
    date_start: str | None = None


class Driver(F1Model):
    driver_number: int
    full_name: str | None = None
    name_acronym: str | None = None
    team_name: str | None = None


class Lap(F1Model):
    driver_number: int
    lap_number: int | None = None
    lap_duration: float | None = None
    is_pit_out_lap: bool | None = None
