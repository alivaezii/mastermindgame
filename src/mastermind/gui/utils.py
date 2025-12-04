"""
Utility functions for the Mastermind GUI.

Provides color-to-symbol mapping, validation, and helper functions
for translating between the visual color interface and the game engine's
symbol-based logic.
"""

from typing import List
from ..engine import Rules


# Color palette for the game
COLOR_MAP = {
    "Red": "0",
    "Blue": "1",
    "Green": "2",
    "Yellow": "3",
    "Purple": "4",
    "Orange": "5"
}

# Reverse mapping for symbol to color conversion
SYMBOL_MAP = {v: k for k, v in COLOR_MAP.items()}

# Hex color codes for visual display
COLOR_HEX = {
    "Red": "#E74C3C",
    "Blue": "#3498DB",
    "Green": "#2ECC71",
    "Yellow": "#F1C40F",
    "Purple": "#9B59B6",
    "Orange": "#E67E22"
}

# Ordered list of colors (matches symbol order)
COLORS_ORDERED = ["Red", "Blue", "Green", "Yellow", "Purple", "Orange"]


def colors_to_symbols(colors: List[str]) -> str:
    """
    Convert a list of color names to a symbol string.
    
    Args:
        colors: List of color names (e.g., ["Red", "Green", "Blue"])
    
    Returns:
        String of symbols (e.g., "021")
    
    Example:
        >>> colors_to_symbols(["Red", "Green", "Blue", "Yellow"])
        "0213"
    """
    return "".join(COLOR_MAP[color] for color in colors)


def symbols_to_colors(symbols: str) -> List[str]:
    """
    Convert a symbol string to a list of color names.
    
    Args:
        symbols: String of symbols (e.g., "0213")
    
    Returns:
        List of color names (e.g., ["Red", "Green", "Blue", "Yellow"])
    
    Example:
        >>> symbols_to_colors("0213")
        ["Red", "Green", "Blue", "Yellow"]
    """
    return [SYMBOL_MAP[symbol] for symbol in symbols]


def get_available_colors(num_colors: int) -> List[str]:
    """
    Get the first N colors from the color palette.
    
    Args:
        num_colors: Number of colors to return (1-6)
    
    Returns:
        List of color names
    
    Raises:
        ValueError: If num_colors is not between 1 and 6
    
    Example:
        >>> get_available_colors(4)
        ["Red", "Blue", "Green", "Yellow"]
    """
    if num_colors < 1 or num_colors > len(COLORS_ORDERED):
        raise ValueError(f"num_colors must be between 1 and {len(COLORS_ORDERED)}")
    return COLORS_ORDERED[:num_colors]


def get_alphabet_for_colors(num_colors: int) -> str:
    """
    Get the alphabet string for a given number of colors.
    
    Args:
        num_colors: Number of colors (1-6)
    
    Returns:
        Alphabet string (e.g., "012345" for 6 colors)
    
    Example:
        >>> get_alphabet_for_colors(4)
        "0123"
    """
    if num_colors < 1 or num_colors > len(COLORS_ORDERED):
        raise ValueError(f"num_colors must be between 1 and {len(COLORS_ORDERED)}")
    return "".join(str(i) for i in range(num_colors))


def validate_color_selection(colors: List[str], rules: Rules) -> tuple[bool, str]:
    """
    Validate a color selection against game rules.
    
    Args:
        colors: List of selected colors
        rules: Game rules to validate against
    
    Returns:
        Tuple of (is_valid, error_message)
        If valid, error_message is empty string
    
    Example:
        >>> rules = Rules(length=4, alphabet="0123", allow_duplicates=False)
        >>> validate_color_selection(["Red", "Red", "Blue", "Green"], rules)
        (False, "Duplicates are not allowed")
    """
    # Check length
    if len(colors) != rules.length:
        return False, f"Must select exactly {rules.length} colors"
    
    # Check for duplicates if not allowed
    if not rules.allow_duplicates and len(set(colors)) < len(colors):
        return False, "Duplicates are not allowed"
    
    # Check if all colors are valid
    valid_colors = get_available_colors(len(rules.alphabet))
    for color in colors:
        if color not in valid_colors:
            return False, f"Invalid color: {color}"
    
    return True, ""


def get_color_hex(color: str) -> str:
    """
    Get the hex color code for a color name.
    
    Args:
        color: Color name
    
    Returns:
        Hex color code (e.g., "#E74C3C")
    
    Example:
        >>> get_color_hex("Red")
        "#E74C3C"
    """
    return COLOR_HEX.get(color, "#CCCCCC")
