# Script to check color contrast ratios in CSS variables for light and dark themes.
import re
import colorsys
from pathlib import Path

CSS_PATH = Path(__file__).parent.parent / 'frontend' / 'static' / 'css' / 'layout.css'

VAR_RE = re.compile(r'--([\w-]+)\s*:\s*([^;]+);')
BLOCK_RE = re.compile(r'(?s)([^\{]+)\{([^}]+)\}')


def hex_to_rgb(hexcol):
    hexcol = hexcol.strip()
    if hexcol.startswith('rgb'):
        # handle rgb(a)
        m = re.match(r'rgba?\(([^)]+)\)', hexcol)
        if m:
            parts = [p.strip() for p in m.group(1).split(',')]
            r = int(parts[0]); g = int(parts[1]); b = int(parts[2])
            return (r/255.0, g/255.0, b/255.0)
    if hexcol.startswith('#'):
        h = hexcol.lstrip('#')
        if len(h) == 3:
            h = ''.join([c*2 for c in h])
        r = int(h[0:2], 16)
        g = int(h[2:4], 16)
        b = int(h[4:6], 16)
        return (r/255.0, g/255.0, b/255.0)
    # fallback try named colors? Not handling full list here.
    raise ValueError(f'Unsupported color format: {hexcol}')


def rgb_to_hex(rgb):
    r = int(round(rgb[0]*255))
    g = int(round(rgb[1]*255))
    b = int(round(rgb[2]*255))
    return '#{:02x}{:02x}{:02x}'.format(r,g,b)


def srgb_to_linear(c):
    # c in 0..1
    if c <= 0.03928:
        return c/12.92
    return ((c+0.055)/1.055) ** 2.4


def rel_luminance(rgb):
    r,l,g = rgb[0],rgb[1],rgb[2]
    R = srgb_to_linear(r)
    G = srgb_to_linear(l)
    B = srgb_to_linear(g)
    return 0.2126*R + 0.7152*G + 0.0722*B


def contrast_ratio(c1, c2):
    L1 = rel_luminance(c1)
    L2 = rel_luminance(c2)
    lighter = max(L1,L2)
    darker = min(L1,L2)
    return (lighter + 0.05) / (darker + 0.05)


def parse_css_vars(css_text):
    # parse :root and explicit .theme-light/.theme-dark blocks
    vars_default = {}
    vars_light = {}
    vars_dark = {}

    # find :root block
    for m in BLOCK_RE.finditer(css_text):
        selector = m.group(1).strip()
        body = m.group(2)
        if selector.endswith(':root') or selector == ':root':
            for vm in VAR_RE.finditer(body):
                vars_default[vm.group(1)] = vm.group(2).strip()

    # parse .theme-light and .theme-dark single-line blocks too
    # simple approach: find occurrences of '.theme-light{...}' or '.theme-dark{...}'
    tl = re.search(r'\.theme-light\s*\{([^}]*)\}', css_text)
    td = re.search(r'\.theme-dark\s*\{([^}]*)\}', css_text)
    if tl:
        for vm in VAR_RE.finditer(tl.group(1)):
            vars_light[vm.group(1)] = vm.group(2).strip()
    if td:
        for vm in VAR_RE.finditer(td.group(1)):
            vars_dark[vm.group(1)] = vm.group(2).strip()

    # Also inspect @media (prefers-color-scheme: dark) :root override
    media_dark = re.search(r"@media\s*\(prefers-color-scheme:\s*dark\)\s*\{[^}]*:root\s*\{([^}]*)\}", css_text, re.S)
    if media_dark:
        for vm in VAR_RE.finditer(media_dark.group(1)):
            vars_dark[vm.group(1)] = vm.group(2).strip()

    return vars_default, vars_light, vars_dark


def adjust_color_to_contrast(fg_hex, bg_hex, target_ratio=4.5, prefer_darker=True):
    # adjust fg color towards black or white by changing lightness until contrast meets target
    try:
        fg_rgb = hex_to_rgb(fg_hex)
        bg_rgb = hex_to_rgb(bg_hex)
    except Exception as e:
        return None
    # convert fg_rgb to hls
    r,g,b = fg_rgb
    h,l,s = colorsys.rgb_to_hls(r,g,b)
    step = 0.02
    max_iter = 100
    for i in range(max_iter):
        cur = (r,g,b)
        ratio = contrast_ratio(cur, bg_rgb)
        if ratio >= target_ratio:
            return rgb_to_hex(cur)
        # adjust lightness
        if prefer_darker:
            l = max(0.0, l - step)
        else:
            l = min(1.0, l + step)
        r,g,b = colorsys.hls_to_rgb(h,l,s)
    # failed
    return rgb_to_hex((r,g,b))


def run_checks():
    css = CSS_PATH.read_text(encoding='utf-8')
    vars_default, vars_light, vars_dark = parse_css_vars(css)
    print('Found variables in :root (sample):')
    for k in ['bg','card','text-primary','muted','accent']:
        print(f'  --{k}:', vars_default.get(k,'(none)'))
    print('\nLight theme overrides (sample):')
    for k in ['text-primary','bg','card','accent']:
        print(f'  --{k}:', vars_light.get(k,vars_default.get(k)))
    print('\nDark theme overrides (sample):')
    for k in ['text-primary','bg','card','accent']:
        print(f'  --{k}:', vars_dark.get(k,vars_default.get(k)))

    # helper to resolve var from light/dark or default
    def resolve(varname, theme='light'):
        if theme == 'dark':
            return vars_dark.get(varname, vars_default.get(varname))
        return vars_light.get(varname, vars_default.get(varname))

    checks = []
    # pairs to check: text-primary vs bg, text-primary vs card, muted vs card, white vs accent, accent vs card
    for theme in ['light','dark']:
        bg = resolve('bg', theme)
        card = resolve('card', theme)
        text = resolve('text-primary', theme)
        muted = resolve('muted', theme)
        accent = resolve('accent', theme)
        accent_contrast = resolve('accent-contrast', theme)
        theme_label = theme.upper()
        print(f'\n=== {theme_label} THEME ===')
        pairs = [
            ('page text (text-primary)', text, 'page background', bg),
            ('heading on card (text-primary)', text, 'card background', card),
            ('muted on card (muted)', muted, 'card background', card),
            ('white on accent (button filled)', '#ffffff', 'accent', accent),
            ('white on accent-contrast (filled via --accent-contrast)', '#ffffff', 'accent-contrast', accent_contrast),
            ('accent on card (button border/default)', accent, 'card background', card),
        ]
        for name, fg, _, bgc in pairs:
            try:
                fg_rgb = hex_to_rgb(fg)
                bg_rgb = hex_to_rgb(bgc)
            except Exception as e:
                print(f'  SKIP {name}: cannot parse colors ({fg} / {bgc})')
                continue
            ratio = contrast_ratio(fg_rgb, bg_rgb)
            aa = ratio >= 4.5
            aa_large = ratio >= 3.0
            aaa = ratio >= 7.0
            aaa_large = ratio >= 4.5
            print(f'  {name}: {fg} on {bgc} -> contrast {ratio:.2f} :1 | AA: {aa} | AAA: {aaa} | AA large: {aa_large} | AAA large: {aaa_large}')
            if not aa:
                # propose adjustment for fg
                # decide direction: if fg is darker than bg, make fg darker; else lighter
                Lfg = rel_luminance(fg_rgb)
                Lbg = rel_luminance(bg_rgb)
                prefer_darker = Lfg > Lbg
                suggestion = adjust_color_to_contrast(fg, bgc, 4.5, prefer_darker=prefer_darker)
                print(f'    -> Suggest {suggestion} to reach AA (4.5:1)')

if __name__ == '__main__':
    try:
        print('Using CSS path:', CSS_PATH)
        print('Exists:', CSS_PATH.exists())
        run_checks()
    except Exception as e:
        import traceback
        traceback.print_exc()
        print('Error:', e)
