"""Gini coefficient calculation for measuring inequality."""

import statistics


def calculate_gini(values: list[int | float]) -> float:
    """Calculate the Gini coefficient for a list of values.

    The Gini coefficient measures inequality on a scale from 0 to 1:
    - 0 = perfect equality (everyone has the same value)
    - 1 = perfect inequality (one person has everything)

    Args:
        values: List of numeric values (e.g., roster values)

    Returns:
        Gini coefficient between 0 and 1
    """
    if not values:
        return 0.0

    sorted_values = sorted(values)
    n = len(sorted_values)
    total = sum(sorted_values)

    if total == 0:
        return 0.0

    # Calculate using the relative mean absolute difference formula
    weighted_sum = sum(
        (2 * (i + 1) - n - 1) * val for i, val in enumerate(sorted_values)
    )

    return weighted_sum / (n * total)


def interpret_gini(gini: float) -> str:
    """Return a human-readable interpretation of the Gini coefficient.

    Args:
        gini: Gini coefficient between 0 and 1

    Returns:
        Description of competitive balance
    """
    if gini < 0.15:
        return "Highly Competitive"
    elif gini < 0.25:
        return "Healthy"
    elif gini < 0.35:
        return "Imbalanced"
    else:
        return "Severely Lopsided"


def calculate_stats(values: list[int | float]) -> dict:
    """Calculate additional statistics for the values.

    Args:
        values: List of numeric values

    Returns:
        Dictionary with average, std_dev, and top_bottom_ratio
    """
    if not values:
        return {"average": 0.0, "std_dev": 0.0, "top_bottom_ratio": 0.0}

    sorted_values = sorted(values)
    avg = statistics.mean(values)
    std = statistics.stdev(values) if len(values) > 1 else 0.0

    # Avoid division by zero for top/bottom ratio
    bottom = sorted_values[0] if sorted_values[0] > 0 else 1
    top_bottom = sorted_values[-1] / bottom

    return {
        "average": avg,
        "std_dev": std,
        "top_bottom_ratio": top_bottom,
    }
