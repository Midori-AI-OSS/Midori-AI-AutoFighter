import logging

import pytest

from plugins.event_bus import EventBus


def test_emit_calls_subscribers() -> None:
    called = []

    def handler(arg: str) -> None:
        called.append(arg)

    bus = EventBus()
    bus.subscribe('ping', handler)
    bus.emit('ping', 'pong')
    assert called == ['pong']


def test_subscriber_errors_are_logged(caplog: pytest.LogCaptureFixture) -> None:
    def handler(_: str) -> None:
        raise RuntimeError('boom')

    bus = EventBus()
    bus.subscribe('boom', handler)
    with caplog.at_level(logging.ERROR):
        bus.emit('boom', 'x')
    assert 'boom' in caplog.text


def test_unsubscribe_stops_calls() -> None:
    called = False

    def handler() -> None:
        nonlocal called
        called = True

    bus = EventBus()
    bus.subscribe('once', handler)
    bus.unsubscribe('once', handler)
    bus.emit('once')
    assert not called

