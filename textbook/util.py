"""Number helpers, so every answer in the book is worked by code."""
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction
import math


def rnd(x, places=0):
    """round half up, the way the class rounds; returns a float"""
    q = Decimal(1).scaleb(-places)
    return float(Decimal(repr(float(x))).quantize(q, rounding=ROUND_HALF_UP))


def n(x, places=None):
    """a number as the book prints it: commas, no trailing zeros"""
    if isinstance(x, Fraction):
        x = float(x)
    if places is not None:
        x = rnd(x, places)
        if places <= 0:
            return f"{int(x):,}"
        return f"{x:,.{places}f}"
    x = round(float(x), 9)
    if x == int(x):
        return f"{int(x):,}"
    s = f"{x:,.8f}".rstrip("0").rstrip(".")
    return s


def r(x, places):
    """rounded, then printed without padding zeros"""
    return n(rnd(x, places))


def fr(x, stacked=True):
    """a fraction or mixed number in lowest terms, in book markup"""
    x = Fraction(x)
    sign = "−" if x < 0 else ""
    x = abs(x)
    w, rem = divmod(x.numerator, x.denominator)
    if rem == 0:
        return f"{sign}{w}"
    part = f"[[{rem}|{x.denominator}]]"
    return f"{sign}{w} {part}" if w else f"{sign}{part}"


def F(s):
    """'3 5/8' or '5/8' or '2.75' -> Fraction"""
    s = s.strip()
    if " " in s:
        w, f = s.split()
        return int(w) + Fraction(f)
    return Fraction(s)


def frtxt(s):
    """'3 5/8' -> markup with a stacked fraction"""
    s = s.strip()
    if "/" not in s:
        return s
    if " " in s:
        w, f = s.split()
        a, b = f.split("/")
        return f"{w} [[{a}|{b}]]"
    a, b = s.split("/")
    return f"[[{a}|{b}]]"


PI = 3.14
sqrt = math.sqrt
