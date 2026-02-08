def fibonacci(n: int) -> int:
    """Retourne le n-ième terme de la suite de Fibonacci (0-indexé)."""
    if n < 0:
        raise ValueError("n doit être ≥ 0")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
