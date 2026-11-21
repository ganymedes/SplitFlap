# Bottom view of the module PCB (mirrored left-right), from pcb/PCB_PCB_SplitFlap_2023-06-04.json pad positions.
# Usage: python3 bottom_svg.py bottom.svg (used by guide.html)
# Units: EasyEDA (10 mil = 0.254 mm). X = 4177.48 - x, Y = y - 3113.04
import sys
W, H = 157.48, 314.96
M = 12
def P(x, y): return (round(4177.48 - x, 2), round(y - 3113.04, 2))
out = []
a = out.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-M} {-M} {W+2*M} {H+2*M}" font-family="Helvetica, Arial, sans-serif">')
a('<defs><style>.pl{fill:#fff;font-size:4.6px;font-weight:600}.cl{fill:#cfe0ff;font-size:5.5px;font-weight:700;letter-spacing:.2px}'
  '.ml{font-size:5.6px;font-weight:700}.pad{fill:#d9b54a;stroke:#8a6d1a;stroke-width:.6}.hole{fill:#f4f4f4;stroke:#bbb;stroke-width:.5}</style></defs>')
a(f'<rect x="0" y="0" width="{W}" height="{H}" rx="4" fill="#1f4396" stroke="#0d2763" stroke-width="1"/>')
for x, y in [(4031.811, 3124.851), (4165.669, 3124.851), (4031.811, 3416.189), (4165.669, 3416.189)]:
    X, Y = P(x, y); a(f'<circle class="hole" cx="{X}" cy="{Y}" r="4.6"/><circle cx="{X}" cy="{Y}" r="3.1" fill="#fff"/>')
# D1 Mini outline (dashed) and 9-pin header outline
xa, xb = P(4128.961, 0)[0], P(4038.961, 0)[0]
a(f'<rect x="{xa-9}" y="{P(0,3184.339)[1]-27}" width="{xb-xa+18}" height="{70+27+38}" rx="6" fill="none" stroke="#9fb7ec" stroke-width=".8" stroke-dasharray="3 2"/>')
a(f'<text class="cl" x="{(xa+xb)/2}" y="{P(0,3254.339)[1]+30}" text-anchor="middle">D1 Mini (other side)</text>')
ux0, ux1 = P(4148.79, 0)[0], P(4057.21, 0)[0]
uy = P(0, 3145)[1]
a(f'<rect x="{ux0}" y="{uy-5}" width="{ux1-ux0}" height="10" fill="none" stroke="#9fb7ec" stroke-width=".8"/>')
a(f'<text class="cl" x="{(ux0+ux1)/2}" y="{uy-21}" text-anchor="middle">9-pin header</text>')
pads = {}
u2 = ['5V', 'GND', 'RST', 'A0', 'D0', 'D4', 'RX', 'TX', '3V3']
for i, n in enumerate(u2):
    X, Y = P(4063 + 10 * i, 3145); pads['U2.' + n] = (X, Y)
    a(f'<circle class="pad" cx="{X}" cy="{Y}" r="2.9"/>')
    a(f'<text class="pl" x="{X}" y="{Y-6.5}" text-anchor="middle" font-size="3.1px">{n}</text>')
colA = ['TX', 'RX', 'D1', 'D2', 'D3', 'D4', 'GND', '5V']
colB = ['RST', 'A0', 'D0', 'D5', 'D6', 'D7', 'D8', '3V3']
for i, n in enumerate(colA):
    X, Y = P(4128.961, 3184.339 + 10 * i); pads[n] = (X, Y)
    a(f'<circle class="pad" cx="{X}" cy="{Y}" r="3.2"/><text class="pl" x="{X-5.5}" y="{Y+1.6}" text-anchor="end">{n}</text>')
for i, n in enumerate(colB):
    X, Y = P(4038.961, 3184.339 + 10 * i); pads[n] = (X, Y)
    a(f'<circle class="pad" cx="{X}" cy="{Y}" r="3.2"/><text class="pl" x="{X+5.5}" y="{Y+1.6}">{n}</text>')
# other parts, grey pads with labels
def grp(name, pts, lx, ly, anchor='middle'):
    for x, y in pts:
        X, Y = P(x, y); a(f'<circle cx="{X}" cy="{Y}" r="2.6" fill="#b9c3d6" stroke="#6b7a96" stroke-width=".5"/>')
    a(f'<text class="cl" x="{lx}" y="{ly}" text-anchor="{anchor}">{name}</text>')
grp('I2C-B', [(4157.795, 3180.717 + 10 * i) for i in range(4)], 19.7, 109)
grp('I2C-A', [(4153.858, 3236.819 + 10 * i) for i in range(4)], 23.6, 165)
grp('Diode', [(4154, 3291.449), (4154, 3322.551)], 33, 196, 'start')
grp('HALL', [(4153.502, 3344.158 + 9.842 * i) for i in range(3)], 24, 262)
grp('Motor (CN2)', [(4091.535 + 10 * i, 3391.583) for i in range(5)], 66, 292)
grp('ULN2003', [(4060.5 + 10 * i, 3333) for i in range(8)] + [(4060.5 + 10 * i, 3363) for i in range(8)], 82, 238)
grp('12V OUT', [(4036.732, 3317.843), (4036.732, 3307.843)], 141, 186)
grp('12V IN', [(4036.732, 3374.929), (4036.732, 3364.929)], 141, 243)
# --- modifications ---
d3, d0, v33 = pads['D3'], pads['D0'], pads['3V3']
# 10k: D0 -> 3V3, body on inner side
bx = d0[0] - 11
a(f'<path d="M {d0[0]} {d0[1]} L {bx} {d0[1]+8} L {bx} {v33[1]-8} L {v33[0]} {v33[1]}" fill="none" stroke="#c9ced6" stroke-width="1.1" stroke-linejoin="round"/>')
a(f'<rect x="{bx-4.2}" y="{d0[1]+13}" width="8.4" height="24" rx="3" fill="#8ce99a" stroke="#2b8a3e" stroke-width=".8"/>')
a(f'<text class="ml" fill="#b2f2bb" x="{bx-6.5}" y="{d0[1]+27}" text-anchor="end">10 kΩ</text>')
# jumper wire D3 -> D0
a(f'<path d="M {d3[0]} {d3[1]} C 82 118, 112 97, {d0[0]} {d0[1]}" fill="none" stroke="#ff922b" stroke-width="2.2" stroke-linecap="round"/>')
a(f'<text class="ml" fill="#ffc078" x="86" y="118" text-anchor="middle">wire</text>')
# master 4.7k: D1 and D2 -> U2 3V3
p9 = pads['U2.3V3']
for (pin, bxm, ytop) in [('D1', 60, 44), ('D2', 71, 40)]:
    p = pads[pin]
    a(f'<path d="M {p[0]} {p[1]} L {bxm} {p[1]} L {bxm} {ytop} L {p9[0]} {ytop} L {p9[0]} {p9[1]}" fill="none" stroke="#c9ced6" stroke-width="1.1" stroke-linejoin="round" stroke-dasharray="none"/>')
    a(f'<rect x="{bxm-4.2}" y="{ytop+9}" width="8.4" height="24" rx="3" fill="#faa2c1" stroke="#c2255c" stroke-width=".8"/>')
a(f'<text class="ml" fill="#fcc2d7" x="77.5" y="64" >4.7 kΩ ×2</text>')
a(f'<text class="ml" fill="#fcc2d7" x="77.5" y="71" font-size="4.6px">master only</text>')
# 10 nF: ULN2003 pin 8 (GND) -> pin 9 (COM, +12V), the pins next to the 12V sockets
p8, p9u = P(4060.5, 3333), P(4060.5, 3363)
a(f'<text class="pl" x="{p8[0]}" y="{p8[1]-5}" text-anchor="middle">8</text>')
a(f'<text class="pl" x="{p9u[0]}" y="{p9u[1]+8.5}" text-anchor="middle">9</text>')
a(f'<path d="M {p8[0]} {p8[1]} L {p9u[0]} {p9u[1]}" stroke="#c9ced6" stroke-width="1.1"/>')
cy = (p8[1] + p9u[1]) / 2
a(f'<rect x="{p8[0]-5.5}" y="{cy-5}" width="11" height="10" rx="4.5" fill="#74c0fc" stroke="#1c7ed6" stroke-width=".8"/>')
a(f'<text class="ml" fill="#a5d8ff" x="{p8[0]+8}" y="{cy-3}">10 nF</text>')
# view label
a(f'<text x="{W/2}" y="{H+8.5}" text-anchor="middle" font-size="6px" fill="#333" font-weight="700">BOTTOM VIEW · 9-pin header at the top</text>')
a('</svg>')
open(sys.argv[1], 'w').write('\n'.join(out))
