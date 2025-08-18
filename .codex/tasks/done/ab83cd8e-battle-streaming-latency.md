# Reduce battle streaming latency (`ab83cd8e`)

## Summary
Battle snapshots arrive with noticeable delay, making combat feel sluggish.

## Tasks
- [x] Investigate backend snapshot endpoint for bottlenecks.
- [x] Lower or dynamically adjust `BattleView` polling interval; explore WebSocket/SSE for real-time updates.
- [x] Display a stained-glass panel with a spinner and status text to the right of the top-left nav bar, fading in while snapshots load and fading out once they complete.
- [x] Add performance logs to monitor round-trip times during fights.

## Context
Players report battle state updates lagging behind actions, degrading responsiveness.

Status: Need Review
