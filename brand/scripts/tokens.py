"""LORE brand tokens — single source of truth for scripts. Mirrors brand-guidelines.md §8."""

CORE = [
    # name, hex, role, pantone (nearest candidate, UNVERIFIED — confirm with physical guide / drawdown)
    ("Ink",        "#14161A", "Primary text, device Ink finish, wordmark on light", "Black 6 C"),
    ("Bone",       "#F3EEE6", "Primary ground, paper, packaging stock", "Warm Gray 1 C @ 25% / natural uncoated stock"),
    ("Terracotta", "#C4623A", "Primary accent: symbol, calls-to-action, LED 'story' state", "7591 C"),
    ("Brass",      "#B8935A", "Premium detail: foil, Atlas crown, dividers", "7562 C (solid) / 871 C (metallic)"),
    ("Olive",      "#5E6B4E", "Secondary accent: maps, parks, 'offline ready'", "5753 C"),
    ("Fog",        "#9AA0A6", "Secondary text, hairlines, disabled", "429 C"),
    ("Night",      "#0D1B2A", "Dark ground, night mode, Walk Me Home", "5395 C"),
]

FUNCTIONAL = [
    ("Signal",  "#D2392B", "SOS and safety-critical alerts ONLY", "485 C (approx.)"),
    ("Verdigris", "#3F7F74", "Confirmations, arrived, check-in OK", "5545 C (approx.)"),
]

INK, BONE, TERRA, BRASS, OLIVE, FOG, NIGHT = (c[1] for c in CORE)
SIGNAL, VERDIGRIS = (c[1] for c in FUNCTIONAL)


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_cmyk(rgb):
    """Naive device-independent conversion. Print values MUST be confirmed by the printer's ICC (FOGRA39/GRACoL)."""
    r, g, b = (v / 255 for v in rgb)
    k = 1 - max(r, g, b)
    if k >= 1:
        return (0, 0, 0, 100)
    c = (1 - r - k) / (1 - k)
    m = (1 - g - k) / (1 - k)
    y = (1 - b - k) / (1 - k)
    return tuple(round(v * 100) for v in (c, m, y, k))


def rel_lum(h):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = hex_to_rgb(h)
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast(a, b):
    la, lb = sorted((rel_lum(a), rel_lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def mix(h1, h2, t):
    a, b = hex_to_rgb(h1), hex_to_rgb(h2)
    return "#%02X%02X%02X" % tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))
