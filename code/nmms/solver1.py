import numpy as np
from collections import deque
from . import trace as nmms


def solve(model):
    _,DY,DX,DZ,FLIP,FILL = range(6)
    m = np.copy(model)
    R = len(m)
    pos = np.zeros(3, dtype=np.int16)

    floor_plan = deque()
    for i in range(R):
        if np.any(m[i]):
            floor_plan.appendleft(i)

    path = list()
    plan = deque()

    def flip():
        plan.appendleft((FLIP,None))
    def sign(x):
        return -1 if x < 0 else 1 if x > 0 else 0
    def mov_xx(a, dt):
        i = 0 if a == DY else 1 if a == DX else 2
        while dt:
            t = sign(dt) * min(15, abs(dt))
            plan.appendleft((a, t))
            pos[i] += t
            path.append(tuple(pos))
            dt -= t
    def movy(dy):
        return mov_xx(DY, dy)
    def movx(dx):
        return mov_xx(DX, dx)
    def movz(dz):
        return mov_xx(DZ, dz)
    def fillz(dt, m):
        a = DZ
        t = sign(dt)
        if m[0]:
            plan.appendleft((FILL, (-1,0,0)))
        for i in range(abs(dt)):
            mov_xx(a, t)
            dt -= t
            if m[i+1]:
                plan.appendleft((FILL, (-1,0,0)))

    flip()

    while floor_plan:
        floor = floor_plan.pop()
        dy = floor + 1 - pos[0]
        if dy: movy(dy)

        while np.any(m[floor]):
            ix = np.nonzero(m[floor])[0]
            l,r = min(ix), max(ix)
            if abs(l - pos[1]) <= abs(r - pos[1]):
                iz = np.nonzero(m[floor,l,:])[0]
                a, b = min(iz), max(iz)
                if abs(a-pos[2]) <= abs(b-pos[2]):
                    movz(a - pos[2])
                    movx(l - pos[1])
                    fillz(b - a, m[floor,l,a:b+1])
                else:
                    movz(b - pos[2])
                    movx(l - pos[1])
                    fillz(a - b, m[floor,l,a:b+1][::-1])
                m[floor,l,:] = 0
            else:
                iz = np.nonzero(m[floor,r,:])[0]
                a, b = min(iz), max(iz)
                if abs(a-pos[2]) <= abs(b-pos[2]):
                    movz(a - pos[2])
                    movx(r - pos[1])
                    fillz(b - a, m[floor,r,a:b+1])
                else:
                    movz(b - pos[2])
                    movx(r - pos[1])
                    fillz(a - b, m[floor,r,a:b+1][::-1])
                m[floor,r,:] = 0

    flip()
    movy(1)
    movz(-pos[2])
    movx(-pos[1])
    movy(-pos[0])

    trace = list()
    while plan:
        op, p = plan.pop()
        if op == DZ:
            trace.append((nmms.S_MOVE, (0, 0, p)))
        elif op == DX:
            trace.append((nmms.S_MOVE, (0, p, 0)))
        elif op == DY:
            trace.append((nmms.S_MOVE, (p, 0, 0)))
        elif op == FLIP:
            trace.append((nmms.FLIP,))
        elif op == FILL:
            trace.append((nmms.FILL, p))
    trace.append((nmms.HALT,))

    return trace
