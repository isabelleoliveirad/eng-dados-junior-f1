"""Ponto de entrada para Streamlit Community Cloud."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from f1.dashboard import main  # noqa: E402

if __name__ == "__main__":
    main()
