import builtins
import importlib.util
from pathlib import Path

import pytest


@pytest.fixture()
def lrm_app(tmp_path, monkeypatch):
    db_path = tmp_path / "save.db"
    monkeypatch.setenv("AF_DB_PATH", str(db_path))
    monkeypatch.setenv("AF_DB_KEY", "testkey")

    original_import = builtins.__import__

    def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "torch":
            raise ImportError("No module named 'torch'")
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", fake_import)
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
async def test_get_lrm_config_defaults(lrm_app):
    client = lrm_app.test_client()
    resp = await client.get("/config/lrm")

    assert resp.status_code == 200
    data = await resp.get_json()
    assert data["provider"] == "disabled"
    assert data["enabled"] is False
    assert "codex_cli" in data["providers"]


@pytest.mark.asyncio
async def test_update_lrm_config_persists_values(lrm_app):
    client = lrm_app.test_client()

    update_resp = await client.post(
        "/config/lrm",
        json={
            "provider": "codex_cli",
            "model": "openai/gpt-oss-20b",
            "reasoning_effort": "medium",
            "summary": "concise",
        },
    )
    assert update_resp.status_code == 200

    get_resp = await client.get("/config/lrm")
    assert get_resp.status_code == 200
    data = await get_resp.get_json()
    assert data["provider"] == "codex_cli"
    assert data["model"] == "openai/gpt-oss-20b"
    assert data["reasoning_effort"] == "medium"
    assert data["summary"] == "concise"


@pytest.mark.asyncio
async def test_update_lrm_config_validates_provider(lrm_app):
    client = lrm_app.test_client()
    resp = await client.post("/config/lrm", json={"provider": "unsupported"})

    assert resp.status_code == 400
    data = await resp.get_json()
    assert "provider" in data["error"]


@pytest.mark.asyncio
async def test_lrm_test_requires_prompt(lrm_app):
    client = lrm_app.test_client()
    resp = await client.post("/config/lrm/test", json={})

    assert resp.status_code == 400
    data = await resp.get_json()
    assert data["error"] == "prompt is required"


@pytest.mark.asyncio
async def test_lrm_test_uses_mocked_codex_runner(lrm_app, monkeypatch):
    from services import lrm_service

    async def fake_run(prompt: str, *, config: lrm_service.LRMConfig, timeout_seconds=None):
        assert prompt == "hello"
        assert config.provider == "codex_cli"
        return lrm_service.LRMExecutionResult(
            ok=True,
            response_text="mocked reply",
            error=None,
            exit_code=0,
            latency_ms=7,
            provider=config.provider,
            model=config.model,
        )

    monkeypatch.setattr(lrm_service, "run_codex_prompt", fake_run)

    client = lrm_app.test_client()
    set_resp = await client.post(
        "/config/lrm",
        json={
            "provider": "codex_cli",
            "model": "openai/gpt-oss-120b",
        },
    )
    assert set_resp.status_code == 200

    test_resp = await client.post("/config/lrm/test", json={"prompt": "hello"})
    assert test_resp.status_code == 200
    payload = await test_resp.get_json()
    assert payload["ok"] is True
    assert payload["response"] == "mocked reply"
    assert payload["error"] is None
