import numpy as np


def decode_model(model):
    R = model[0]
    if isinstance(model, list):
        a = np.array(model[1:], dtype=np.uint8)
    else:
        a = np.frombuffer(model[1:], dtype=np.uint8)
    b = np.unpackbits(a)
    c = b.reshape(-1,8)[:,::-1].reshape(-1)
    return c[:R*R*R].reshape(R,R,R).transpose((1,0,2))


def encode_model(matrix):
    R = len(matrix)
    a = matrix.transpose((1,0,2)).reshape(-1)
    r = (-R*R*R) % 8
    b = np.append(a, np.zeros(r, dtype=np.uint8))
    c = b.reshape(-1,8)[:,::-1]
    return bytes([R]) + bytes(np.packbits(c))


def read_model(fn):
    with open(fn, 'rb') as f:
        return decode_model(f.read())


def write_model(fn, model):
    data = encode_model(model)
    with open(fn, 'wb') as f:
        f.write(data)
