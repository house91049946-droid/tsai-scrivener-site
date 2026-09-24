#!/usr/bin/env python3
"""產生全站插畫（SVG），輸出到 public/illus/。風格：扁平向量、事務所藍＋暖色。
   跑法：python3 scripts/make-illus.py
"""
import os, math, random

OUT = os.path.join(os.path.dirname(__file__), '..', 'public', 'illus')
os.makedirs(OUT, exist_ok=True)

# 調色盤
BLUE='#1F4E9C'; BLUE_D='#163B78'; BLUE_M='#3A6CC0'; BLUE_L='#C9D8EE'; SKY='#EEF3FA'; SKY2='#DCE6F5'
WHITE='#FFFFFF'; PAPER='#F7F4EC'; INK='#222831'; GREY='#B8C2D3'
SKIN='#F3C9A2'; SKIN2='#E4B48C'; HAIR='#2B2B33'; HAIR_G='#9AA3B2'
WARM='#E9A24C'; WOOD='#C99A6B'; GREEN='#7FB07A'; GREEN_D='#5E9160'; RED='#C8402F'; GOLD='#D9B25C'

def svg(w, h, body, bg=None):
    bgrect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{bgrect}{body}</svg>'

def r(x,y,w,h,f,rx=0,extra=''): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{f}" {extra}/>'
def c(cx,cy,rad,f,extra=''): return f'<circle cx="{cx}" cy="{cy}" r="{rad}" fill="{f}" {extra}/>'
def p(d,f,extra=''): return f'<path d="{d}" fill="{f}" {extra}/>'
def g(body,extra=''): return f'<g {extra}>{body}</g>'
def txt(x,y,s,size,f,extra=''): return f'<text x="{x}" y="{y}" font-size="{size}" fill="{f}" font-family="Noto Sans TC, PingFang TC, sans-serif" {extra}>{s}</text>'

# ---------- 元件 ----------
def house(x, y, w=180, floors=3, body=WHITE, roof=BLUE, win=BLUE_L, arcade=True, tank=True, seed=0):
    """台灣透天厝正面，y 為地面線。"""
    fh = 62
    h = fh*floors + 12
    top = y - h
    s = r(x, top, w, h, body, 4)
    s += r(x, top-10, w, 12, roof, 2)  # 女兒牆
    s += r(x+8, top-4, w-16, 4, BLUE_D)
    if tank:
        s += r(x+w-46, top-44, 30, 30, GREY, 4) + r(x+w-40, top-14, 4, 6, GREY) + r(x+w-26, top-14, 4, 6, GREY)
        s += r(x+w-38, top-50, 14, 8, BLUE_D, 2)
    # 樓層窗
    for f in range(floors):
        fy = top + 12 + f*fh
        if f == floors-1 and arcade:
            # 騎樓：拱門
            s += r(x, fy, w, fh, BLUE_D)
            n = 2
            aw = (w-24)/n
            for i in range(n):
                ax = x+12+i*aw
                s += p(f'M{ax+4} {fy+fh} V{fy+30} a{aw/2-4} {aw/2-4} 0 0 1 {aw-8} 0 V{fy+fh} Z', SKY2)
            s += r(x+w/2-16, fy+fh-38, 32, 38, WOOD, 2)
            s += c(x+w/2+9, fy+fh-18, 2.5, INK)
        else:
            # 陽台欄杆＋兩扇窗
            s += r(x, fy+fh-14, w, 4, BLUE_L)
            for i in range(6):
                s += r(x+10+i*((w-20)/6), fy+fh-14, 3, -12, BLUE_L)
            s += r(x+18, fy+12, w/2-30, 30, win, 2) + r(x+w/2+12, fy+12, w/2-30, 30, win, 2)
            s += r(x+18+(w/2-30)/2-1, fy+12, 2, 30, WHITE) + r(x+w/2+12+(w/2-30)/2-1, fy+12, 2, 30, WHITE)
    # 門牌
    s += r(x+w-30, top+h-fh-20, 18, 8, WARM, 1)
    return s

def person(x, y, h=120, shirt=BLUE, skin=SKIN, hair=HAIR, hair_style='short', skirt=False):
    """站姿人物，x 為中心，y 為腳底。"""
    hw = h*0.19
    hr = h*0.13
    s = ''
    # 腿
    s += r(x-hw*0.75, y-h*0.42, hw*0.6, h*0.42, INK if not skirt else shirt, 4)
    s += r(x+hw*0.15, y-h*0.42, hw*0.6, h*0.42, INK if not skirt else shirt, 4)
    if skirt: s += p(f'M{x-hw*1.1} {y-h*0.16} L{x+hw*1.1} {y-h*0.16} L{x+hw*0.8} {y-h*0.48} L{x-hw*0.8} {y-h*0.48} Z', shirt)
    # 鞋
    s += r(x-hw*0.85, y-8, hw*0.8, 8, INK, 3) + r(x+hw*0.05, y-8, hw*0.8, 8, INK, 3)
    # 身體
    s += r(x-hw, y-h*0.72, hw*2, h*0.34, shirt, hw*0.5)
    # 手臂
    s += r(x-hw-hw*0.42, y-h*0.70, hw*0.42, h*0.26, shirt, hw*0.2) + r(x+hw, y-h*0.70, hw*0.42, h*0.26, shirt, hw*0.2)
    s += c(x-hw-hw*0.21, y-h*0.43, hw*0.22, skin) + c(x+hw+hw*0.21, y-h*0.43, hw*0.22, skin)
    # 頭
    s += r(x-hr*0.35, y-h*0.78, hr*0.7, h*0.09, skin, 3)
    s += c(x, y-h*0.86, hr, skin)
    if hair_style == 'short':
        s += p(f'M{x-hr} {y-h*0.86} a{hr} {hr} 0 0 1 {2*hr} 0 v-{hr*0.15} a{hr} {hr*0.9} 0 0 0 -{2*hr} 0 Z', hair)
        s += p(f'M{x-hr} {y-h*0.86} a{hr} {hr} 0 0 1 {2*hr} 0 l0 4 a{hr} {hr*0.6} 0 0 0 -{2*hr} 0 Z', hair)
    elif hair_style == 'long':
        s += p(f'M{x-hr*1.05} {y-h*0.86+hr*0.9} v-{hr*0.9} a{hr*1.05} {hr*1.05} 0 0 1 {2.1*hr} 0 v{hr*0.9} h-{hr*0.35} v-{hr*0.6} h-{hr*1.4} v{hr*0.6} Z', hair)
    elif hair_style == 'bun':
        s += p(f'M{x-hr} {y-h*0.86} a{hr} {hr} 0 0 1 {2*hr} 0 l0 4 a{hr} {hr*0.6} 0 0 0 -{2*hr} 0 Z', hair) + c(x, y-h*0.86-hr*1.05, hr*0.38, hair)
    elif hair_style == 'child':
        s += p(f'M{x-hr} {y-h*0.86} a{hr} {hr} 0 0 1 {2*hr} 0 l0 2 a{hr} {hr*0.5} 0 0 0 -{2*hr} 0 Z', hair)
    # 臉
    s += c(x-hr*0.35, y-h*0.85, 1.6, INK) + c(x+hr*0.35, y-h*0.85, 1.6, INK)
    s += p(f'M{x-hr*0.3} {y-h*0.86+hr*0.35} q{hr*0.3} {hr*0.25} {hr*0.6} 0', 'none', f'stroke="{INK}" stroke-width="1.5" stroke-linecap="round"')
    return s

def doc(x, y, w=90, h=116, stamp=True, lines=5, glyph=None):
    s = r(x+4, y+6, w, h, '#E2DDD1', 4) + r(x, y, w, h, WHITE, 4, f'stroke="{BLUE_L}" stroke-width="2"')
    for i in range(lines):
        lw = w*0.62 if i else w*0.42
        s += r(x+12, y+18+i*16, lw, 5, BLUE_L if i else BLUE, 2)
    if stamp:
        s += g(r(x+w-40, y+h-42, 30, 30, 'none', 3, f'stroke="{RED}" stroke-width="3"') + txt(x+w-25, y+h-20, glyph or '印', 16, RED, 'text-anchor="middle" font-weight="700"'), f'transform="rotate(-12 {x+w-25} {y+h-27})"')
    return s

def tree(x, y, s=1.0):
    return r(x-5*s, y-40*s, 10*s, 40*s, WOOD, 3) + c(x, y-62*s, 26*s, GREEN) + c(x-16*s, y-46*s, 18*s, GREEN_D) + c(x+16*s, y-48*s, 18*s, GREEN)

def cloud(x, y, s=1.0, f=WHITE):
    return c(x, y, 18*s, f) + c(x+20*s, y-6*s, 24*s, f) + c(x+44*s, y+2*s, 16*s, f) + r(x-6*s, y, 60*s, 16*s, f, 8)

def coin(x, y, rad=14):
    return c(x, y, rad, GOLD) + c(x, y, rad-4, '#EBC97A') + txt(x, y+rad*0.4, '$', rad*1.1, '#B8912E', 'text-anchor="middle" font-weight="700"')

def key(x, y, s=1.0, rot=-30):
    body = c(x, y, 16*s, GOLD) + c(x, y, 7*s, WHITE) + r(x+12*s, y-4*s, 46*s, 8*s, GOLD, 3) + r(x+46*s, y+4*s, 6*s, 10*s, GOLD) + r(x+34*s, y+4*s, 6*s, 8*s, GOLD)
    return g(body, f'transform="rotate({rot} {x} {y})"')

def calculator(x, y, w=70, h=92):
    s = r(x, y, w, h, BLUE_D, 6) + r(x+8, y+8, w-16, 22, SKY2, 3)
    for i in range(3):
        for j in range(3):
            s += r(x+9+j*((w-18)/3), y+38+i*16, (w-18)/3-4, 11, BLUE_L if (i,j)!=(2,2) else WARM, 2)
    return s

def skyline(w, h, y_ground, seed=3, dark=BLUE_D, mid=BLUE, light=BLUE_M):
    """城市剪影三層。"""
    random.seed(seed); s=''
    for layer,(col,scale,off) in enumerate([(light,0.55,0),(mid,0.8,0),(dark,1.0,0)]):
        x = -20
        while x < w+40:
            bw = random.randint(46,110)*scale
            bh = random.randint(60,180)*scale + layer*20
            top = y_ground - bh
            s += r(x, top, bw, bh, col, 2)
            if random.random()<0.6: s += r(x+bw-22*scale, top-16*scale, 14*scale, 16*scale, col, 2)
            if layer==2:
                for wy in range(int(top)+14, int(y_ground)-10, 22):
                    for wx in range(int(x)+10, int(x+bw)-12, 20):
                        if random.random()<0.55: s += r(wx, wy, 9, 11, '#5A83C9', 1, 'opacity="0.55"')
            x += bw + random.randint(6,18)
    return s

# ---------- 場景 ----------
def hero():
    W,H = 1600, 640
    s = f'<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#EAF0FA"/><stop offset="1" stop-color="#F8FAFD"/></linearGradient></defs>'
    s += r(0,0,W,H,'url(#sky)')
    s += c(1320, 120, 54, '#FFE7B3')
    s += cloud(180, 110, 1.3) + cloud(560, 70, 1.0) + cloud(1050, 130, 1.1)
    s += g(skyline(W, H, 470, seed=7, dark='#B9CBE8', mid='#CBD9EE', light='#DCE6F5'), 'opacity="0.9"')
    ground = 520
    s += r(0, ground, W, H-ground, '#DCE6F5')          # 地面
    s += r(0, ground, W, 6, BLUE_L)
    # 房子群
    s += house(150, ground, 200, 3, seed=1)
    s += house(370, ground, 170, 2, body=PAPER, roof=BLUE_M, tank=False)
    s += house(1150, ground, 210, 3, body='#F3F0E8', roof=BLUE_D)
    s += house(1380, ground, 160, 2, body=WHITE, roof=BLUE_M, tank=False)
    s += tree(600, ground+6, 1.1) + tree(1100, ground+6, 0.9) + tree(1560, ground+6, 1.0)
    # 人物：阿公、阿嬤、成年子女、小孩 拿文件
    s += person(720, ground+4, 150, shirt='#5B7BB5', hair=HAIR_G, hair_style='short')
    s += person(800, ground+4, 140, shirt='#D98A8A', hair=HAIR_G, hair_style='bun', skirt=True)
    s += person(895, ground+4, 160, shirt=BLUE, hair=HAIR, hair_style='short')
    s += person(965, ground+4, 90, shirt=WARM, hair=HAIR, hair_style='child')
    s += doc(930, ground-190, 78, 100, glyph='稅')
    s += key(1040, ground-150, 0.9, -40)
    # 路面
    s += r(0, ground+70, W, 3, '#C4D2E8')
    return svg(W,H,s)

def banner_bg():
    W,H = 1600, 300
    s = f'<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#1B437F"/><stop offset="1" stop-color="#3A6CC0"/></linearGradient></defs>'
    s += r(0,0,W,H,'url(#bg)')
    s += c(1350, 70, 40, '#FFFFFF', 'opacity="0.12"') + cloud(200, 60, 1.4, '#FFFFFF') .replace('fill="#FFFFFF"','fill="#FFFFFF" opacity="0.10"')
    s += skyline(W, H, 300, seed=11, dark='#12305F', mid='#1A4489', light='#2A5AA8')
    return svg(W,H,s)

def cover(kind):
    """文章封面 800x400，五類。"""
    W,H = 800, 400
    s = r(0,0,W,H,SKY)
    s += c(650, 80, 34, '#FFE7B3') + cloud(90, 70, 1.0) + cloud(520, 50, 0.8)
    ground = 330
    s += r(0, ground, W, H-ground, SKY2)
    if kind == 'tax':      # 稅務：計算機、文件、硬幣、人
        s += house(80, ground, 170, 2, tank=False)
        s += doc(330, 150, 120, 150, glyph='稅')
        s += calculator(470, 200)
        s += coin(560, 300) + coin(590, 300) + coin(575, 275)
        s += person(690, ground+4, 150, shirt=BLUE)
    elif kind == 'inherit': # 繼承：房子＋三代
        s += house(300, ground, 200, 3)
        s += person(150, ground+4, 140, shirt='#5B7BB5', hair=HAIR_G)
        s += person(225, ground+4, 130, shirt='#D98A8A', hair=HAIR_G, hair_style='bun', skirt=True)
        s += person(600, ground+4, 155, shirt=BLUE)
        s += person(670, ground+4, 90, shirt=WARM, hair_style='child')
        s += doc(520, 150, 80, 100, glyph='繼')
    elif kind == 'gift':    # 贈與：長輩把鑰匙交給子女
        s += house(500, ground, 200, 2, body=PAPER)
        s += person(220, ground+4, 150, shirt='#5B7BB5', hair=HAIR_G)
        s += person(360, ground+4, 155, shirt=BLUE)
        s += key(292, ground-110, 1.1, -20)
        s += r(255, ground-30, 70, 12, WARM, 6) .replace('fill', 'opacity="0" fill')
        s += doc(110, 130, 80, 100, glyph='贈')
        s += coin(620, 300) + coin(650, 300)
    elif kind == 'transfer': # 買賣過戶：簽約桌
        s += house(560, ground, 190, 3, body=WHITE)
        s += r(150, ground-70, 300, 14, WOOD, 4) + r(170, ground-56, 14, 56, WOOD) + r(416, ground-56, 14, 56, WOOD)
        s += doc(250, ground-160, 100, 90, glyph='約', lines=4)
        s += person(140, ground+4, 150, shirt=BLUE)
        s += person(470, ground+4, 150, shirt='#5B7BB5', hair_style='long')
        s += key(330, ground-100, 0.8, 20)
    elif kind == 'mortgage': # 抵押設定：房子＋鎖、銀行
        s += house(120, ground, 190, 3)
        s += r(420, ground-150, 220, 150, WHITE, 4) + r(420, ground-166, 220, 18, BLUE_D, 2)
        for i in range(4): s += r(440+i*52, ground-140, 16, 130, BLUE_L, 2)
        s += txt(530, ground-172, '銀行', 18, WHITE, 'text-anchor="middle" font-weight="700"')
        s += r(300, ground-120, 46, 40, GOLD, 6) + p(f'M312 {ground-120} v-18 a11 11 0 0 1 22 0 v18', 'none', f'stroke="{GOLD}" stroke-width="7"') + c(323, ground-100, 5, INK)
        s += person(700, ground+4, 150, shirt=BLUE)
    return svg(W,H,s)

def service(kind):
    """服務卡插圖 400x220。"""
    W,H = 400, 220
    s = r(0,0,W,H,SKY)
    ground = 190
    s += r(0, ground, W, H-ground, SKY2)
    if kind == 'estate':
        s += house(40, ground, 120, 2, tank=False) + doc(200, 60, 90, 110, glyph='稅') + coin(330, 170) + coin(355, 170) + coin(342, 148)
    elif kind == 'gift':
        s += person(90, ground+2, 120, shirt='#5B7BB5', hair=HAIR_G) + person(200, ground+2, 125, shirt=BLUE) + key(145, ground-88, 0.9, -20) + house(260, ground, 110, 2, body=PAPER, tank=False)
    elif kind == 'inherit':
        s += house(150, ground, 130, 3) + person(80, ground+2, 110, shirt='#5B7BB5', hair=HAIR_G) + person(330, ground+2, 115, shirt=BLUE) + person(370, ground+2, 70, shirt=WARM, hair_style='child')
    elif kind == 'plan':
        s += r(40, 150, 320, 4, BLUE_L, 2)
        for i,x in enumerate([70, 200, 330]):
            s += c(x, 152, 9, BLUE) + house(x-40, 140, 80, 1 if i<2 else 2, tank=False, arcade=False)
        s += doc(290, 30, 70, 88, glyph='傳', lines=4)
    elif kind == 'ptax':
        s += house(50, ground, 130, 3) + p('M230 150 L300 80 L330 110 L390 50', 'none', f'stroke="{BLUE}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"') + p('M365 50 L390 50 L390 75', 'none', f'stroke="{BLUE}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"') + txt(270, 200, '%', 42, WARM, 'font-weight="700"')
    elif kind == 'transfer':
        s += house(230, ground, 130, 2, body=WHITE, tank=False) + doc(60, 60, 90, 100, glyph='約', lines=4) + key(180, 120, 0.9, -30)
    return svg(W,H,s)

def flow_icon(kind):
    W=120; s=''
    if kind == 'phone':
        s += p('M38 26c-4 0-8 4-8 8 0 30 26 56 56 56 4 0 8-4 8-8v-10l-16-6-8 8c-10-4-18-12-22-22l8-8-6-16z', BLUE)
    elif kind == 'calc':
        s += calculator(35, 18, 50, 84)
    elif kind == 'sign':
        s += doc(30, 22, 62, 78, glyph='約', lines=4) + p('M70 92 l30-30 6 6-30 30-8 2z', WARM)
    elif kind == 'folder':
        s += p('M20 34h30l10 10h40v46H20z', BLUE) + r(20, 50, 80, 40, BLUE_M, 3) + r(40, 62, 40, 5, WHITE, 2) + r(40, 72, 28, 5, WHITE, 2)
    elif kind == 'done':
        s += c(60, 60, 34, BLUE) + p('M42 60 l12 12 24-26', 'none', f'stroke="{WHITE}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"')
    return svg(W,W,s)

files = {
    'hero.svg': hero(),
    'banner-bg.svg': banner_bg(),
    'cover-tax.svg': cover('tax'), 'cover-inherit.svg': cover('inherit'), 'cover-gift.svg': cover('gift'),
    'cover-transfer.svg': cover('transfer'), 'cover-mortgage.svg': cover('mortgage'),
    'svc-estate.svg': service('estate'), 'svc-gift.svg': service('gift'), 'svc-inherit.svg': service('inherit'),
    'svc-plan.svg': service('plan'), 'svc-ptax.svg': service('ptax'), 'svc-transfer.svg': service('transfer'),
    'flow-phone.svg': flow_icon('phone'), 'flow-calc.svg': flow_icon('calc'), 'flow-sign.svg': flow_icon('sign'),
    'flow-folder.svg': flow_icon('folder'), 'flow-done.svg': flow_icon('done'),
}
for name, content in files.items():
    with open(os.path.join(OUT, name), 'w') as f: f.write(content)
print('wrote', len(files), 'files to', os.path.abspath(OUT))
