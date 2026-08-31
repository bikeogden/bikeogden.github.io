#!/usr/bin/env python3
"""
Make a QR code as an SVG file. No libraries needed beyond Python itself.

    python3 make-qr.py "https://example.com" output.svg

Optional third argument sets the error-correction level: L, M, Q or H.
Q is the default and is the right choice for a printed flyer -- it survives
being folded, rained on, and photographed at an angle.
"""

import sys

# ---------------------------------------------------------------- tables
TOTAL_CODEWORDS = {1:26, 2:44, 3:70, 4:100, 5:134,
                   6:172, 7:196, 8:242, 9:292, 10:346}

# level -> version -> (ec_per_block, [(block_count, data_codewords), ...])
BLOCKS = {
 'L': {1:(7,[(1,19)]), 2:(10,[(1,34)]), 3:(15,[(1,55)]), 4:(20,[(1,80)]),
       5:(26,[(1,108)]), 6:(18,[(2,68)]), 7:(20,[(2,78)]), 8:(24,[(2,97)]),
       9:(30,[(2,116)]), 10:(18,[(2,68),(2,69)])},
 'M': {1:(10,[(1,16)]), 2:(16,[(1,28)]), 3:(26,[(1,44)]), 4:(18,[(2,32)]),
       5:(24,[(2,43)]), 6:(16,[(4,27)]), 7:(18,[(4,31)]),
       8:(22,[(2,38),(2,39)]), 9:(22,[(3,36),(2,37)]), 10:(26,[(4,43),(1,44)])},
 'Q': {1:(13,[(1,13)]), 2:(22,[(1,22)]), 3:(18,[(2,17)]), 4:(26,[(2,24)]),
       5:(18,[(2,15),(2,16)]), 6:(24,[(4,19)]), 7:(18,[(2,14),(4,15)]),
       8:(22,[(4,18),(2,19)]), 9:(20,[(4,16),(4,17)]), 10:(24,[(6,19),(2,20)])},
 'H': {1:(17,[(1,9)]), 2:(28,[(1,16)]), 3:(22,[(2,13)]), 4:(16,[(4,9)]),
       5:(22,[(2,11),(2,12)]), 6:(28,[(4,15)]), 7:(26,[(4,13),(1,14)]),
       8:(26,[(4,14),(2,15)]), 9:(24,[(4,12),(4,13)]), 10:(28,[(6,15),(2,16)])},
}

ALIGN = {1:[], 2:[6,18], 3:[6,22], 4:[6,26], 5:[6,30],
         6:[6,34], 7:[6,22,38], 8:[6,24,42], 9:[6,26,46], 10:[6,28,50]}

EC_BITS = {'L':0b01, 'M':0b00, 'Q':0b11, 'H':0b10}

# ---------------------------------------------------------------- GF(256)
EXP = [0]*512
LOG = [0]*256
_x = 1
for _i in range(255):
    EXP[_i] = _x
    LOG[_x] = _i
    _x <<= 1
    if _x & 0x100:
        _x ^= 0x11D
for _i in range(255, 512):
    EXP[_i] = EXP[_i-255]

def gf_mul(a, b):
    if a == 0 or b == 0:
        return 0
    return EXP[LOG[a] + LOG[b]]

def rs_generator(n):
    g = [1]
    for i in range(n):
        g2 = [0]*(len(g)+1)
        for j, c in enumerate(g):
            g2[j]   ^= gf_mul(c, 1)
            g2[j+1] ^= gf_mul(c, EXP[i])
        g = g2
    return g

def rs_encode(data, n):
    gen = rs_generator(n)
    rem = [0]*n
    for byte in data:
        factor = byte ^ rem[0]
        rem = rem[1:] + [0]
        for i, c in enumerate(gen[1:]):
            rem[i] ^= gf_mul(c, factor)
    return rem

# ---------------------------------------------------------------- encode
def choose_version(nbytes, level):
    for v in range(1, 11):
        ec, blocks = BLOCKS[level][v]
        cap = sum(cnt*dw for cnt, dw in blocks)
        header = 4 + (8 if v < 10 else 16)
        if nbytes + (header + 7)//8 <= cap:
            return v
    raise ValueError('Text too long for this generator (max version 10). '
                     'Shorten the URL or use a lower error-correction level.')

def build_codewords(text, level):
    raw = text.encode('utf-8')
    version = choose_version(len(raw), level)
    ec_len, blocks = BLOCKS[level][version]
    capacity = sum(cnt*dw for cnt, dw in blocks)

    bits = []
    def put(val, n):
        for i in range(n-1, -1, -1):
            bits.append((val >> i) & 1)

    put(0b0100, 4)                                  # byte mode
    put(len(raw), 8 if version < 10 else 16)
    for b in raw:
        put(b, 8)
    put(0, min(4, capacity*8 - len(bits)))          # terminator
    while len(bits) % 8:
        bits.append(0)

    codewords = [int(''.join(map(str, bits[i:i+8])), 2)
                 for i in range(0, len(bits), 8)]
    pad = [0xEC, 0x11]
    while len(codewords) < capacity:
        codewords.append(pad[(len(codewords) - len(bits)//8) % 2])

    # split into blocks, compute ECC
    data_blocks, ec_blocks, pos = [], [], 0
    for cnt, dw in blocks:
        for _ in range(cnt):
            blk = codewords[pos:pos+dw]
            pos += dw
            data_blocks.append(blk)
            ec_blocks.append(rs_encode(blk, ec_len))

    # interleave
    out = []
    for i in range(max(len(b) for b in data_blocks)):
        for b in data_blocks:
            if i < len(b):
                out.append(b[i])
    for i in range(ec_len):
        for b in ec_blocks:
            out.append(b[i])
    return version, out

# ---------------------------------------------------------------- matrix
def make_matrix(version, codewords, level):
    size = version*4 + 17
    m = [[None]*size for _ in range(size)]

    def finder(r, c):
        for dr in range(-1, 8):
            for dc in range(-1, 8):
                rr, cc = r+dr, c+dc
                if 0 <= rr < size and 0 <= cc < size:
                    inring = (0 <= dr <= 6 and 0 <= dc <= 6)
                    on = inring and (dr in (0,6) or dc in (0,6) or
                                     (2 <= dr <= 4 and 2 <= dc <= 4))
                    m[rr][cc] = 1 if on else 0
    finder(0, 0); finder(0, size-7); finder(size-7, 0)

    for i in range(8, size-8):                      # timing
        v = 1 if i % 2 == 0 else 0
        m[6][i] = v
        m[i][6] = v

    for r in ALIGN[version]:                        # alignment
        for c in ALIGN[version]:
            if (r < 8 and c < 8) or (r < 8 and c > size-9) or (r > size-9 and c < 8):
                continue
            for dr in range(-2, 3):
                for dc in range(-2, 3):
                    m[r+dr][c+dc] = 1 if (abs(dr) == 2 or abs(dc) == 2
                                          or (dr == 0 and dc == 0)) else 0

    m[size-8][8] = 1                                # dark module

    reserved = [[m[r][c] is not None for c in range(size)] for r in range(size)]
    for i in range(9):                              # format areas
        if m[8][i] is None: reserved[8][i] = True
        if m[i][8] is None: reserved[i][8] = True
    for i in range(8):
        reserved[8][size-1-i] = True
        reserved[size-1-i][8] = True
    if version >= 7:
        for i in range(6):
            for j in range(3):
                reserved[size-11+j][i] = True
                reserved[i][size-11+j] = True

    # place data, zigzag from bottom right
    bits = [(cw >> i) & 1 for cw in codewords for i in range(7, -1, -1)]
    idx, col, upward = 0, size-1, True
    while col > 0:
        if col == 6:
            col -= 1
        rows = range(size-1, -1, -1) if upward else range(size)
        for r in rows:
            for c in (col, col-1):
                if not reserved[r][c]:
                    m[r][c] = bits[idx] if idx < len(bits) else 0
                    idx += 1
        col -= 2
        upward = not upward

    # masking
    def mask_fn(k, r, c):
        return [lambda r,c: (r+c) % 2 == 0,
                lambda r,c: r % 2 == 0,
                lambda r,c: c % 3 == 0,
                lambda r,c: (r+c) % 3 == 0,
                lambda r,c: (r//2 + c//3) % 2 == 0,
                lambda r,c: (r*c) % 2 + (r*c) % 3 == 0,
                lambda r,c: ((r*c) % 2 + (r*c) % 3) % 2 == 0,
                lambda r,c: ((r+c) % 2 + (r*c) % 3) % 2 == 0][k](r, c)

    def penalty(g):
        p = 0
        for line in list(g) + [list(x) for x in zip(*g)]:
            run, prev = 1, line[0]
            for v in line[1:]:
                if v == prev:
                    run += 1
                else:
                    if run >= 5: p += 3 + (run-5)
                    run, prev = 1, v
            if run >= 5: p += 3 + (run-5)
        for r in range(size-1):
            for c in range(size-1):
                if g[r][c] == g[r][c+1] == g[r+1][c] == g[r+1][c+1]:
                    p += 3
        dark = sum(sum(row) for row in g)
        p += 10 * (abs(dark*100 // (size*size) - 50) // 5)
        return p

    best, best_grid, best_p = 0, None, None
    for k in range(8):
        g = [[(m[r][c] ^ 1) if (not reserved[r][c] and mask_fn(k, r, c)) else m[r][c]
              for c in range(size)] for r in range(size)]
        fmt = (EC_BITS[level] << 3) | k
        rem = fmt << 10
        while rem.bit_length() > 10:
            rem ^= 0b10100110111 << (rem.bit_length() - 11)
        fmt15 = ((fmt << 10) | rem) ^ 0b101010000010010
        fbits = [(fmt15 >> i) & 1 for i in range(14, -1, -1)]
        coords1 = [(8,0),(8,1),(8,2),(8,3),(8,4),(8,5),(8,7),(8,8),
                   (7,8),(5,8),(4,8),(3,8),(2,8),(1,8),(0,8)]
        coords2 = [(size-1,8),(size-2,8),(size-3,8),(size-4,8),(size-5,8),
                   (size-6,8),(size-7,8),(8,size-8),(8,size-7),(8,size-6),
                   (8,size-5),(8,size-4),(8,size-3),(8,size-2),(8,size-1)]
        for (r,c),b in zip(coords1, fbits): g[r][c] = b
        for (r,c),b in zip(coords2, fbits): g[r][c] = b
        if version >= 7:
            vrem = version << 12
            while vrem.bit_length() > 12:
                vrem ^= 0b1111100100101 << (vrem.bit_length() - 13)
            v18 = (version << 12) | vrem
            for i in range(18):
                b = (v18 >> i) & 1
                g[size-11 + i%3][i//3] = b
                g[i//3][size-11 + i%3] = b
        p = penalty(g)
        if best_p is None or p < best_p:
            best_p, best_grid, best = p, g, k
    return best_grid

def to_svg(grid, box=10, quiet=6):
    size = len(grid)
    dim = (size + quiet*2) * box
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {dim} {dim}" '
             f'width="{dim}" height="{dim}" shape-rendering="crispEdges">',
             f'<rect width="{dim}" height="{dim}" fill="#ffffff"/>',
             '<g fill="#000000">']
    for r in range(size):
        c = 0
        while c < size:
            if grid[r][c]:
                start = c
                while c < size and grid[r][c]:
                    c += 1
                parts.append(f'<rect x="{(start+quiet)*box}" y="{(r+quiet)*box}" '
                             f'width="{(c-start)*box}" height="{box}"/>')
            else:
                c += 1
    parts.append('</g></svg>')
    return '\n'.join(parts)

def make(text, level='Q'):
    version, cws = build_codewords(text, level)
    return version, make_matrix(version, cws, level)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    text, out = sys.argv[1], sys.argv[2]
    level = sys.argv[3].upper() if len(sys.argv) > 3 else 'Q'
    version, grid = make(text, level)
    open(out, 'w').write(to_svg(grid))
    print(f'Wrote {out}  (version {version}, error correction {level})')
    print(f'Encodes: {text}')
