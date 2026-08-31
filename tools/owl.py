from PIL import Image, ImageDraw

def draw_owl(px=600):
    """Redraw assets/owl.svg (viewBox 120x124) as a transparent PNG."""
    S = px/120.0
    W, H = int(120*S), int(124*S)
    im = Image.new('RGBA', (W*4, H*4), (0,0,0,0))   # 4x supersample
    d = ImageDraw.Draw(im)
    k = S*4
    def E(x0,y0,x1,y1,fill): d.ellipse([x0*k,y0*k,x1*k,y1*k], fill=fill)
    def P(pts,fill):          d.polygon([(x*k,y*k) for x,y in pts], fill=fill)
    def L(pts,fill,w):        d.line([(x*k,y*k) for x,y in pts], fill=fill, width=int(w*k), joint='curve')

    INK=(20,33,61,255); INK2=(30,46,82,255); PAPER=(251,250,247,255)
    GOLD=(242,194,48,255); LANE=(0,122,61,255); LANE2=(0,97,47,255)

    E(25,39,95,113, INK)                      # body
    E(40,58,80,110, INK2)                     # belly
    P([(25,70),(18,92),(31,106),(38,88),(36,72)], INK2)   # left wing
    P([(95,70),(102,92),(89,106),(82,88),(84,72)], INK2)  # right wing
    L([(48,110),(48,118)], GOLD, 5); L([(44,118),(52,118)], GOLD, 5)
    L([(72,110),(72,118)], GOLD, 5); L([(68,118),(76,118)], GOLD, 5)
    E(32,52,60,80, PAPER); E(60,52,88,80, PAPER)          # eyes
    E(41.5,60.5,54.5,73.5, INK); E(65.5,60.5,78.5,73.5, INK)
    E(47.8,61.8,52.2,66.2, PAPER); E(71.8,61.8,76.2,66.2, PAPER)
    P([(60,72),(54,82),(66,82)], GOLD)                    # beak
    d.pieslice([22*k,20*k,98*k,96*k], 180, 360, fill=LANE)  # helmet dome
    d.rectangle([22*k,56*k,98*k,62*k], fill=LANE2)          # helmet brim
    for x0,y0,x1,y1 in [(44,30,40,50),(60,26,60,48),(76,30,80,50)]:
        L([(x0,y0),(x1,y1)], LANE2, 4)
    return im.resize((W,H), Image.LANCZOS)

if __name__ == '__main__':
    draw_owl(600).save('owl.png')
    print('owl.png written')
