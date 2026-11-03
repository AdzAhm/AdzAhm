#!/usr/bin/env python3
"""Generate the animated space-themed header and footer SVGs for the profile README.

Standard library only. Run from the repository root:

    python3 scripts/generate_space_svgs.py

Writes assets/header.svg and assets/footer.svg. Everything is drawn with plain
SVG shapes and CSS animations, so the images need no fonts or external files and
keep working when GitHub embeds them as <img>. Edit the constants below
(text, colors, timings) and re-run to change them.
"""

from __future__ import annotations

import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

# Tokyo Night palette, matching the stats cards in the README.
BG_DEEP = "#0f1021"
BG = "#1a1b26"
BG_LIGHT = "#24283b"
FG = "#c0caf5"
MUTED = "#565f89"
BLUE = "#7aa2f7"
CYAN = "#7dcfff"
TEAL = "#73daca"
PURPLE = "#bb9af7"
PINK = "#f7768e"
ORANGE = "#ff9e64"
YELLOW = "#e0af68"
GREEN = "#9ece6a"

HEADER_GREETING = "HI THERE, I'M"
HEADER_NAME = "AHMAD"
# Typed out one after another under the name, like a terminal prompt.
# The first one is what still previews (and reduced-motion viewers) show.
HEADER_ROLES = ["COMPUTER ENGINEER", "TECH ENTHUSIAST", "BUILDING FROM SCRATCH", "ALWAYS LEARNING"]
TYPE_SPEED = 0.085  # seconds per typed character
DELETE_SPEED = 0.04  # seconds per deleted character
HOLD = 1.8  # seconds a finished line stays on screen
GAP = 0.4  # seconds of empty prompt between lines

# The little ship circling the planet.
ORBIT_SECONDS = 16  # one lap
ORBIT_TILT = 12  # degrees; the ring is tilted the other way
ORBIT_RX, ORBIT_RY = 104, 40
TRAIL_PARTICLES = 13

FOOTER_TITLE = "THANKS FOR VISITING!"
FOOTER_SUBTITLE = "SEE YOU IN ORBIT"
FOOTER_PLAYER = "ADZAHM"

# ---------------------------------------------------------------------------
# 5x7 pixel font
# ---------------------------------------------------------------------------

FONT: dict[str, list[str]] = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "C": [".###.", "#...#", "#....", "#....", "#....", "#...#", ".###."],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "F": ["#####", "#....", "#....", "####.", "#....", "#....", "#...."],
    "G": [".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".###."],
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "I": [".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."],
    "J": ["..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."],
    "K": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "N": ["#...#", "#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
    "Q": [".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "V": ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
    "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "#.#.#", ".#.#."],
    "X": ["#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"],
    "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
    "Z": ["#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"],
    "0": [".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."],
    "1": ["..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."],
    "2": [".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"],
    "3": ["####.", "....#", "....#", ".###.", "....#", "....#", "####."],
    "4": ["...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."],
    "5": ["#####", "#....", "####.", "....#", "....#", "#...#", ".###."],
    "6": [".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."],
    "7": ["#####", "....#", "...#.", "..#..", ".#...", ".#...", ".#..."],
    "8": [".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."],
    "9": [".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."],
    "!": ["..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."],
    ",": [".....", ".....", ".....", ".....", "..#..", "..#..", ".#..."],
    "'": ["..#..", "..#..", ".#...", ".....", ".....", ".....", "....."],
    ">": [".#...", "..#..", "...#.", "....#", "...#.", "..#..", ".#..."],
    "_": [".....", ".....", ".....", ".....", ".....", ".....", "#####"],
    "-": [".....", ".....", ".....", "#####", ".....", ".....", "....."],
    "+": [".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."],
    ".": [".....", ".....", ".....", ".....", ".....", ".....", "..#.."],
    ":": [".....", "..#..", ".....", ".....", ".....", "..#..", "....."],
    " ": [".....", ".....", ".....", ".....", ".....", ".....", "....."],
}
GLYPH_W, GLYPH_H, ADVANCE = 5, 7, 6


def text_width(text: str, scale: float) -> float:
    return (len(text) * ADVANCE - 1) * scale


def pixel_text_path(text: str, x: float, y: float, scale: float) -> str:
    """Path data for text drawn in the pixel font. Horizontal runs are merged."""
    parts = []
    for i, ch in enumerate(text.upper()):
        rows = FONT[ch]
        gx = x + i * ADVANCE * scale
        for r, row in enumerate(rows):
            c = 0
            while c < GLYPH_W:
                if row[c] == "#":
                    start = c
                    while c < GLYPH_W and row[c] == "#":
                        c += 1
                    w = (c - start) * scale
                    parts.append(f"M{fmt(gx + start * scale)} {fmt(y + r * scale)}h{fmt(w)}v{fmt(scale)}h{fmt(-w)}z")
                else:
                    c += 1
    return "".join(parts)


def fmt(v: float) -> str:
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return s if s != "-0" else "0"


# ---------------------------------------------------------------------------
# Sprites (original designs). Each letter maps to a color; "." is transparent.
# ---------------------------------------------------------------------------

SHIP = [
    "..PPP............",
    "..PBBB...........",
    "...DBBB..........",
    "...DBBBWW........",
    "DDBBBWWWWWCCWW...",
    "DBBBWWWWWWCCCWWR.",
    "DDBBBWWWWWCCWW...",
    "...DBBBWW........",
    "...DBBB..........",
    "..PBBB...........",
    "..PPP............",
]
SHIP_COLORS = {"P": PURPLE, "B": BLUE, "D": "#3d59a1", "W": FG, "C": CYAN, "R": PINK}

FLAME = [
    "..OY",
    "OOYY",
    "..OY",
]
FLAME_COLORS = {"O": ORANGE, "Y": YELLOW}

# One-eyed blob with wriggling tentacles.
BLOB = (
    [
        "...#####...",
        ".#########.",
        "###WWWWW###",
        "##WWKKKWW##",
        "##WWKKKWW##",
        "###WWWWW###",
        ".#########.",
        "#.#.#.#.#.#",
    ],
    [
        "...#####...",
        ".#########.",
        "###WWWWW###",
        "##WKKKWWW##",
        "##WKKKWWW##",
        "###WWWWW###",
        ".#########.",
        ".#.#.#.#.#.",
    ],
)
# Little saucer with blinking lights.
SAUCER = (
    [
        "....###....",
        "..#WWWWW#..",
        ".#########.",
        "###Y#Y#Y###",
        ".#########.",
        "..#.....#..",
        ".#.......#.",
    ],
    [
        "....###....",
        "..#WWWWW#..",
        ".#########.",
        "####Y#Y####",
        ".#########.",
        "..#.....#..",
        "..#.....#..",
    ],
)
# Spiky urchin with two eyes.
URCHIN = (
    [
        ".....#.....",
        "..#..#..#..",
        "...#####...",
        "#.##W#W##.#",
        ".#########.",
        "...#####...",
        "..#..#..#..",
        ".....#.....",
    ],
    [
        "..#.....#..",
        "...#.#.#...",
        "...#####...",
        ".###W#W###.",
        ".#########.",
        "...#####...",
        "...#.#.#...",
        "..#.....#..",
    ],
)


def sprite_rects(rows: list[str], colors: dict[str, str], scale: float, x: float = 0, y: float = 0) -> str:
    """Draw a sprite as one <path> per color, merging horizontal runs."""
    by_color: dict[str, list[str]] = {}
    for r, row in enumerate(rows):
        c = 0
        while c < len(row):
            ch = row[c]
            if ch == ".":
                c += 1
                continue
            start = c
            while c < len(row) and row[c] == ch:
                c += 1
            w = (c - start) * scale
            by_color.setdefault(colors[ch], []).append(
                f"M{fmt(x + start * scale)} {fmt(y + r * scale)}h{fmt(w)}v{fmt(scale)}h{fmt(-w)}z"
            )
    return "".join(f'<path fill="{col}" d="{"".join(d)}"/>' for col, d in by_color.items())


# ---------------------------------------------------------------------------
# Shared pieces
# ---------------------------------------------------------------------------


def stars(rng: random.Random, n: int, w: float, h: float, rmin: float, rmax: float, colors: list[str]) -> str:
    out = []
    for _ in range(n):
        out.append(
            f'<circle cx="{fmt(rng.uniform(0, w))}" cy="{fmt(rng.uniform(0, h))}" '
            f'r="{fmt(rng.uniform(rmin, rmax))}" fill="{rng.choice(colors)}"/>'
        )
    return "".join(out)


def svg_open(w: int, h: int, title: str, desc: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'role="img" aria-labelledby="t d">'
        f"<title id=\"t\">{title}</title><desc id=\"d\">{desc}</desc>"
    )


def background(w: int, h: int, uid: str) -> str:
    return f"""
<defs>
  <linearGradient id="{uid}bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{BG_DEEP}"/>
    <stop offset="0.55" stop-color="{BG}"/>
    <stop offset="1" stop-color="{BG_LIGHT}"/>
  </linearGradient>
  <radialGradient id="{uid}neb1" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{PURPLE}" stop-opacity="0.28"/>
    <stop offset="1" stop-color="{PURPLE}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="{uid}neb2" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{BLUE}" stop-opacity="0.22"/>
    <stop offset="1" stop-color="{BLUE}" stop-opacity="0"/>
  </radialGradient>
  <clipPath id="{uid}clip"><rect width="{w}" height="{h}" rx="18"/></clipPath>
</defs>
<rect width="{w}" height="{h}" rx="18" fill="url(#{uid}bg)"/>
"""


REDUCED_MOTION = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"

# ---------------------------------------------------------------------------
# Typing effect
# ---------------------------------------------------------------------------


def step_keyframes(name: str, events: list[tuple[float, str]], total: float, prop: str) -> str:
    """Keyframes for a value that jumps at the given times (used with steps(1,end))."""
    events = sorted(events)
    frames = []
    for t, value in events:
        frames.append(f"{fmt(100 * t / total)}%{{{prop}:{value}}}")
    frames.append(f"100%{{{prop}:{events[0][1]}}}")
    return f"@keyframes {name}{{{''.join(frames)}}}"


def typing_block(roles: list[str], x: float, y: float, scale: float) -> tuple[str, str]:
    """Pixel-font text that types, holds, and deletes each role in turn.

    Returns (svg, css). The loop starts with roles[0] fully typed and ends by
    re-typing it, so the first frame and the last frame match.
    """
    adv = ADVANCE * scale
    prompt = pixel_text_path(">", x, y, scale)
    text_x = x + 2 * adv

    # Build the timeline: for each role, when each character appears/disappears.
    t = 0.0
    shown: list[list[list[float]]] = [[[] for _ in r] for r in roles]  # boundary times per char
    cursor: list[tuple[float, int]] = []  # (time, number of visible chars)
    first = roles[0]
    # Start fully typed and holding.
    cursor.append((0.0, len(first)))
    t += HOLD
    order = list(range(1, len(roles))) + [0]
    current = 0
    for nxt in order:
        n = len(roles[current])
        for i in range(n - 1, -1, -1):  # delete from the end
            t += DELETE_SPEED
            shown[current][i].append(t)
            cursor.append((t, i))
        t += GAP
        m = len(roles[nxt])
        for i in range(m):  # type
            shown[nxt][i].append(t)
            t += TYPE_SPEED
            cursor.append((t, i + 1))
        if nxt != 0:
            t += HOLD
        current = nxt
    total = t

    svg = [f'<path d="{prompt}" fill="{TEAL}" shape-rendering="crispEdges"/>']
    css = []
    for r, role in enumerate(roles):
        for i, ch in enumerate(role):
            if ch == " ":
                continue
            # Visibility toggles at each boundary; role 0 starts visible.
            visible = r == 0
            events = [(0.0, "1" if visible else "0")]
            for b in shown[r][i]:
                visible = not visible
                events.append((b, "1" if visible else "0"))
            name = f"ty{r}_{i}"
            css.append(step_keyframes(name, events, total, "opacity"))
            d = pixel_text_path(ch, text_x + i * adv, y, scale)
            base = "" if r == 0 else ' opacity="0"'
            svg.append(
                f'<path class="ty" style="animation-name:{name}" d="{d}" fill="{FG}" '
                f'shape-rendering="crispEdges"{base}/>'
            )
    cursor_events = [(ct, f"translateX({fmt(n * adv)}px)") for ct, n in cursor]
    css.append(step_keyframes("tycur", cursor_events, total, "transform"))
    base_x = len(first) * adv
    svg.append(
        f'<g transform="translate({fmt(text_x)} {fmt(y)})"><g class="tycur" style="transform:translateX({fmt(base_x)}px)">'
        f'<rect class="cursor" x="0" y="0" width="{fmt(scale * 5)}" height="{fmt(scale * 7)}" fill="{TEAL}"/></g></g>'
    )
    css.insert(
        0,
        f".ty,.tycur{{animation-duration:{fmt(total)}s;animation-timing-function:steps(1,end);"
        f"animation-iteration-count:infinite;animation-fill-mode:both}}"
        f".tycur{{animation-name:tycur}}",
    )
    return "".join(svg), "".join(css)


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------


def orbiter(px: float, py: float, half: str) -> str:
    """Ship + particle trail on a tilted elliptical orbit around (px, py).

    Drawn twice: the far half (half="back") before the planet so the planet hides
    it, and the near half (half="front") after. Both copies share the same clock.
    """
    rx, ry, dur = ORBIT_RX, ORBIT_RY, ORBIT_SECONDS
    # Starts at the left end, sweeps along the near (lower) side first.
    path = f"M{px - rx} {py}A{rx} {ry} 0 0 0 {px + rx} {py}A{rx} {ry} 0 0 0 {px - rx} {py}"
    scale = 1.8
    ship_w, ship_h = len(SHIP[0]) * scale, len(SHIP) * scale
    ship = sprite_rects(SHIP, SHIP_COLORS, scale, x=-ship_w / 2, y=-ship_h / 2)
    flame = sprite_rects(FLAME, FLAME_COLORS, scale, x=-ship_w / 2 - 4 * scale, y=-ship_h / 2 + 4 * scale)
    # Bigger on the near side, smaller on the far side, for a bit of depth.
    depth = '<animateTransform attributeName="transform" type="scale" values="1;1.2;1;.72;1" keyTimes="0;.25;.5;.75;1" dur="{d}s" repeatCount="indefinite"/>'.format(d=dur)

    trail = []
    palette = [YELLOW, YELLOW, ORANGE, ORANGE, PINK, PINK, PINK, PURPLE, PURPLE, PURPLE, BLUE, BLUE, BLUE]
    spacing = 0.15
    for i in range(TRAIL_PARTICLES):
        lag = (i + 3) * spacing  # how far behind the ship, in seconds
        k = i / max(1, TRAIL_PARTICLES - 1)
        r = 2.8 - 1.9 * k
        op = 1 - 0.75 * k
        trail.append(
            f'<circle r="{fmt(r)}" fill="{palette[i % len(palette)]}" opacity="{fmt(op)}">'
            f'<animate attributeName="r" values="{fmt(r)};{fmt(r * 0.55)};{fmt(r)}" dur="{fmt(0.5 + 0.07 * i)}s" repeatCount="indefinite"/>'
            f'<animateMotion dur="{dur}s" repeatCount="indefinite" begin="-{fmt(dur - lag)}s" path="{path}"/></circle>'
        )
    return (
        f'<g transform="rotate({ORBIT_TILT} {px} {py})" clip-path="url(#o{half})">'
        f'{"".join(trail)}'
        f'<g><animateMotion dur="{dur}s" repeatCount="indefinite" rotate="auto" path="{path}"/>'
        f'<g>{depth}<g class="flame">{flame}</g>{ship}</g></g>'
        f"</g>"
    )


def build_header() -> str:
    W, H = 1000, 300
    rng = random.Random(7)
    star_colors = [FG, FG, FG, CYAN, PURPLE]
    twinkle_groups = "".join(
        f'<g class="tw tw{i}">{stars(rng, 22, W, H, 0.6, 1.8, star_colors)}</g>' for i in range(4)
    )

    greet_scale, name_scale, tag_scale = 3, 13, 4
    x0 = 64
    greet = pixel_text_path(HEADER_GREETING, x0, 58, greet_scale)
    name_y = 96
    name = pixel_text_path(HEADER_NAME, x0, name_y, name_scale)
    name_shadow = pixel_text_path(HEADER_NAME, x0 + 7, name_y + 7, name_scale)
    tag_y = 218
    typing_svg, typing_css = typing_block(HEADER_ROLES, x0, tag_y, tag_scale)

    # Planet with a ring: the back half of the ring is drawn behind the planet,
    # the front half (clipped to the lower half) in front of it.
    px, py, pr = 865, 140, 72
    ring = f'<ellipse cx="{px}" cy="{py}" rx="128" ry="26" fill="none" stroke="url(#hring)" stroke-width="7"/>'

    ship = sprite_rects(SHIP, SHIP_COLORS, 3)
    flame = sprite_rects(FLAME, FLAME_COLORS, 3, x=-12, y=12)

    return (
        svg_open(W, H, "Hi there, I'm Ahmad", "Animated space banner: twinkling stars, a ringed planet with a small spaceship orbiting it, and another ship flying past the name Ahmad. Below the name, a terminal prompt types out: " + ", ".join(r.title() for r in HEADER_ROLES) + ".")
        + background(W, H, "h")
        + f"""
<defs>
  <linearGradient id="hname" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{CYAN}"/>
    <stop offset="0.5" stop-color="{BLUE}"/>
    <stop offset="1" stop-color="{PURPLE}"/>
  </linearGradient>
  <radialGradient id="hplanet" cx="0.35" cy="0.3" r="0.8">
    <stop offset="0" stop-color="{CYAN}"/>
    <stop offset="0.45" stop-color="{BLUE}"/>
    <stop offset="1" stop-color="#2a2f6b"/>
  </radialGradient>
  <linearGradient id="hring" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{PURPLE}" stop-opacity="0.15"/>
    <stop offset="0.5" stop-color="{PURPLE}" stop-opacity="0.95"/>
    <stop offset="1" stop-color="{PINK}" stop-opacity="0.2"/>
  </linearGradient>
  <linearGradient id="htrail" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{FG}" stop-opacity="0"/>
    <stop offset="1" stop-color="{FG}" stop-opacity="0.9"/>
  </linearGradient>
  <clipPath id="hfront"><rect x="{px - 140}" y="{py}" width="280" height="60"/></clipPath>
  <clipPath id="oback"><rect x="{px - 220}" y="{py - 140}" width="440" height="140"/></clipPath>
  <clipPath id="ofront"><rect x="{px - 220}" y="{py}" width="440" height="140"/></clipPath>
  <filter id="hblur" x="-20%" y="-60%" width="140%" height="220%"><feGaussianBlur stdDeviation="10"/></filter>
</defs>
<style>
  .tw{{animation:twinkle 4s ease-in-out infinite}}
  .tw1{{animation-delay:-1s}} .tw2{{animation-delay:-2s}} .tw3{{animation-delay:-3s}}
  @keyframes twinkle{{0%,100%{{opacity:.25}}50%{{opacity:1}}}}
  .neb{{animation:drift 14s ease-in-out infinite alternate}}
  @keyframes drift{{from{{transform:translate(0,0)}}to{{transform:translate(40px,12px)}}}}
  .planet{{animation:bob 7s ease-in-out infinite alternate}}
  @keyframes bob{{from{{transform:translateY(-5px)}}to{{transform:translateY(5px)}}}}
  .shoot{{animation:shoot 9s linear infinite;opacity:0}}
  .shoot2{{animation-delay:-4.5s}}
  @keyframes shoot{{0%{{transform:translate(0,0);opacity:0}}2%{{opacity:1}}9%{{transform:translate(-260px,130px);opacity:0}}100%{{transform:translate(-260px,130px);opacity:0}}}}
  .fly{{animation:fly 12s ease-in-out infinite;opacity:0}}
  @keyframes fly{{0%{{transform:translate(-80px,262px);opacity:1}}30%{{transform:translate(1080px,250px);opacity:1}}30.01%,100%{{opacity:0;transform:translate(1080px,250px)}}}}
  .flame{{animation:flicker .12s steps(2) infinite alternate;transform-box:fill-box;transform-origin:100% 50%}}
  @keyframes flicker{{from{{transform:scaleX(.6)}}to{{transform:scaleX(1.25)}}}}
  .cursor{{animation:blink 1s steps(1) infinite}}
  @keyframes blink{{50%{{opacity:0}}}}
  {typing_css}
  .glow{{animation:glow 3s ease-in-out infinite alternate}}
  @keyframes glow{{from{{opacity:.35}}to{{opacity:.8}}}}
  {REDUCED_MOTION}
</style>
<g clip-path="url(#hclip)">
  <g class="neb">
    <ellipse cx="300" cy="80" rx="320" ry="140" fill="url(#hneb1)"/>
    <ellipse cx="760" cy="250" rx="300" ry="150" fill="url(#hneb2)"/>
  </g>
  {twinkle_groups}
  <g class="shoot"><line x1="780" y1="20" x2="880" y2="-30" stroke="url(#htrail)" stroke-width="2" transform="rotate(180 830 -5)"/></g>
  <g class="shoot shoot2"><line x1="520" y1="10" x2="600" y2="-30" stroke="url(#htrail)" stroke-width="1.5" transform="rotate(180 560 -10)"/></g>
  <g class="planet">
    <g transform="rotate(-16 {px} {py})">{ring}</g>
    {orbiter(px, py, "back")}
    <circle cx="{px}" cy="{py}" r="{pr + 10}" fill="{BLUE}" opacity=".12"/>
    <circle cx="{px}" cy="{py}" r="{pr}" fill="url(#hplanet)"/>
    <path d="M{px - pr + 12} {py - 18}q{pr} -22 {2 * pr - 24} 6" fill="none" stroke="{FG}" stroke-opacity=".18" stroke-width="6" stroke-linecap="round"/>
    <path d="M{px - pr + 8} {py + 22}q{pr} -18 {2 * pr - 14} 4" fill="none" stroke="#2a2f6b" stroke-opacity=".5" stroke-width="8" stroke-linecap="round"/>
    <g transform="rotate(-16 {px} {py})" clip-path="url(#hfront)">{ring}</g>
    {orbiter(px, py, "front")}
  </g>
  <g class="fly"><g transform="rotate(-0.6)"><g class="flame">{flame}</g>{ship}</g></g>
  <path d="{greet}" fill="{TEAL}" shape-rendering="crispEdges"/>
  <path class="glow" d="{name}" fill="{BLUE}" opacity=".5" transform="translate(-2 -2)" filter="url(#hblur)"/>
  <path d="{name_shadow}" fill="#2a2f6b" shape-rendering="crispEdges"/>
  <path d="{name}" fill="url(#hname)" shape-rendering="crispEdges"/>
  {typing_svg}
</g>
</svg>
"""
    )


# ---------------------------------------------------------------------------
# Footer: the ship clears a wave of aliens, forever.
# ---------------------------------------------------------------------------

LOOP = 4.5  # seconds for one full cycle (three shots)
SEG = LOOP / 3  # one shot per lane


def pct(t: float) -> str:
    return fmt(100 * t / LOOP) + "%"


def build_footer() -> str:
    W, H = 1000, 300
    rng = random.Random(11)

    # Parallax starfield: each layer is drawn twice side by side and scrolled
    # left by exactly one width, so the loop is seamless.
    layers = []
    for i, (n, rmin, rmax, speed, op) in enumerate(
        [(45, 0.5, 1.0, 40, 0.5), (28, 0.8, 1.5, 22, 0.75), (14, 1.2, 2.2, 11, 1.0)]
    ):
        field = stars(rng, n, W, H, rmin, rmax, [FG, FG, CYAN, PURPLE])
        layers.append(
            f'<g class="sf" style="animation-duration:{speed}s" opacity="{op}">'
            f'{field}<g transform="translate({W} 0)">{field}</g></g>'
        )

    scale = 4
    lanes = [96, 146, 196]  # lane centre y
    order = [0, 2, 1]  # which lane each shot targets, in time order
    ship_x = 96
    ship_h = len(SHIP) * scale
    ship_nose = ship_x + len(SHIP[0]) * scale
    alien_x = 820
    alien_w = 11 * scale

    # Ship moves between lanes: start in the last lane of the previous cycle.
    move = 0.35
    frames = []
    for k, lane in enumerate(order):
        t0 = k * SEG
        prev = order[k - 1]
        frames.append(f"{pct(t0)}{{transform:translateY({lanes[prev] - lanes[1]}px)}}")
        frames.append(f"{pct(t0 + move)}{{transform:translateY({lanes[lane] - lanes[1]}px)}}")
    frames.append(f"100%{{transform:translateY({lanes[order[-1]] - lanes[1]}px)}}")
    ship_keys = "".join(frames)

    fire, hit = 0.42, 0.75
    respawn_start, respawn_end = 3.2, 3.6
    travel = alien_x - 8 - ship_nose

    aliens = [
        (BLOB, {"#": PINK, "W": FG, "K": BG}, PINK),
        (SAUCER, {"#": GREEN, "W": CYAN, "Y": YELLOW}, GREEN),
        (URCHIN, {"#": PURPLE, "W": FG}, PURPLE),
    ]

    lane_groups = []
    for k, lane in enumerate(order):
        delay = fmt(k * SEG)
        sprite, colors, color = aliens[lane]
        a_h = len(sprite[0]) * scale
        ay = lanes[lane] - a_h / 2
        f1 = sprite_rects(sprite[0], colors, scale)
        f2 = sprite_rects(sprite[1], colors, scale)
        # Debris: 8 pixels thrown outward.
        debris = []
        for j, (dx, dy) in enumerate([(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]):
            debris.append(
                f'<rect class="deb d{j}" x="-4" y="-4" width="8" height="8" fill="{(color, YELLOW, FG)[j % 3]}" '
                f'style="animation-delay:{delay}s"/>'
            )
        cx, cy = alien_x + alien_w / 2, lanes[lane]
        popup = pixel_text_path("+100", 0, 0, 2)
        lane_groups.append(
            f"""
  <g transform="translate({ship_nose} {lanes[lane] - 2})">
    <g class="laser" style="animation-delay:{delay}s">
      <rect x="0" y="-3" width="34" height="10" rx="5" fill="{TEAL}" opacity=".35"/>
      <rect x="0" y="0" width="34" height="4" rx="2" fill="{CYAN}"/>
      <rect x="20" y="0" width="14" height="4" rx="2" fill="#ffffff"/>
    </g>
    <g class="muzzle" style="animation-delay:{delay}s"><circle r="12" cx="2" cy="2" fill="{CYAN}" opacity=".45"/><circle r="6" cx="2" cy="2" fill="#ffffff"/></g>
  </g>
  <g transform="translate({alien_x} {fmt(ay)})">
    <g class="alien" style="animation-delay:{delay}s">
      <g class="wig" style="animation-delay:-{fmt(k * 0.45)}s">
        <g class="fa">{f1}</g><g class="fb">{f2}</g>
      </g>
    </g>
  </g>
  <g transform="translate({fmt(cx)} {fmt(cy)})">
    <circle class="ring" r="22" fill="none" stroke="{color}" stroke-width="3" style="animation-delay:{delay}s"/>
    <circle class="boom" r="12" fill="#ffffff" style="animation-delay:{delay}s"/>
    {"".join(debris)}
  </g>
  <g transform="translate({fmt(alien_x - text_width('+100', 2) - 14)} {fmt(cy - 26)})">
    <path class="pop" d="{popup}" fill="{YELLOW}" shape-rendering="crispEdges" style="animation-delay:{delay}s"/>
  </g>"""
        )

    debris_keys = []
    for j, (dx, dy) in enumerate([(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]):
        dist = 54 if dx == 0 or dy == 0 else 40
        debris_keys.append(
            f".d{j}{{animation-name:deb{j}}}"
            f"@keyframes deb{j}{{0%,{pct(hit)}{{transform:translate(0,0);opacity:0}}"
            f"{pct(hit + 0.01)}{{opacity:1;transform:translate(0,0)}}"
            f"{pct(hit + 0.5)}{{opacity:0;transform:translate({dx * dist}px,{dy * dist}px) rotate(90deg)}}"
            f"100%{{opacity:0;transform:translate({dx * dist}px,{dy * dist}px)}}}}"
        )

    ship = sprite_rects(SHIP, SHIP_COLORS, scale)
    flame = sprite_rects(FLAME, FLAME_COLORS, scale, x=-4 * scale, y=4 * scale)

    title_scale, sub_scale, hud_scale = 4, 2, 2
    title = pixel_text_path(FOOTER_TITLE, (W - text_width(FOOTER_TITLE, title_scale)) / 2, 236, title_scale)
    title_shadow = pixel_text_path(FOOTER_TITLE, (W - text_width(FOOTER_TITLE, title_scale)) / 2 + 3, 239, title_scale)
    sub = pixel_text_path(FOOTER_SUBTITLE, (W - text_width(FOOTER_SUBTITLE, sub_scale)) / 2, 276, sub_scale)
    hud_1up = pixel_text_path("1UP", 28, 22, hud_scale)
    hud_name = pixel_text_path(FOOTER_PLAYER, 28 + text_width("1UP ", hud_scale) + 6, 22, hud_scale)
    hud_lives = pixel_text_path("LIVES", W - 150, 22, hud_scale)
    mini = "".join(
        f'<g transform="translate({W - 82 + i * 20} 19)">{sprite_rects(SHIP, SHIP_COLORS, 1)}</g>' for i in range(3)
    )

    return (
        svg_open(W, H, "Thanks for visiting!", "Animated footer: a pixel spaceship moves between lanes and shoots aliens over a scrolling starfield, above the text Thanks for visiting, see you in orbit.")
        + background(W, H, "f")
        + f"""
<defs>
  <linearGradient id="ftitle" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{TEAL}"/>
    <stop offset="0.5" stop-color="{BLUE}"/>
    <stop offset="1" stop-color="{PURPLE}"/>
  </linearGradient>
</defs>
<style>
  .sf{{animation:scroll linear infinite}}
  @keyframes scroll{{from{{transform:translateX(0)}}to{{transform:translateX(-{W}px)}}}}
  .ship{{animation:lanes {LOOP}s ease-in-out infinite}}
  @keyframes lanes{{{ship_keys}}}
  .hover{{animation:hover 1.3s ease-in-out infinite alternate}}
  @keyframes hover{{from{{transform:translateY(-3px)}}to{{transform:translateY(3px)}}}}
  .flame{{animation:flicker .12s steps(2) infinite alternate;transform-box:fill-box;transform-origin:100% 50%}}
  @keyframes flicker{{from{{transform:scaleX(.55)}}to{{transform:scaleX(1.3)}}}}
  .laser{{opacity:0;animation:laser {LOOP}s linear infinite both}}
  @keyframes laser{{0%,{pct(fire)}{{opacity:0;transform:translateX(0)}}{pct(fire + 0.01)}{{opacity:1;transform:translateX(0)}}{pct(hit)}{{opacity:1;transform:translateX({fmt(travel)}px)}}{pct(hit + 0.01)},100%{{opacity:0;transform:translateX({fmt(travel)}px)}}}}
  .muzzle{{opacity:0;animation:muzzle {LOOP}s linear infinite both;transform-box:fill-box;transform-origin:center}}
  @keyframes muzzle{{0%,{pct(fire)}{{opacity:0;transform:scale(.2)}}{pct(fire + 0.02)}{{opacity:.9;transform:scale(1)}}{pct(fire + 0.14)},100%{{opacity:0;transform:scale(1.6)}}}}
  .alien{{animation:alien {LOOP}s linear infinite both;transform-box:fill-box;transform-origin:center}}
  @keyframes alien{{0%,{pct(hit)}{{opacity:1;transform:scale(1)}}{pct(hit + 0.08)}{{opacity:0;transform:scale(1.35)}}{pct(respawn_start)}{{opacity:0;transform:scale(0)}}{pct(respawn_end)}{{opacity:1;transform:scale(1.1)}}{pct(respawn_end + 0.15)},100%{{opacity:1;transform:scale(1)}}}}
  .wig{{animation:wig 1.4s ease-in-out infinite alternate}}
  @keyframes wig{{from{{transform:translateY(-7px)}}to{{transform:translateY(7px)}}}}
  .fa{{animation:fa .9s steps(1) infinite}}
  .fb{{animation:fb .9s steps(1) infinite}}
  @keyframes fa{{0%{{opacity:1}}50%{{opacity:0}}}}
  @keyframes fb{{0%{{opacity:0}}50%{{opacity:1}}}}
  .boom{{opacity:0;animation:boom {LOOP}s ease-out infinite both;transform-box:fill-box;transform-origin:center}}
  @keyframes boom{{0%,{pct(hit)}{{opacity:0;transform:scale(.3)}}{pct(hit + 0.02)}{{opacity:1;transform:scale(1)}}{pct(hit + 0.16)},100%{{opacity:0;transform:scale(1.5)}}}}
  .ring{{opacity:0;animation:ring {LOOP}s ease-out infinite both;transform-box:fill-box;transform-origin:center}}
  @keyframes ring{{0%,{pct(hit)}{{opacity:0;transform:scale(.2)}}{pct(hit + 0.02)}{{opacity:1;transform:scale(.4)}}{pct(hit + 0.45)},100%{{opacity:0;transform:scale(1.8)}}}}
  .deb{{opacity:0;animation-duration:{LOOP}s;animation-timing-function:ease-out;animation-iteration-count:infinite;animation-fill-mode:both}}
  {"".join(debris_keys)}
  .pop{{opacity:0;animation:pop {LOOP}s ease-out infinite both}}
  @keyframes pop{{0%,{pct(hit)}{{opacity:0;transform:translateY(0)}}{pct(hit + 0.05)}{{opacity:1}}{pct(hit + 0.7)}{{opacity:1;transform:translateY(-18px)}}{pct(hit + 0.9)},100%{{opacity:0;transform:translateY(-24px)}}}}
  .blink{{animation:blink 1.2s steps(1) infinite}}
  @keyframes blink{{50%{{opacity:.15}}}}
  {REDUCED_MOTION}
</style>
<g clip-path="url(#fclip)">
  <ellipse cx="520" cy="140" rx="380" ry="120" fill="url(#fneb1)"/>
  <ellipse cx="150" cy="260" rx="260" ry="110" fill="url(#fneb2)"/>
  {"".join(layers)}
  {"".join(lane_groups)}
  <g transform="translate({ship_x} {lanes[1] - ship_h / 2})">
    <g class="ship"><g class="hover"><g class="flame">{flame}</g>{ship}</g></g>
  </g>
  <path d="{hud_1up}" fill="{PINK}" shape-rendering="crispEdges"/>
  <path d="{hud_name}" fill="{FG}" shape-rendering="crispEdges"/>
  <path d="{hud_lives}" fill="{MUTED}" shape-rendering="crispEdges"/>
  {mini}
  <path d="{title_shadow}" fill="#2a2f6b" shape-rendering="crispEdges"/>
  <path d="{title}" fill="url(#ftitle)" shape-rendering="crispEdges"/>
  <path class="blink" d="{sub}" fill="{YELLOW}" shape-rendering="crispEdges"/>
</g>
</svg>
"""
    )


def minify(svg: str) -> str:
    return "\n".join(line.strip() for line in svg.splitlines() if line.strip()) + "\n"


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    for name, build in [("header.svg", build_header), ("footer.svg", build_footer)]:
        path = ASSETS / name
        path.write_text(minify(build()), encoding="utf-8")
        print(f"wrote {path.relative_to(ROOT)} ({path.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
