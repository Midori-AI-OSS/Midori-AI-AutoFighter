from __future__ import annotations

from quart import Blueprint
from quart import Response
from quart import jsonify
from quart import request
from services.radio_service import RadioServiceError
from services.radio_service import build_error_envelope
from services.radio_service import fetch_art
from services.radio_service import fetch_art_image
from services.radio_service import fetch_channels
from services.radio_service import fetch_current
from services.radio_service import normalize_channel

bp = Blueprint("radio", __name__, url_prefix="/radio")


def _error_response(exc: RadioServiceError):
    payload = build_error_envelope(exc.message, code=exc.code)
    return jsonify(payload), exc.status_code


@bp.get("/channels")
async def radio_channels():
    try:
        status_code, payload = await fetch_channels()
        return jsonify(payload), status_code
    except RadioServiceError as exc:
        return _error_response(exc)


@bp.get("/current")
async def radio_current():
    channel = normalize_channel(request.args.get("channel"))
    try:
        status_code, payload = await fetch_current(channel=channel)
        return jsonify(payload), status_code
    except RadioServiceError as exc:
        return _error_response(exc)


@bp.get("/art")
async def radio_art():
    channel = normalize_channel(request.args.get("channel"))
    try:
        status_code, payload = await fetch_art(channel=channel)
        return jsonify(payload), status_code
    except RadioServiceError as exc:
        return _error_response(exc)


@bp.get("/art/image")
async def radio_art_image():
    channel = normalize_channel(request.args.get("channel"))
    try:
        image = await fetch_art_image(channel=channel)
    except RadioServiceError as exc:
        return _error_response(exc)

    return Response(
        image.body,
        status=image.status_code,
        headers={
            "Content-Type": image.content_type,
            "Cache-Control": "no-store, no-cache, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        },
    )
