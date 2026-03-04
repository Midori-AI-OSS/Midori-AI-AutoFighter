from __future__ import annotations

import math

from options import OptionKey
from options import get_option
from options import set_option
from quart import Blueprint
from quart import jsonify
from quart import request
from tracking import log_menu_action
from tracking import log_overlay_action
from tracking import log_settings_change

from autofighter.rooms.battle.pacing import refresh_turn_pacing
from autofighter.rooms.battle.pacing import set_turn_pacing

bp = Blueprint("config", __name__, url_prefix="/config")

_TURN_PACING_DEFAULT = 0.5

# Future Codex CLI reference:
# OPENAI_BASE_URL="$base_url" \
# OPENAI_API_KEY="$api_key" \
# codex exec \
#   "$prompt" \
#   --skip-git-repo-check \
#   --sandbox read-only \
#   --disable enable_request_compression \
#   --config 'model_reasoning_effort="high"' \
#   -m openai/gpt-oss-120b \
#   -o "$output_file" \
#   > /dev/null \
#   2> "$stderr_file"


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
