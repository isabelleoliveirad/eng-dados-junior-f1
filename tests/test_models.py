import pytest
from pydantic import ValidationError

from f1.models import Driver, Lap, Meeting, SessionInfo


def test_models_aceitam_campos_adicionais():
    meeting = Meeting.model_validate({"meeting_key": 10, "meeting_name": "GP", "outro": "ignorado"})
    assert meeting.meeting_key == 10
    assert meeting.country_name is None


def test_campos_obrigatorios():
    with pytest.raises(ValidationError):
        Driver.model_validate({"full_name": "Sem número"})


def test_lap_null():
    assert Lap(driver_number=2, lap_duration=None).lap_duration is None


def test_session():
    assert SessionInfo(session_key=10, session_name="Race").session_name == "Race"
