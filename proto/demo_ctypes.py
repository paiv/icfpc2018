#!/usr/bin/env python
import ctypes


class Foo(ctypes.Structure):
    _fields_ = [
        ('p', ctypes.c_int),
        ('q', ctypes.c_ushort),
        ('x', ctypes.c_float),
    ]
    

def demo():
    some = ctypes.cdll.LoadLibrary('somelib/build/libsome.dylib')
    
    x = some.ifu()
    print('ifu: ', x)

    x = some.ifub(b'Hello, world!')
    print('ifub: ', x)
    
    some.bfu.restype = ctypes.c_char_p
    x = some.bfu()
    print('bfu: ', repr(x))
    
    some.wfu.restype = ctypes.c_wchar_p
    x = some.wfu()
    print('wfu: ', repr(x))

    foo = Foo(p=3, q=2, x=11.8)
    x = some.ifufoo(ctypes.byref(foo))
    print('ifufoo: ', x)

    atype = ctypes.c_int * 5
    a = atype(3, 2, 11, 4, 8)
    x = some.ifuiai(len(a), a)
    print('ifuiai: ', x, a[:])


if __name__ == '__main__':
    demo()
