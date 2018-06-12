#!/usr/bin/python3

import sys
import pykms
import time

def wait_key():
    ''' Wait for a key press on the console and return it. '''
    result = None
    import termios
    fd = sys.stdin.fileno()

    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)

    try:
        result = sys.stdin.read(1)
    except IOError:
        pass
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    return result

card = pykms.Card()
res = pykms.ResourceManager(card)
conn = res.reserve_connector()
crtc = res.reserve_crtc(conn)
mode = conn.get_default_mode()

plane = res.reserve_generic_plane(crtc)
card.disable_planes()

crtc.set_mode(conn, mode)

fb = pykms.DumbFramebuffer(card, 256, 256, "AR24")
pykms.draw_rect(fb, 0, 0, 256, 256, pykms.RGB(255, 255, 0, 0))

print("set crtc {}, plane {}, fb {}".format(crtc.id, plane.id, fb.id))

size = 50
x = 100
y = 100

while True:
    plane.set_props({
        "FB_ID": fb.id,
        "CRTC_ID": crtc.id,
        "SRC_X": size << 16,
        "SRC_Y": size << 16,
        "SRC_W": (fb.width-size) << 16,
        "SRC_H": (fb.height-size) << 16,
        "CRTC_X": x,
        "CRTC_Y": y,
        "CRTC_W": fb.width-size,
        "CRTC_H": fb.height-size,
    })
    c = wait_key()
    if c == 'w':
        y = y - 1
    elif c == 's':
        y = y + 1
    elif c == 'a':
        x = x - 1
    elif c == 'd':
        x = x + 1
    elif c == '+':
        size = size + 1
    elif c == '-':
        size = size - 1
    elif c == 'q':
        break

