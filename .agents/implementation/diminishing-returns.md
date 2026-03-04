# Diminishing Returns System

The diminishing returns system ensures that buffs become less effective as a character's stats get higher, preventing exponential power scaling and maintaining game balance.

## Overview

When any stat buff is applied (through `create_stat_buff()` or `StatModifier`), the buff value is automatically scaled based on the character's current stat level. Higher stats result in dramatically reduced buff effectiveness.

## Scaling Rules

### HP Scaling
- **Threshold**: Every 500 HP
- **Scaling Factor**: 4x reduction per threshold
- **Examples**:
  - 400 HP: 100% buff effectiveness  
  - 500 HP: 25% buff effectiveness (4x reduction)
  - 1000 HP: 6.25% buff effectiveness (16x reduction)
  - 1500 HP: 1.56% buff effectiveness (64x reduction)

### ATK/DEF Scaling
- **Threshold**: Every 100 points
- **Scaling Factor**: 100x reduction per threshold
- **Examples**:
  - 50 ATK: 100% buff effectiveness
  - 100 ATK: 1% buff effectiveness (100x reduction)
  - 200 ATK: 0.01% buff effectiveness (10,000x reduction)
  - 300 ATK: 0.0001% buff effectiveness (1,000,000x reduction)

### Percentage Stats (Crit Rate, Mitigation, Vitality)
- **Base Threshold**: 2% (no scaling below this)
- **Threshold**: Every 1% above base
- **Scaling Factor**: 100x reduction per threshold
- **Examples**:
  - 2% crit rate: 100% buff effectiveness
  - 3% crit rate: 1% buff effectiveness (100x reduction)
  - 4% crit rate: 0.01% buff effectiveness (10,000x reduction)

### Crit Damage Scaling
- **Base Threshold**: 200% (2.0 multiplier)
- **Threshold**: Every 500% above base
- **Scaling Factor**: 1000x reduction per threshold
- **Examples**:
  - 200% crit damage: 100% buff effectiveness
  - 700% crit damage: 0.1% buff effectiveness (1000x reduction)
  - 1200% crit damage: 0.0001% buff effectiveness (1,000,000x reduction)

## Implementation Details

### Automatic Application
- All stat modifiers are automatically scaled when applied
- Affects both additive deltas (`atk=50`) and multiplicative changes (`atk_mult=1.5`)
- Applied to both positive buffs and negative debuffs
- No changes required to existing code using `create_stat_buff()`

### Numerical Safety
- Minimum effectiveness: 0.0001% (1e-6) to prevent zero effects
- Maximum effectiveness: 100% (1.0) 
- Handles floating point precision issues with epsilon correction
- Prevents overflow/underflow with safe arithmetic

### Configuration
Located in `backend/autofighter/effects.py`:
```python
DIMINISHING_RETURNS_CONFIG = {
    'max_hp': {'threshold': 500, 'scaling_factor': 4.0, 'base_offset': 0},
    'atk': {'threshold': 100, 'scaling_factor': 100.0, 'base_offset': 0},
    'defense': {'threshold': 100, 'scaling_factor': 100.0, 'base_offset': 0},
    'crit_rate': {'threshold': 0.01, 'scaling_factor': 100.0, 'base_offset': 0.02},
    # ... etc
}
```

## Balance Considerations

⚠️ **Warning**: The current scaling factors are quite aggressive and may need adjustment based on gameplay testing:

- **HP**: 4x per 500 might be too steep for tank builds
- **ATK/DEF**: 100x per 100 makes high-stat builds nearly unbuffable
- **Percentage stats**: 100x scaling creates hard caps around 3-4%

### Recommended Tuning Areas
1. **Reduce scaling factors** (e.g., 2x instead of 4x for HP)
2. **Increase thresholds** (e.g., every 1000 HP instead of 500)
3. **Add stat-specific configurations** for different playstyles
4. **Consider diminishing returns curves** instead of step functions

## Testing

Comprehensive test suite in `backend/tests/test_diminishing_returns.py`:
- Unit tests for calculation logic
- Integration tests with actual buffs
- Edge case testing (negatives, zeros, extremes)
- Manual validation examples

Run tests: `uv run pytest tests/test_diminishing_returns.py -v`

## Example Usage

```python
from autofighter.stats import Stats
from autofighter.effects import create_stat_buff

# Low-level character gets full effectiveness
char = Stats()
char.set_base_stat('max_hp', 400)
create_stat_buff(char, max_hp=100)  # Gets full +100 HP

# High-level character gets reduced effectiveness  
high_char = Stats()
high_char.set_base_stat('max_hp', 1500) 
create_stat_buff(high_char, max_hp=100)  # Gets only ~1.6 HP
```

The system automatically scales all buffs without requiring any changes to existing buff creation code.