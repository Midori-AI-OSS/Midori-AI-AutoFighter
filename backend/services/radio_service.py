from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime
from datetime import timezone
from http.client import HTTPResponse
import json
import re
import ssl
from typing import Any
from urllib import error as urllib_error
from urllib import parse as urllib_parse
from urllib import request as urllib_request

RADIO_BASE_URL = "https://radio.midori-ai.xyz"
RADIO_ENVELOPE_VERSION = "radio.v1"
_DEFAULT_CHANNEL = "all"
_ALLOWED_CHANNEL = re.compile(r"^[a-z0-9-]{1,40}$")
_ALLOWED_QUALITIES = {"low", "medium", "high"}
_JSON_TIMEOUT_SECONDS = 8.0
_IMAGE_TIMEOUT_SECONDS = 12.0
_MAX_JSON_BYTES = 1_000_000
_MAX_IMAGE_BYTES = 5_000_000


@dataclass(slots=True)
class UpstreamImage:
    body: bytes
    content_type: str
    status_code: int


class RadioServiceError(Exception):
    def __init__(self, message: str, *, status_code: int = 502, code: str = "RADIO_UPSTREAM_ERROR") -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code


class _NoRedirectHandler(urllib_request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        return None


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def normalize_channel(value: object) -> str:
    raw = str(value or "").strip().lower()
    if not raw or raw == _DEFAULT_CHANNEL:
        return _DEFAULT_CHANNEL
    if not _ALLOWED_CHANNEL.fullmatch(raw):
        return _DEFAULT_CHANNEL
    return raw


def normalize_quality(value: object) -> str:
    raw = str(value or "").strip().lower()
    if raw in _ALLOWED_QUALITIES:
        return raw
    return "medium"


def build_error_envelope(message: str, *, code: str, now: str | None = None) -> dict[str, Any]:
    return {
        "version": RADIO_ENVELOPE_VERSION,
        "ok": False,
        "now": now or _utc_now_iso(),
        "data": None,
        # Keep this as a string for httpClient normalizeError compatibility.
        "error": message,
        "code": code,
    }


def _read_with_limit(response: HTTPResponse, max_bytes: int) -> bytes:
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = response.read(64 * 1024)
        if not chunk:
            break
        total += len(chunk)
        if total > max_bytes:
            raise RadioServiceError(
                "Upstream response exceeded allowed size",
                status_code=502,
                code="RADIO_UPSTREAM_TOO_LARGE",
            )
        chunks.append(chunk)
    return b"".join(chunks)


def _build_url(path: str, *, channel: str | None = None) -> str:
    base = urllib_parse.urljoin(f"{RADIO_BASE_URL}/", path.lstrip("/"))
    if channel is None:
        return base
    query = urllib_parse.urlencode({"channel": normalize_channel(channel)})
    return f"{base}?{query}"


def _open_url(url: str, *, timeout: float) -> tuple[int, dict[str, str], bytes]:
    request = urllib_request.Request(url, headers={"Accept": "application/json", "User-Agent": "sgo-endless-radio-proxy"})
    ssl_context = ssl.create_default_context()
    opener = urllib_request.build_opener(_NoRedirectHandler(), urllib_request.HTTPSHandler(context=ssl_context))

    try:
        with opener.open(request, timeout=timeout) as response:
            headers = {key.lower(): value for key, value in response.headers.items()}
            body = _read_with_limit(response, _MAX_JSON_BYTES)
            return int(response.status), headers, body
    except urllib_error.HTTPError as exc:
        body = _read_with_limit(exc, _MAX_JSON_BYTES)
        headers = {key.lower(): value for key, value in (exc.headers.items() if exc.headers else [])}
        return int(exc.code), headers, body
    except urllib_error.URLError as exc:
        raise RadioServiceError(
            f"Radio upstream unreachable: {exc.reason}",
            status_code=502,
            code="RADIO_UPSTREAM_UNREACHABLE",
        ) from exc
    except TimeoutError as exc:
        raise RadioServiceError(
            "Radio upstream request timed out",
            status_code=504,
            code="RADIO_UPSTREAM_TIMEOUT",
        ) from exc


def _parse_envelope(body: bytes, *, endpoint: str) -> dict[str, Any]:
    try:
        payload = json.loads(body.decode("utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise RadioServiceError(
            f"Invalid JSON from radio upstream ({endpoint})",
            status_code=502,
            code="RADIO_INVALID_JSON",
        ) from exc

    if not isinstance(payload, dict):
        raise RadioServiceError(
            f"Invalid radio envelope from upstream ({endpoint})",
            status_code=502,
            code="RADIO_INVALID_ENVELOPE",
        )

    if payload.get("version") != RADIO_ENVELOPE_VERSION:
        raise RadioServiceError(
            f"Unsupported radio API version: {payload.get('version')}",
            status_code=502,
            code="RADIO_UNSUPPORTED_VERSION",
        )

    return payload


def _normalize_error_field(payload: dict[str, Any]) -> dict[str, Any]:
    cloned = dict(payload)
    err = cloned.get("error")
    if isinstance(err, dict):
        message = str(err.get("message") or "Radio request failed")
        code = str(err.get("code") or cloned.get("code") or "RADIO_UPSTREAM_ERROR")
        cloned["error"] = message
        cloned["code"] = code
    elif err is None:
        cloned["error"] = None
    else:
        cloned["error"] = str(err)
    return cloned


def _validate_upstream_host(raw_url: str) -> str:
    parsed = urllib_parse.urlparse(raw_url)
    if parsed.scheme != "https" or parsed.netloc != "radio.midori-ai.xyz":
        raise RadioServiceError(
            "Invalid upstream host in art URL",
            status_code=502,
            code="RADIO_INVALID_ART_URL",
        )
    return raw_url


async def fetch_channels() -> tuple[int, dict[str, Any]]:
    return await fetch_json_endpoint("/radio/v1/channels")


async def fetch_current(*, channel: str) -> tuple[int, dict[str, Any]]:
    return await fetch_json_endpoint("/radio/v1/current", channel=channel)


async def fetch_art(*, channel: str, same_origin_prefix: str = "/api") -> tuple[int, dict[str, Any]]:
    status, payload = await fetch_json_endpoint("/radio/v1/art", channel=channel)
    normalized_payload = dict(payload)
    data = normalized_payload.get("data")
    if isinstance(data, dict):
        data = dict(data)
        upstream_art = str(data.get("art_url") or "").strip()
        if upstream_art:
            absolute = upstream_art
            if upstream_art.startswith("/"):
                absolute = f"{RADIO_BASE_URL}{upstream_art}"
            _validate_upstream_host(absolute)
        data["art_url"] = f"{same_origin_prefix}/radio/art/image?channel={urllib_parse.quote(normalize_channel(channel), safe='')}"
        normalized_payload["data"] = data
    return status, normalized_payload


async def fetch_art_image(*, channel: str) -> UpstreamImage:
    return await asyncio.to_thread(_fetch_art_image_sync, normalize_channel(channel))


def _fetch_art_image_sync(channel: str) -> UpstreamImage:
    url = _build_url("/radio/v1/art/image", channel=channel)
    request = urllib_request.Request(url, headers={"Accept": "image/*", "User-Agent": "sgo-endless-radio-proxy"})
    ssl_context = ssl.create_default_context()
    opener = urllib_request.build_opener(_NoRedirectHandler(), urllib_request.HTTPSHandler(context=ssl_context))

    try:
        with opener.open(request, timeout=_IMAGE_TIMEOUT_SECONDS) as response:
            content_type = str(response.headers.get("Content-Type") or "image/jpeg")
            body = _read_with_limit(response, _MAX_IMAGE_BYTES)
            return UpstreamImage(body=body, content_type=content_type, status_code=int(response.status))
    except urllib_error.HTTPError as exc:
        message = f"Radio art image request failed with status {exc.code}"
        raise RadioServiceError(
            message,
            status_code=int(exc.code),
            code="RADIO_ART_IMAGE_HTTP_ERROR",
        ) from exc
    except urllib_error.URLError as exc:
        raise RadioServiceError(
            f"Radio art image unreachable: {exc.reason}",
            status_code=502,
            code="RADIO_ART_IMAGE_UNREACHABLE",
        ) from exc
    except TimeoutError as exc:
        raise RadioServiceError(
            "Radio art image request timed out",
            status_code=504,
            code="RADIO_ART_IMAGE_TIMEOUT",
        ) from exc


async def fetch_json_endpoint(path: str, *, channel: str | None = None) -> tuple[int, dict[str, Any]]:
    return await asyncio.to_thread(_fetch_json_endpoint_sync, path, channel)


def _fetch_json_endpoint_sync(path: str, channel: str | None) -> tuple[int, dict[str, Any]]:
    url = _build_url(path, channel=channel)
    status, _headers, body = _open_url(url, timeout=_JSON_TIMEOUT_SECONDS)
    payload = _parse_envelope(body, endpoint=path)
    normalized_payload = _normalize_error_field(payload)
    return status, normalized_payload
