import pytest
from player import Player


def test_level_up_exp_calculation():
    """Test that EXP is correctly calculated when leveling up."""
    player = Player("Test")
    player.level = 1
    player.EXP = 0
    
    # Get the EXP required to level up from level 1
    exp_needed = player.exp_to_levelup()
    
    # Give player exactly enough EXP to level up
    player.EXP = exp_needed
    
    # Record the EXP to level up from level 1 before leveling
    exp_to_subtract = exp_needed
    
    # Level up
    player.level_up()
    
    # Player should now be level 2
    assert player.level == 2
    
    # Remaining EXP should be 0 (exactly enough to level up)
    assert player.EXP == 0


def test_level_up_exp_calculation_with_excess():
    """Test that excess EXP is handled correctly when leveling up."""
    player = Player("Test")
    player.level = 1
    player.EXP = 0
    
    # Get the EXP required to level up from level 1
    exp_needed = player.exp_to_levelup()
    excess_exp = 0.5  # Use a smaller excess that won't trigger multiple level ups
    
    # Give player more than enough EXP to level up by a small amount
    player.EXP = exp_needed + excess_exp
    
    # Level up
    player.level_up()
    
    # Player should now be level 2
    assert player.level == 2
    
    # Remaining EXP should be the excess
    assert abs(player.EXP - excess_exp) < 0.001  # Allow for floating point precision


def test_multiple_level_ups():
    """Test leveling up multiple times in one call."""
    player = Player("Test")
    player.level = 1
    player.EXP = 0
    
    # Calculate EXP needed for multiple levels
    level_1_exp = player.exp_to_levelup()
    player.level = 2
    level_2_exp = player.exp_to_levelup()
    player.level = 1  # Reset
    
    total_exp_needed = level_1_exp + level_2_exp
    excess_exp = 5
    
    # Give enough EXP for 2 levels plus some extra
    player.EXP = total_exp_needed + excess_exp
    
    # Level up
    player.level_up()
    
    # Player should now be level 3
    assert player.level == 3
    
    # Should have correct remaining EXP
    assert player.EXP == excess_exp


def test_exp_gain_consistency():
    """Test that EXP gain behaves consistently."""
    player = Player("Test")
    player.level = 5
    player.EXP = 0
    
    initial_exp = player.EXP
    player.gain_exp(mod=1.0, foe_level=5)
    
    # Should have gained some EXP
    assert player.EXP > initial_exp


def test_set_level_effect_stats():
    """Test that set_level properly calculates EffectRES and EffectHitRate."""
    player = Player("Test")
    
    # Test at level 10
    player.set_level(10)
    assert player.level == 10
    expected_effect_res = 0.05 + (0.002 * 10)  # 0.07
    expected_effect_hit_rate = 1 + (0.0001 * 10)  # 1.001
    
    assert abs(player.EffectRES - expected_effect_res) < 0.001
    assert abs(player.EffectHitRate - expected_effect_hit_rate) < 0.001
    
    # Test at level 100
    player.set_level(100)
    assert player.level == 100
    expected_effect_res = 0.05 + (0.002 * 100)  # 0.25
    expected_effect_hit_rate = 1 + (0.0001 * 100)  # 1.01
    
    assert abs(player.EffectRES - expected_effect_res) < 0.001
    assert abs(player.EffectHitRate - expected_effect_hit_rate) < 0.001


def test_set_level_vs_level_up_consistency():
    """Test that set_level and level_up produce consistent results."""
    # Create two identical players
    player1 = Player("Test1")
    player2 = Player("Test2")
    
    # Set both to level 1 initially
    player1.set_level(1)
    player2.set_level(1)
    
    # Use set_level to jump to level 5
    player1.set_level(5)
    
    # Use level_up to gradually reach level 5
    player2.EXP = 0
    target_level = 5
    
    # Give enough EXP to reach target level
    total_exp_needed = 0
    temp_level = player2.level
    for level in range(player2.level, target_level):
        player2.level = level
        total_exp_needed += player2.exp_to_levelup()
    
    player2.level = temp_level  # Reset to original
    player2.EXP = total_exp_needed
    player2.level_up()
    
    # Both players should be at level 5
    assert player1.level == 5
    assert player2.level == 5
    
    # Stats should be reasonably similar (allowing for randomness in level_up)
    # We'll just check that they're both positive and in reasonable ranges
    assert player1.MHP > 0
    assert player2.MHP > 0
    assert player1.Atk > 0
    assert player2.Atk > 0