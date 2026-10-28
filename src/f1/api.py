"""Cliente HTTP simples e testável para a API OpenF1."""

import logging

import requests
from pydantic import BaseModel, ValidationError
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from f1.models import Driver, Lap, Meeting, SessionInfo

BASE_URL = "https://api.openf1.org/v1"
LOG = logging.getLogger(__name__)


class APIError(Exception):
    """Falha de rede, HTTP ou formato inesperado da API."""


class OpenF1Client:
    def __init__(
        self,
        session: requests.Session | None = None,
        base_url: str = BASE_URL,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        if session is not None:
            self.session = session
        else:
            self.session = requests.Session()
            retries = Retry(
                total=2,
                backoff_factor=1,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=["GET"],
                respect_retry_after_header=True,
            )
            adapter = HTTPAdapter(max_retries=retries)
            self.session.mount("https://", adapter)
            self.session.mount("http://", adapter)

    def _get[ModelT: BaseModel](self, endpoint: str, model: type[ModelT], **params: int) -> list[ModelT]:
        try:
            response = self.session.get(
                f"{self.base_url}/{endpoint}",
                params=params,
                timeout=25,
            )
            response.raise_for_status()
            payload = response.json()
        except (requests.RequestException, ValueError) as exc:
            raise APIError(f"Falha ao consultar '{endpoint}': {exc}") from exc

        if not isinstance(payload, list):
            raise APIError(f"Resposta inesperada em '{endpoint}': esperada lista JSON")

        result: list[ModelT] = []
        for entry in payload:
            try:
                result.append(model.model_validate(entry))
            except ValidationError:
                LOG.warning("Ignorando item inválido em %s", endpoint)
        return result

    def meetings(self, year: int) -> list[Meeting]:
        return self._get("meetings", Meeting, year=year)

    def sessions(self, meeting_key: int) -> list[SessionInfo]:
        return self._get("sessions", SessionInfo, meeting_key=meeting_key)

    def drivers(self, session_key: int) -> list[Driver]:
        return self._get("drivers", Driver, session_key=session_key)

    def laps(self, session_key: int) -> list[Lap]:
        return self._get("laps", Lap, session_key=session_key)
