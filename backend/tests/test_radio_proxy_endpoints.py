from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
from unittest.mock import patch

import pytest
from services import radio_service
from services.radio_service import RadioServiceError
from services.radio_service import UpstreamImage


@pytest.fixture()
def app_with_db(tmp_path, monkeypatch):
    db_path = tmp_path / "save.db"
    monkeypatch.setenv("AF_DB_PATH", str(db_path))
    monkeypatch.setenv("AF_DB_KEY", "testkey")
    monkeypatch.setenv("UV_EXTRA", "test")
    if "app" in sys.modules:
        del sys.modules["app"]
    monkeypatch.syspath_prepend(Path(__file__).resolve().parents[1])
    spec = importlib.util.spec_from_file_location(
        "app", Path(__file__).resolve().parents[1] / "app.py",
    )
    app_module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(app_module)
    app_module.app.testing = True
    return app_module.app


@pytest.mark.asyncio
async def test_radio_channels_success(app_with_db):
    app = app_with_db
    client = app.test_client()

    payload = {
        "version": "radio.v1",
        "ok": True,
        "now": "2026-03-05T00:00:00.000Z",
        "data": {"channels": [{"name": "all", "track_count": 10}]},
        "error": None,
    }

    async def fake_fetch_channels():
        return 200, payload

    with patch("routes.radio.fetch_channels", fake_fetch_channels):
        response = await client.get("/radio/channels")

    assert response.status_code == 200
    body = await response.get_json()
    assert body == payload


@pytest.mark.asyncio
async def test_radio_current_normalizes_channel(app_with_db):
    app = app_with_db
    client = app.test_client()

    captured: dict[str, str] = {}

    async def fake_fetch_current(*, channel: str):
        captured["channel"] = channel
        return 200, {
            "version": "radio.v1",
            "ok": True,
            "now": "2026-03-05T00:00:00.000Z",
            "data": {"channel": channel, "title": "Song"},
            "error": None,
        }

    with patch("routes.radio.fetch_current", fake_fetch_current):
        response = await client.get("/radio/current?channel=http://evil.example")

    assert response.status_code == 200
    assert captured["channel"] == "all"


@pytest.mark.asyncio
async def test_radio_art_image_success(app_with_db):
    app = app_with_db
    client = app.test_client()

    async def fake_fetch_art_image(*, channel: str):
        assert channel == "all"
        return UpstreamImage(body=b"img", content_type="image/jpeg", status_code=200)

    with patch("routes.radio.fetch_art_image", fake_fetch_art_image):
        response = await client.get("/radio/art/image?channel=all")

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("image/jpeg")
    assert response.headers["Cache-Control"] == "no-store, no-cache, must-revalidate"
    assert response.headers["Pragma"] == "no-cache"
    assert response.headers["Expires"] == "0"
    assert await response.get_data() == b"img"


@pytest.mark.asyncio
async def test_radio_routes_map_service_errors(app_with_db):
    app = app_with_db
    client = app.test_client()

    async def fake_fetch_art(*, channel: str):
        raise RadioServiceError("upstream failed", status_code=502, code="RADIO_UPSTREAM_UNREACHABLE")

    with patch("routes.radio.fetch_art", fake_fetch_art):
        response = await client.get("/radio/art?channel=all")

    assert response.status_code == 502
    body = await response.get_json()
    assert body["ok"] is False
    assert body["error"] == "upstream failed"
    assert body["code"] == "RADIO_UPSTREAM_UNREACHABLE"


def test_normalize_channel_hardening():
    assert radio_service.normalize_channel("") == "all"
    assert radio_service.normalize_channel("all") == "all"
    assert radio_service.normalize_channel("lunar-mix") == "lunar-mix"
    assert radio_service.normalize_channel("HTTP://evil") == "all"
    assert radio_service.normalize_channel("../../etc/passwd") == "all"


@pytest.mark.asyncio
async def test_fetch_art_rewrites_same_origin_url(monkeypatch):
    async def fake_fetch_json_endpoint(path: str, *, channel: str | None = None):
        assert path == "/radio/v1/art"
        assert channel == "all"
        return 200, {
            "version": "radio.v1",
            "ok": True,
            "now": "2026-03-05T00:00:00.000Z",
            "data": {
                "channel": "all",
                "track_id": "id",
                "has_art": True,
                "mime": "image/jpeg",
                "art_url": "/radio/v1/art/image?channel=all",
            },
            "error": None,
        }

    monkeypatch.setattr(radio_service, "fetch_json_endpoint", fake_fetch_json_endpoint)

    status, payload = await radio_service.fetch_art(channel="all")

    assert status == 200
    assert payload["data"]["art_url"] == "/api/radio/art/image?channel=all"


@pytest.mark.asyncio
async def test_fetch_art_rejects_invalid_upstream_art_host(monkeypatch):
    async def fake_fetch_json_endpoint(path: str, *, channel: str | None = None):
        return 200, {
            "version": "radio.v1",
            "ok": True,
            "now": "2026-03-05T00:00:00.000Z",
            "data": {
                "channel": "all",
                "track_id": "id",
                "has_art": True,
                "mime": "image/jpeg",
                "art_url": "https://example.com/malicious.jpg",
            },
            "error": None,
        }

    monkeypatch.setattr(radio_service, "fetch_json_endpoint", fake_fetch_json_endpoint)

    with pytest.raises(RadioServiceError):
        await radio_service.fetch_art(channel="all")
