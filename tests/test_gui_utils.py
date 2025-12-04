"""
Tests for GUI utility functions.

Tests color mapping, validation, and helper functions.
"""
import pytest
from mastermind import Rules
from mastermind.gui import utils


def test_colors_to_symbols():
    """Test converting colors to symbols."""
    colors = ["Red", "Green", "Blue", "Yellow"]
    symbols = utils.colors_to_symbols(colors)
    assert symbols == "0213"


def test_colors_to_symbols_single():
    """Test converting single color."""
    colors = ["Red"]
    symbols = utils.colors_to_symbols(colors)
    assert symbols == "0"


def test_symbols_to_colors():
    """Test converting symbols to colors."""
    symbols = "0213"
    colors = utils.symbols_to_colors(symbols)
    assert colors == ["Red", "Green", "Blue", "Yellow"]


def test_symbols_to_colors_single():
    """Test converting single symbol."""
    symbols = "0"
    colors = utils.symbols_to_colors(symbols)
    assert colors == ["Red"]


def test_round_trip_conversion():
    """Test that color->symbol->color conversion is consistent."""
    original_colors = ["Red", "Blue", "Green", "Yellow", "Purple", "Orange"]
    symbols = utils.colors_to_symbols(original_colors)
    converted_colors = utils.symbols_to_colors(symbols)
    assert converted_colors == original_colors


def test_get_available_colors():
    """Test getting available colors."""
    colors = utils.get_available_colors(4)
    assert colors == ["Red", "Blue", "Green", "Yellow"]
    assert len(colors) == 4


def test_get_available_colors_all():
    """Test getting all colors."""
    colors = utils.get_available_colors(6)
    assert len(colors) == 6
    assert colors == ["Red", "Blue", "Green", "Yellow", "Purple", "Orange"]


def test_get_available_colors_invalid():
    """Test that invalid num_colors raises error."""
    with pytest.raises(ValueError):
        utils.get_available_colors(0)
    
    with pytest.raises(ValueError):
        utils.get_available_colors(7)


def test_get_alphabet_for_colors():
    """Test getting alphabet for colors."""
    alphabet = utils.get_alphabet_for_colors(4)
    assert alphabet == "0123"


def test_get_alphabet_for_colors_all():
    """Test getting alphabet for all colors."""
    alphabet = utils.get_alphabet_for_colors(6)
    assert alphabet == "012345"


def test_get_alphabet_for_colors_invalid():
    """Test that invalid num_colors raises error."""
    with pytest.raises(ValueError):
        utils.get_alphabet_for_colors(0)
    
    with pytest.raises(ValueError):
        utils.get_alphabet_for_colors(7)


def test_validate_color_selection_valid():
    """Test validating a valid color selection."""
    rules = Rules(length=4, alphabet="0123", allow_duplicates=True)
    colors = ["Red", "Green", "Blue", "Yellow"]
    is_valid, error = utils.validate_color_selection(colors, rules)
    assert is_valid is True
    assert error == ""


def test_validate_color_selection_wrong_length():
    """Test validation fails with wrong length."""
    rules = Rules(length=4, alphabet="0123", allow_duplicates=True)
    colors = ["Red", "Green", "Blue"]
    is_valid, error = utils.validate_color_selection(colors, rules)
    assert is_valid is False
    assert "Must select exactly 4 colors" in error


def test_validate_color_selection_duplicates_not_allowed():
    """Test validation fails when duplicates not allowed."""
    rules = Rules(length=4, alphabet="0123", allow_duplicates=False)
    colors = ["Red", "Red", "Blue", "Green"]
    is_valid, error = utils.validate_color_selection(colors, rules)
    assert is_valid is False
    assert "Duplicates are not allowed" in error


def test_validate_color_selection_duplicates_allowed():
    """Test validation passes when duplicates allowed."""
    rules = Rules(length=4, alphabet="0123", allow_duplicates=True)
    colors = ["Red", "Red", "Blue", "Green"]
    is_valid, error = utils.validate_color_selection(colors, rules)
    assert is_valid is True
    assert error == ""


def test_get_color_hex():
    """Test getting hex color codes."""
    assert utils.get_color_hex("Red") == "#E74C3C"
    assert utils.get_color_hex("Blue") == "#3498DB"
    assert utils.get_color_hex("Green") == "#2ECC71"


def test_get_color_hex_invalid():
    """Test getting hex for invalid color returns default."""
    assert utils.get_color_hex("InvalidColor") == "#CCCCCC"


def test_color_map_consistency():
    """Test that color maps are consistent."""
    # Ensure COLOR_MAP and SYMBOL_MAP are inverses
    for color, symbol in utils.COLOR_MAP.items():
        assert utils.SYMBOL_MAP[symbol] == color
    
    # Ensure all colors have hex codes
    for color in utils.COLOR_MAP.keys():
        assert color in utils.COLOR_HEX


def test_colors_ordered_matches_map():
    """Test that COLORS_ORDERED matches COLOR_MAP."""
    for i, color in enumerate(utils.COLORS_ORDERED):
        assert utils.COLOR_MAP[color] == str(i)
