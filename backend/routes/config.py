from __future__ import annotations

import math

from options import OptionKey
from options import get_option
from options import set_option
from quart import Blueprint
from quart import jsonify
from quart import request
from services import lrm_service
from tracking import log_menu_action
from tracking import log_overlay_action
from tracking import log_settings_change

from autofighter.rooms.battle.pacing import refresh_turn_pacing
from autofighter.rooms.battle.pacing import set_turn_pacing

bp = Blueprint("config", __name__, url_prefix="/config")

_TURN_PACING_DEFAULT = 0.5

@bp.get("/turn_pacing")
async def get_turn_pacing() -> tuple[str, int, dict[str, float]]:
    """Get current battle turn pacing configuration.

    Returns:
        JSON response with:
        - turn_pacing: Current pacing value (seconds between turns)
        - default: Default pacing value
    """
    value = refresh_turn_pacing()
    payload = {"turn_pacing": value, "default": _TURN_PACING_DEFAULT}
    try:
        await log_menu_action("Settings", "view_turn_pacing", {"value": value})
        await log_overlay_action("settings", {"section": "turn_pacing"})
    except Exception:
        pass
    return jsonify(payload)


@bp.post("/turn_pacing")
async def update_turn_pacing() -> tuple[str, int, dict[str, float]]:
    """Update battle turn pacing configuration.

    Request body should contain:
        turn_pacing: New pacing value in seconds (must be >= 0)

    Returns:
        JSON response with updated turn_pacing value.

    Raises:
        400: If turn_pacing missing or invalid.
    """
    data = await request.get_json()
    if not isinstance(data, dict) or "turn_pacing" not in data:
        return jsonify({"error": "turn_pacing is required"}), 400

    try:
        requested = float(data["turn_pacing"])
    except (TypeError, ValueError):
        return jsonify({"error": "turn_pacing must be numeric"}), 400

    if not math.isfinite(requested):
        return jsonify({"error": "turn_pacing must be finite"}), 400

    if requested <= 0:
        return jsonify({"error": "turn_pacing must be positive"}), 400

    old = await get_option(OptionKey.TURN_PACING, f"{_TURN_PACING_DEFAULT}")
    value = set_turn_pacing(requested)
    await set_option(OptionKey.TURN_PACING, f"{value}")
    try:
        await log_settings_change("turn_pacing", old, value)
        await log_menu_action("Settings", "update_turn_pacing", {"old": old, "new": value})
    except Exception:
        pass
    return jsonify({"turn_pacing": value, "default": _TURN_PACING_DEFAULT})


@bp.get("/concise_descriptions")
async def get_concise_descriptions() -> tuple[str, int, dict[str, bool]]:
    """Get current concise descriptions setting.

    Returns:
        JSON response with:
        - enabled: Whether concise descriptions are enabled (boolean)
    """
    value = await get_option(OptionKey.CONCISE_DESCRIPTIONS, "false")
    enabled = value.lower() == "true"
    payload = {"enabled": enabled}
    try:
        await log_menu_action("Settings", "view_concise_descriptions", {"enabled": enabled})
        await log_overlay_action("settings", {"section": "concise_descriptions"})
    except Exception:
        pass
    return jsonify(payload)


@bp.post("/concise_descriptions")
async def update_concise_descriptions() -> tuple[str, int, dict[str, bool]]:
    """Update concise descriptions setting.

    Request body should contain:
        enabled: Boolean flag to enable/disable concise descriptions

    Returns:
        JSON response with updated enabled value.

    Raises:
        400: If enabled field is missing or not boolean.
    """
    data = await request.get_json()
    if not isinstance(data, dict) or "enabled" not in data:
        return jsonify({"error": "enabled is required"}), 400

    enabled = bool(data["enabled"])
    old = await get_option(OptionKey.CONCISE_DESCRIPTIONS, "false")
    await set_option(OptionKey.CONCISE_DESCRIPTIONS, "true" if enabled else "false")
    try:
        await log_settings_change("concise_descriptions", old, enabled)
        await log_menu_action("Settings", "update_concise_descriptions", {"old": old, "new": enabled})
    except Exception:
        pass
    return jsonify({"enabled": enabled})


@bp.get("/lrm")
async def get_lrm_config() -> tuple[str, int, dict[str, object]]:
    """Get current LRM provider configuration."""
    config = await lrm_service.get_lrm_config()
    return jsonify(lrm_service.serialise_lrm_config(config))


@bp.post("/lrm")
async def update_lrm_config() -> tuple[str, int, dict[str, object]]:
    """Update and persist LRM provider configuration."""
    data = await request.get_json()
    if data is None:
        data = {}
    if not isinstance(data, dict):
        return jsonify({"error": "request body must be a JSON object"}), 400

    previous = await lrm_service.get_lrm_config()
    try:
        updated = await lrm_service.save_lrm_config(
            provider=data.get("provider"),
            model=data.get("model"),
            reasoning_effort=data.get("reasoning_effort"),
            summary=data.get("summary"),
        )
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    try:
        if previous.provider != updated.provider:
            await log_settings_change("lrm_provider", previous.provider, updated.provider)
        if previous.model != updated.model:
            await log_settings_change("lrm_model", previous.model, updated.model)
        if previous.reasoning_effort != updated.reasoning_effort:
            await log_settings_change(
                "lrm_reasoning_effort",
                previous.reasoning_effort,
                updated.reasoning_effort,
            )
        if previous.summary != updated.summary:
            await log_settings_change("lrm_summary", previous.summary, updated.summary)
        await log_menu_action(
            "Settings",
            "update_lrm_config",
            {
                "provider": updated.provider,
                "model": updated.model,
                "reasoning_effort": updated.reasoning_effort,
                "summary": updated.summary,
            },
        )
    except Exception:
        pass

    return jsonify(lrm_service.serialise_lrm_config(updated))


@bp.post("/lrm/test")
async def test_lrm_config() -> tuple[str, int, dict[str, object]]:
    """Probe LRM config with a one-shot prompt using Codex CLI."""
    data = await request.get_json()
    if not isinstance(data, dict):
        return jsonify({"error": "request body must be a JSON object"}), 400

    prompt_raw = data.get("prompt")
    prompt = str(prompt_raw).strip() if prompt_raw is not None else ""
    if not prompt:
        return jsonify({"error": "prompt is required"}), 400

    current = await lrm_service.get_lrm_config()
    try:
        effective = lrm_service.build_lrm_config(
            provider=data.get("provider", current.provider),
            model=data.get("model", current.model),
            reasoning_effort=data.get("reasoning_effort", current.reasoning_effort),
            summary=data.get("summary", current.summary),
        )
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    if effective.provider != lrm_service.PROVIDER_CODEX_CLI:
        return jsonify({"error": "provider must be 'codex_cli' to run test"}), 400

    result = await lrm_service.run_codex_prompt(prompt, config=effective)
    payload: dict[str, object] = {
        "ok": result.ok,
        "provider": result.provider,
        "model": result.model,
        "latency_ms": result.latency_ms,
        "exit_code": result.exit_code,
        "error": result.error,
        "response": result.response_text,
    }
    if result.ok:
        return jsonify(payload)
    return jsonify(payload), 503
