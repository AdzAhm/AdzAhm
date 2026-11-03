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

import math
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
# Footer: a short scripted battle that loops every FOOTER_LOOP seconds.
#
#   0.3s  the middle alien fires; the ship raises its shield and the bolt bursts on it
#   1.1s  the top and bottom aliens fire too; both bolts hit the shield
#   2.7s  shield down; the ship flies to the top lane and shoots the top alien
#   3.6s  the middle alien fires again; the ship dodges to the bottom lane and
#         shoots the bottom alien while the bolt flies through the empty lane
#   4.7s  back to the middle: charge up, fire a beam, big explosion, +300
#   6.6s  WAVE CLEAR! then the aliens warp back in one by one
# ---------------------------------------------------------------------------

FOOTER_LOOP = 10.0  # seconds for the whole battle

Frame = tuple[float, str]


def keyframes(name: str, frames: list[Frame], total: float = FOOTER_LOOP) -> str:
    """CSS keyframes from (seconds, declarations) pairs.

    A value holds between two pairs that repeat it. The first value is reused
    at the end so the loop is seamless.
    """
    frames = sorted(frames, key=lambda f: f[0])
    if frames[0][0] > 0:
        frames.insert(0, (0.0, frames[0][1]))
    if frames[-1][0] < total:
        frames.append((total, frames[0][1]))
    body = "".join(f"{fmt(100 * t / total)}%{{{css}}}" for t, css in frames)
    return f"@keyframes {name}{{{body}}}"


def blip(t: float, on: str, off: str, rise: float = 0.05, hold: float = 0.0, fall: float = 0.25) -> list[Frame]:
    """A quick flash: off at t, on after `rise`, (held for `hold`), off again after `fall`."""
    frames = [(t, off), (t + rise, on)]
    if hold:
        frames.append((t + rise + hold, on))
    frames.append((t + rise + hold + fall, off))
    return frames


def build_footer() -> str:
    W, H = 1000, 300
    rng = random.Random(11)

    # Parallax starfield: each layer is drawn twice side by side and scrolled
    # left by exactly one width, so the loop is seamless.
    layers = []
    for n, rmin, rmax, speed, op in [(45, 0.5, 1.0, 40, 0.5), (28, 0.8, 1.5, 22, 0.75), (14, 1.2, 2.2, 11, 1.0)]:
        field = stars(rng, n, W, H, rmin, rmax, [FG, FG, CYAN, PURPLE])
        layers.append(
            f'<g class="sf" style="animation-duration:{speed}s" opacity="{op}">'
            f'{field}<g transform="translate({W} 0)">{field}</g></g>'
        )

    s = 4  # sprite pixel size
    lanes = [96, 146, 196]  # lane centre y: top, middle, bottom
    mid = lanes[1]
    ship_x = 96
    ship_w, ship_h = len(SHIP[0]) * s, len(SHIP) * s
    nose = ship_x + ship_w
    alien_x = 820
    alien_w = 11 * s
    alien_cx = alien_x + alien_w / 2
    shield_r = 46
    shield_edge = ship_x + ship_w / 2 + shield_r

    css: list[str] = []

    def anim(cls: str, frames: list[Frame], timing: str = "linear", extra: str = "") -> None:
        css.append(f".{cls}{{animation:{cls} {fmt(FOOTER_LOOP)}s {timing} infinite both;{extra}}}")
        css.append(keyframes(cls, frames))

    centred = "transform-box:fill-box;transform-origin:center"
    hidden = 'opacity="0"'  # transient pieces stay hidden when animations are off

    # --- Timeline (seconds) ---------------------------------------------------
    enemy_shots = [  # (name, from lane, fire time, end time, end x, end y)
        ("b1", 1, 0.30, 1.00, shield_edge + 4, mid),
        ("b2", 0, 1.10, 1.75, shield_edge + 4, mid - 4),
        ("b3", 2, 1.40, 2.10, shield_edge + 4, mid + 4),
        ("b4", 1, 3.60, 4.70, -40, mid),  # dodged: flies through the empty lane
    ]
    shield_hits = [1.00, 1.75, 2.10]
    ship_shots = [("l0", 0, 3.15, 3.47), ("l2", 2, 4.10, 4.42)]  # (name, lane, fire, hit)
    charge_start, beam_on, beam_off = 5.10, 5.95, 6.45
    hits = {0: 3.47, 2: 4.42, 1: 6.00}  # when each alien is destroyed
    warps = {0: 7.85, 1: 8.10, 2: 8.35}  # when each alien warps back in
    wave_clear = 6.60

    # --- Ship -------------------------------------------------------------------
    def lane_y(lane: int) -> str:
        return f"transform:translateY({lanes[lane] - mid}px)"

    anim(
        "ship",
        [(0, lane_y(1)), (2.75, lane_y(1)), (3.10, lane_y(0)), (3.65, lane_y(0)),
         (4.05, lane_y(2)), (4.70, lane_y(2)), (5.10, lane_y(1))],
        timing="ease-in-out",
    )
    anim("recoil", [(0, "transform:translateX(0px)"), (beam_on, "transform:translateX(0px)"),
                    (beam_on + 0.05, "transform:translateX(-10px)"), (beam_on + 0.45, "transform:translateX(0px)")],
         timing="ease-out")
    anim("shield", [(0, "opacity:0;transform:scale(.6)"), (0.40, "opacity:0;transform:scale(.6)"),
                    (0.65, "opacity:1;transform:scale(1)"), (2.45, "opacity:1;transform:scale(1)"),
                    (2.70, "opacity:0;transform:scale(1.2)")], extra=centred)
    flare, spark = [], []
    for t in shield_hits:
        flare += blip(t, "opacity:1", "opacity:0", rise=0.04, fall=0.30)
        spark += blip(t, "opacity:1;transform:scale(1)", "opacity:0;transform:scale(.3)", rise=0.04, fall=0.22)
    anim("sflare", flare)
    anim("spark", spark, extra=centred)

    ship = sprite_rects(SHIP, SHIP_COLORS, s)
    flame = sprite_rects(FLAME, FLAME_COLORS, s, x=-4 * s, y=4 * s)
    scx, scy = ship_w / 2, ship_h / 2
    spark_rays = "".join(
        f'<line x1="0" y1="0" x2="{fmt(11 * dx)}" y2="{fmt(11 * dy)}" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round"/>'
        for dx, dy in [(1, 0), (0.7, 0.7), (0.7, -0.7), (0, 1), (0, -1)]
    )
    ship_svg = f"""
  <g transform="translate({ship_x} {mid - ship_h / 2})">
    <g class="ship"><g class="recoil">
      <g class="shield" {hidden}>
        <circle cx="{scx}" cy="{scy}" r="{shield_r}" fill="url(#fshield)" stroke="{CYAN}" stroke-opacity=".9" stroke-width="2.5"/>
        <g class="spin"><circle cx="{scx}" cy="{scy}" r="{shield_r - 6}" fill="none" stroke="{TEAL}" stroke-width="2" stroke-dasharray="4 9" opacity=".8"/></g>
        <circle class="sflare" {hidden} cx="{scx}" cy="{scy}" r="{shield_r}" fill="none" stroke="#ffffff" stroke-width="5"/>
      </g>
      <g class="hover"><g class="flame">{flame}</g>{ship}</g>
      <g transform="translate({scx + shield_r} {scy})"><g class="spark" {hidden}>{spark_rays}<circle r="5" fill="#ffffff"/></g></g>
    </g></g>
  </g>"""

    # --- Enemy fire ---------------------------------------------------------------
    aliens = [
        (BLOB, {"#": PINK, "W": FG, "K": BG}, PINK),
        (SAUCER, {"#": GREEN, "W": CYAN, "Y": YELLOW}, GREEN),
        (URCHIN, {"#": PURPLE, "W": FG}, PURPLE),
    ]
    bolts_svg = []
    for name, lane, t0, t1, ex, ey in enemy_shots:
        sx, sy = alien_x - 6, lanes[lane]
        dx, dy = fmt(ex - sx), fmt(ey - sy)
        anim(name, [(t0, "opacity:0;transform:translate(0px,0px)"), (t0 + 0.01, "opacity:1;transform:translate(0px,0px)"),
                    (t1, f"opacity:1;transform:translate({dx}px,{dy}px)"),
                    (t1 + 0.01, f"opacity:0;transform:translate({dx}px,{dy}px)")])
        color = aliens[lane][2]
        bolts_svg.append(
            f'<g transform="translate({sx} {sy})"><g class="{name}" {hidden}>'
            f'<ellipse cx="10" cy="0" rx="13" ry="3.5" fill="{color}" opacity=".35"/>'
            f'<circle r="8" fill="{color}" opacity=".35"/><circle r="4.5" fill="{color}"/><circle r="2" fill="#ffffff"/></g></g>'
        )
    # Each alien glows for a moment before it fires.
    tells_svg = []
    for lane in range(3):
        times = [t0 for _, ln, t0, *_ in enemy_shots if ln == lane]
        frames: list[Frame] = []
        for t in times:
            frames += [(t - 0.18, "opacity:0;transform:scale(.2)"), (t, "opacity:1;transform:scale(1)"),
                       (t + 0.12, "opacity:0;transform:scale(1.4)")]
        anim(f"tell{lane}", frames, extra=centred)
        color = aliens[lane][2]
        tells_svg.append(
            f'<g transform="translate({alien_x - 4} {lanes[lane]})"><g class="tell{lane}" {hidden}>'
            f'<circle r="10" fill="{color}" opacity=".45"/><circle r="4" fill="#ffffff"/></g></g>'
        )

    # --- Ship fire ------------------------------------------------------------------
    travel = fmt(alien_x - 8 - nose)
    lasers_svg = []
    for name, lane, tf, th in ship_shots:
        anim(name, [(tf, "opacity:0;transform:translateX(0px)"), (tf + 0.01, "opacity:1;transform:translateX(0px)"),
                    (th, f"opacity:1;transform:translateX({travel}px)"), (th + 0.01, f"opacity:0;transform:translateX({travel}px)")])
        anim(f"m{name}", blip(tf, "opacity:.95;transform:scale(1)", "opacity:0;transform:scale(.2)", rise=0.03, fall=0.14),
             extra=centred)
        lasers_svg.append(f"""
  <g transform="translate({nose} {lanes[lane] - 2})">
    <g class="{name}" {hidden}>
      <rect x="0" y="-3" width="34" height="10" rx="5" fill="{TEAL}" opacity=".35"/>
      <rect x="0" y="0" width="34" height="4" rx="2" fill="{CYAN}"/>
      <rect x="20" y="0" width="14" height="4" rx="2" fill="#ffffff"/>
    </g>
    <g class="m{name}" {hidden}><circle r="12" cx="2" cy="2" fill="{CYAN}" opacity=".45"/><circle r="6" cx="2" cy="2" fill="#ffffff"/></g>
  </g>""")

    # Charge-up: an orb grows at the nose while particles are pulled into it.
    anim("orb", [(charge_start, "opacity:0;transform:scale(0)"), (charge_start + 0.05, "opacity:1;transform:scale(.25)"),
                 (beam_on - 0.03, "opacity:1;transform:scale(1.15)"), (beam_on + 0.05, "opacity:0;transform:scale(1.8)")],
         extra=centred)
    pulls = []
    for i in range(10):
        a = math.radians(i * 137.5)
        r = 40 if i % 2 else 54
        px, py = fmt(r * math.cos(a)), fmt(r * math.sin(a))
        t = charge_start + 0.075 * i
        anim(f"pull{i}", [(t, f"opacity:0;transform:translate({px}px,{py}px)"),
                          (t + 0.05, f"opacity:1;transform:translate({px}px,{py}px)"),
                          (t + 0.38, "opacity:0;transform:translate(0px,0px)")], timing="ease-in")
        pulls.append(f'<circle class="pull{i}" {hidden} r="{2.2 if i % 2 else 1.6}" fill="{(CYAN, "#ffffff", TEAL)[i % 3]}"/>')
    anim("beam", [(beam_on, "opacity:0;transform:scaleY(0)"), (beam_on + 0.05, "opacity:1;transform:scaleY(1.35)"),
                  (beam_on + 0.13, "opacity:1;transform:scaleY(1)"), (beam_off - 0.13, "opacity:1;transform:scaleY(.85)"),
                  (beam_off, "opacity:0;transform:scaleY(0)")], extra="transform-box:fill-box;transform-origin:0 50%")
    anim("flash", blip(hits[1], "opacity:.22", "opacity:0", rise=0.03, fall=0.30))
    beam_len = fmt(alien_cx + 10 - nose)
    charge_svg = f"""
  <g transform="translate({nose + 6} {mid})">
    <g class="orb" {hidden}><g class="opulse"><circle r="18" fill="{CYAN}" opacity=".35"/><circle r="10" fill="{CYAN}" opacity=".8"/><circle r="5" fill="#ffffff"/></g></g>
    {"".join(pulls)}
  </g>
  <g transform="translate({nose} {mid})">
    <g class="beam" {hidden}><g class="bflick">
      <rect x="0" y="-13" width="{beam_len}" height="26" rx="13" fill="{CYAN}" opacity=".3"/>
      <rect x="0" y="-6" width="{beam_len}" height="12" rx="6" fill="{CYAN}"/>
      <rect x="0" y="-2.5" width="{beam_len}" height="5" rx="2.5" fill="#ffffff"/>
    </g></g>
  </g>"""

    # --- Aliens: destroyed, then warp back in -------------------------------------
    alive = "opacity:1;transform:scale(1)"
    aliens_svg, booms_svg = [], []
    for lane, (sprite, colors, color) in enumerate(aliens):
        hit, warp = hits[lane], warps[lane]
        big = lane == 1  # the beam kill gets the big explosion
        anim(f"a{lane}", [(hit, alive), (hit + 0.08, "opacity:0;transform:scale(1.35)"), (hit + 0.09, "opacity:0;transform:scale(0)"),
                          (warp, "opacity:0;transform:scale(0)"), (warp + 0.25, "opacity:1;transform:scale(1.15)"),
                          (warp + 0.40, alive)], extra=centred)
        anim(f"w{lane}", [(warp - 0.05, "opacity:0;transform:scale(1,0)"), (warp + 0.08, "opacity:1;transform:scale(1,1)"),
                          (warp + 0.30, "opacity:0;transform:scale(6,.15)")], extra=centred)
        ay = lanes[lane] - len(sprite[0]) * s / 2
        f1, f2 = sprite_rects(sprite[0], colors, s), sprite_rects(sprite[1], colors, s)
        aliens_svg.append(f"""
  <g transform="translate({alien_x} {fmt(ay)})">
    <g class="a{lane}"><g class="wig" style="animation-delay:-{fmt(lane * 0.45)}s"><g class="fa">{f1}</g><g class="fb">{f2}</g></g></g>
  </g>
  <g transform="translate({fmt(alien_cx)} {lanes[lane]})"><g class="w{lane}" {hidden}>
    <rect x="-5" y="-26" width="10" height="52" rx="5" fill="{CYAN}" opacity=".4"/><rect x="-1.5" y="-26" width="3" height="52" fill="#ffffff"/>
  </g></g>""")

        grow = 1.6 if big else 1.0
        anim(f"ring{lane}", [(hit, "opacity:0;transform:scale(.2)"), (hit + 0.02, "opacity:1;transform:scale(.4)"),
                             (hit + 0.45 * grow, f"opacity:0;transform:scale({fmt(1.8 * grow)})")], timing="ease-out", extra=centred)
        anim(f"boom{lane}", [(hit, "opacity:0;transform:scale(.3)"), (hit + 0.02, "opacity:1;transform:scale(1)"),
                             (hit + 0.16 * grow, f"opacity:0;transform:scale({fmt(1.5 * grow)})")], timing="ease-out", extra=centred)
        rings = f'<circle class="ring{lane}" {hidden} r="22" fill="none" stroke="{color}" stroke-width="3"/>'
        if big:
            anim("ring1b", [(hit + 0.08, "opacity:0;transform:scale(.2)"), (hit + 0.10, "opacity:.9;transform:scale(.4)"),
                            (hit + 0.75, "opacity:0;transform:scale(2.4)")], timing="ease-out", extra=centred)
            rings += f'<circle class="ring1b" {hidden} r="22" fill="none" stroke="#ffffff" stroke-width="2"/>'
        n_debris = 12 if big else 8
        debris = []
        for j in range(n_debris):
            a = 2 * math.pi * j / n_debris
            dist = (78 if j % 2 else 56) if big else (54 if j % 2 == 0 else 40)
            dx, dy = fmt(dist * math.cos(a)), fmt(dist * math.sin(a))
            name = f"d{lane}_{j}"
            anim(name, [(hit, "opacity:0;transform:translate(0px,0px) rotate(0deg)"),
                        (hit + 0.01, "opacity:1;transform:translate(0px,0px) rotate(0deg)"),
                        (hit + 0.5 * grow, f"opacity:0;transform:translate({dx}px,{dy}px) rotate(120deg)")], timing="ease-out")
            debris.append(f'<rect class="{name}" {hidden} x="-4" y="-4" width="8" height="8" fill="{(color, YELLOW, FG)[j % 3]}"/>')
        points = "+300" if big else "+100"
        pop_scale = 3 if big else 2
        anim(f"pop{lane}", [(hit, "opacity:0;transform:translateY(0px)"), (hit + 0.05, "opacity:1;transform:translateY(-2px)"),
                            (hit + 0.70, "opacity:1;transform:translateY(-18px)"), (hit + 0.90, "opacity:0;transform:translateY(-24px)")],
             timing="ease-out")
        popup = pixel_text_path(points, 0, 0, pop_scale)
        booms_svg.append(f"""
  <g transform="translate({fmt(alien_cx)} {lanes[lane]})">
    {rings}
    <circle class="boom{lane}" {hidden} r="{16 if big else 12}" fill="#ffffff"/>
    {"".join(debris)}
  </g>
  <g transform="translate({fmt(alien_x - text_width(points, pop_scale) - 14)} {lanes[lane] - 26})">
    <path class="pop{lane}" {hidden} d="{popup}" fill="{YELLOW}" shape-rendering="crispEdges"/>
  </g>""")

    # --- WAVE CLEAR! ----------------------------------------------------------------
    clear = []
    for a, b in [(0.0, 0.35), (0.45, 0.80), (0.90, 1.20)]:
        clear += [(wave_clear + a, "opacity:0"), (wave_clear + a + 0.01, "opacity:1"),
                  (wave_clear + b, "opacity:1"), (wave_clear + b + 0.01, "opacity:0")]
    anim("clear", clear)
    wc_scale = 4
    wc_x = (W - text_width("WAVE CLEAR!", wc_scale)) / 2
    wc_svg = (
        f'<g class="clear" {hidden}>'
        f'<path d="{pixel_text_path("WAVE CLEAR!", wc_x + 3, mid - 11, wc_scale)}" fill="#2a2f6b" shape-rendering="crispEdges"/>'
        f'<path d="{pixel_text_path("WAVE CLEAR!", wc_x, mid - 14, wc_scale)}" fill="{YELLOW}" shape-rendering="crispEdges"/></g>'
    )

    # --- HUD and title ----------------------------------------------------------------
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
        svg_open(
            W, H, "Thanks for visiting!",
            "Animated footer: aliens fire at a pixel spaceship, which blocks the shots with a shield, dodges, "
            "shoots back and finishes the wave with a charged beam, over a scrolling starfield, above the text "
            "Thanks for visiting, see you in orbit.",
        )
        + background(W, H, "f")
        + f"""
<defs>
  <linearGradient id="ftitle" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{TEAL}"/>
    <stop offset="0.5" stop-color="{BLUE}"/>
    <stop offset="1" stop-color="{PURPLE}"/>
  </linearGradient>
  <radialGradient id="fshield" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{CYAN}" stop-opacity="0"/>
    <stop offset="0.7" stop-color="{CYAN}" stop-opacity="0.06"/>
    <stop offset="1" stop-color="{CYAN}" stop-opacity="0.35"/>
  </radialGradient>
</defs>
<style>
  .sf{{animation:scroll linear infinite}}
  @keyframes scroll{{from{{transform:translateX(0)}}to{{transform:translateX(-{W}px)}}}}
  .hover{{animation:hover 1.3s ease-in-out infinite alternate}}
  @keyframes hover{{from{{transform:translateY(-3px)}}to{{transform:translateY(3px)}}}}
  .flame{{animation:flicker .12s steps(2) infinite alternate;transform-box:fill-box;transform-origin:100% 50%}}
  @keyframes flicker{{from{{transform:scaleX(.55)}}to{{transform:scaleX(1.3)}}}}
  .spin{{animation:spin 3s linear infinite;{centred}}}
  @keyframes spin{{to{{transform:rotate(360deg)}}}}
  .opulse{{animation:opulse .16s ease-in-out infinite alternate;{centred}}}
  @keyframes opulse{{from{{transform:scale(.8)}}to{{transform:scale(1.1)}}}}
  .bflick{{animation:bflick .07s steps(2) infinite alternate}}
  @keyframes bflick{{from{{opacity:.75}}to{{opacity:1}}}}
  .wig{{animation:wig 1.4s ease-in-out infinite alternate}}
  @keyframes wig{{from{{transform:translateY(-7px)}}to{{transform:translateY(7px)}}}}
  .fa{{animation:fa .9s steps(1) infinite}}
  .fb{{animation:fb .9s steps(1) infinite}}
  @keyframes fa{{0%{{opacity:1}}50%{{opacity:0}}}}
  @keyframes fb{{0%{{opacity:0}}50%{{opacity:1}}}}
  .blink{{animation:blink 1.2s steps(1) infinite}}
  @keyframes blink{{50%{{opacity:.15}}}}
  {"".join(css)}
  {REDUCED_MOTION}
</style>
<g clip-path="url(#fclip)">
  <ellipse cx="520" cy="140" rx="380" ry="120" fill="url(#fneb1)"/>
  <ellipse cx="150" cy="260" rx="260" ry="110" fill="url(#fneb2)"/>
  {"".join(layers)}
  {"".join(aliens_svg)}
  {"".join(tells_svg)}
  {"".join(booms_svg)}
  {"".join(lasers_svg)}
  {charge_svg}
  {ship_svg}
  {"".join(bolts_svg)}
  {wc_svg}
  <path d="{hud_1up}" fill="{PINK}" shape-rendering="crispEdges"/>
  <path d="{hud_name}" fill="{FG}" shape-rendering="crispEdges"/>
  <path d="{hud_lives}" fill="{MUTED}" shape-rendering="crispEdges"/>
  {mini}
  <path d="{title_shadow}" fill="#2a2f6b" shape-rendering="crispEdges"/>
  <path d="{title}" fill="url(#ftitle)" shape-rendering="crispEdges"/>
  <path class="blink" d="{sub}" fill="{YELLOW}" shape-rendering="crispEdges"/>
  <rect class="flash" {hidden} width="{W}" height="{H}" fill="#ffffff"/>
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
