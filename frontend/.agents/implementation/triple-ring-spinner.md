# TripleRingSpinner Component

Renders three concentric rings with element-colored dots. Each dot orbits its ring using the `spin` animation while the rings
pulse with `pulse`. The middle ring's dot rotates in the opposite direction to the inner and outer rings. Animation timing is
configurable via the `duration` prop and defaults to theme variables. The component also accepts a `color` prop for customizing
the ring and dot color and respects the `reducedMotion` flag to disable animations when necessary. Width and height default to
`clamp(14px, calc(var(--portrait-size, 96px) * 0.18), 32px)` and can be overridden via the `--spinner-size` custom property.
