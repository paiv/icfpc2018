import numpy as np

#  1     2     3     4       5       6     7       8       9     10    11      12
_, FLIP, WAIT, HALT, S_MOVE, L_MOVE, FILL, FUSE_P, FUSE_S, FISS, VOID, G_FILL, G_VOID = range(13)


def add_coords(a, b):
    ay,ax,az = a
    by,bx,bz = b
    return (ay+by, ax+bx, az+bz)


def decode_trace(trace):
    def nd(op):
        x = (op >> 3) // 9 - 1
        y = (op >> 3) % 9 // 3 - 1
        z = (op >> 3) % 3 - 1
        return (y, x, z)
    def fd(op):
        return op - 30

    res = list()
    i = 0
    while i < len(trace):
        op = trace[i]

        if op == 0b11111101:
            res.append((FLIP,))

        elif op == 0b11111110:
            res.append((WAIT,))

        elif op == 0b11111111:
            res.append((HALT,))

        else:
            q = op & 0b111

            if q == 0b100:
                if op & 0b1111 == 0b0100:
                    a = op >> 4
                    x = trace[i+1] - 15
                    res.append((S_MOVE, ((a==2)*x, (a==1)*x, (a==3)*x)))
                else:
                    a = op >> 6
                    b = (op >> 4) & 3
                    x = trace[i+1]
                    x, y = (x >> 4) - 5, (x & 15) - 5
                    res.append((L_MOVE, ((a==2)*x or (b==2)*y, (a==1)*x or (b==1)*y, (a==3)*x or (b==3)*y)))
                i += 1

            elif q == 0b011:
                res.append((FILL, nd(op)))

            elif q == 0b010:
                res.append((VOID, nd(op)))

            elif q == 0b111:
                res.append((FUSE_P, nd(op)))

            elif q == 0b110:
                res.append((FUSE_S, nd(op)))

            elif q == 0b101:
                m = trace[i+1]
                res.append((FISS, nd(op), m))
                i += 1

            elif q == 0b001:
                x,y,z = map(fd, trace[i+1:i+4])
                res.append((G_FILL, nd(op), (y,x,z)))
                i += 3

            elif q == 0b000:
                x,y,z = map(fd, trace[i+1:i+4])
                res.append((G_VOID, nd(op), (y,x,z)))
                i += 3

            else:
                raise Exception(f'unhandled op {op:08b}')

        i += 1

    return res


def encode_trace(trace):
    def nd(y, x, z):
        return ((x + 1) * 9 + (y + 1) * 3 + (z + 1)) << 3

    res = list()

    for i, op in enumerate(trace):
        op, *args = op

        if op == FLIP:
            res.append(0b11111101)

        elif op == WAIT:
            res.append(0b11111110)

        elif op == HALT:
            res.append(0b11111111)

        elif op == S_MOVE:
            y,x,z = args[0]
            a = (x and 1) or (y and 2) or (z and 3)
            res.append((a << 4) | 0b0100)
            res.append(((x or y or z) + 15) % 256)

        elif op == L_MOVE:
            y,x,z = args[0]
            if x == 0:
                a1, a2 = 2, 3
                i1, i2 = y, z
            elif y == 0:
                a1, a2 = 1, 3
                i1, i2 = x, z
            elif z == 0:
                a1, a2 = 1, 2
                i1, i2 = x, y
            res.append((a2 << 6) | (a1 << 4) | 0b1100)
            res.append(((i2 + 5) % 256 << 4) | (i1 + 5) % 256)

        elif op == FILL:
            res.append(nd(*args[0]) | 0b011)

        elif op == VOID:
            res.append(nd(*args[0]) | 0b010)

        elif op == FUSE_P:
            res.append(nd(*args[0]) | 0b111)

        elif op == FUSE_S:
            res.append(nd(*args[0]) | 0b110)

        elif op == FISS:
            res.append(nd(*args[0]) | 0b101)
            res.append(args[1])

        else:
            raise Exception(f'unhandled op {op} {args}')

    return bytes(res)


def score_trace(model, trace, verbose=False):
    def log(*args):
        if verbose: print(*args)

    R = len(model)
    log('model R:', R)
    harmonics = 0
    bots = [(0,0,0)]
    energy = 0
    matrix = np.zeros((R,R,R), dtype=np.uint8)

    def move_bot(i, dp):
        t = add_coords(bots[i], dp)
        if any(x < 0 or x >= R for x in t):
            raise Exception('invalid move for bot {} at {}: {}'.format(i, bots[i], dp))
        if matrix[t]:
            raise Exception('cannot move bot {} from {} to filled space at {}'.format(i, bots[i], dp))
        bots[i] = t

    for i, op in enumerate(trace):
        op, *args = op
        log(f'{i}: {op} {args} bots: {bots}')

        energy += R*R*R * 3 * (10 if harmonics else 1)
        energy += 20 * len(bots)

        if op == FLIP:
            harmonics = 1 - harmonics

        elif op == WAIT:
            pass

        elif op == HALT:
            if harmonics:
                raise Exception('halt at high harmonics')

        elif op == S_MOVE:
            move_bot(0, args[0])
            energy += 2 * sum(map(abs, args[0]))

        elif op == L_MOVE:
            move_bot(0, args[0])
            energy += 2 * sum(map(abs, args[0])) + 4

        elif op == FILL:
            p = add_coords(bots[0], args[0])
            t = matrix[p]
            matrix[p] = 1
            energy += 6 * (2 - t)

        elif op == FUSE_P:
            p = add_coords(bots[0], args[0])
            energy -= 24

        elif op == FUSE_S:
            p = add_coords(bots[0], args[0])
            energy -= 24

        elif op == FISS:
            p = add_coords(bots[0], args[0])
            m = args[1]
            energy += 24

        else:
            raise Exception(f'unhandled op {op} {args}')

        log('energy:', energy)
    return energy, matrix


def read_trace(fn):
    with open(fn, 'rb') as f:
        return decode_trace(f.read())


def write_trace(fn, trace):
    data = encode_trace(trace)
    with open(fn, 'wb') as f:
        f.write(data)


def write_empty_trace(fn):
    return write_trace(fn, [(HALT,)])
