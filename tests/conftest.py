from __future__ import annotations

import json
from pathlib import Path
from collections.abc import Callable
from typing import Any

import pytest


FIXTURE_ROOT = Path(__file__).parent / "fixtures"


def load_json_fixture(relative_path: str) -> Any:
    fixture_path = FIXTURE_ROOT / relative_path
    with fixture_path.open(encoding="utf-8") as fixture_file:
        return json.load(fixture_file)


@pytest.fixture
def fixture_json() -> Callable[[str], Any]:
    return load_json_fixture
