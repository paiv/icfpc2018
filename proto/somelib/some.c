#include <string.h>
#include <wchar.h>


int ifu() {
    return 42;
}


int ifub(char* text) {
    return strlen(text);
}


char* bfu() {
    return "abcdefghi";
}


wchar_t* wfu() {
    return L"Hello, world!";
}


typedef struct {
    int p;
    unsigned short q;
    float x;
} Foo;


int ifufoo(Foo* foo) {
    return foo->p + foo->q + foo->x;
}


int ifuiai(int size, int xs[]) {
    int res = 0;
    for (size_t i = 0; i < size; i++) {
        res += xs[i];
        xs[i] = size - i;
    }
    return res;
}
