import numpy as np
from collections import deque
from . import trace as nmms


def erase(model):
    _,DY,DX,DZ = range(4)
    m = np.copy(model)
    R = len(m)
    pos = {0:np.zeros(3, dtype=np.int16)}
    seeds = {0:list(range(1,40))}
    botat = np.zeros((R,R,R), dtype=np.int8) - 1
    botat[(0,0,0)] = 0
    trace = list()

    def flip():
        trace.append((nmms.FLIP,))
    def sign(x):
        return -1 if x < 0 else 1 if x > 0 else 0
    def mov_xx(bot, a, dt):
        i = 0 if a == DY else 1 if a == DX else 2
        while dt:
            t = sign(dt) * min(15, abs(dt))
            trace.append((nmms.S_MOVE, ((a==DY)*t, (a==DX)*t, (a==DZ)*t)))
            botat[tuple(pos[bot])] = -1
            pos[bot][i] += t
            botat[tuple(pos[bot])] = bot
            dt -= t
    def movy(bot, dy):
        return mov_xx(bot, DY, dy)
    def movx(bot, dx):
        return mov_xx(bot, DX, dx)
    def movz(bot, dz):
        return mov_xx(bot, DZ, dz)
    def halt():
        trace.append((nmms.HALT,))
    def fiss(bot, p, m=None):
        old_seeds = seeds[bot]
        if m is None: m = (len(seeds) - 1) // 2
        trace.append((nmms.FISS, p, m))
        bid = old_seeds[0]
        pos[bid] = pos[bot] + p
        botat[tuple(pos[bid])] = bid
        seeds[bid] = old_seeds[1:m+1]
        seeds[bot] = old_seeds[m+1:]
    def fuse(bot, p):
        trace.append((nmms.FUSE_P, p))
        trace.append((nmms.FUSE_S, tuple(-np.array(p, dtype=np.int8))))
        bid = botat[tuple(pos[bot]+p)]
        botat[tuple(pos[bot]+p)] = -1
        seeds[bot] = sorted(seeds[bid] + seeds[bot])
        seeds.pop(bid)
        pos.pop(bid)

    flip()
    while np.any(m):
        pass
    movy(0, -pos[0][0])
    movz(0, -pos[0][1])
    movx(0, -pos[0][2])
    flip()
    halt()

    return trace
