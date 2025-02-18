#pragma once
#include <ffi.h>
#include <string>

class Target {
public:
    void sayHello();
    // FFI测试函数
    static void testFFICallback(ffi_cif *cif, void *ret, void* args[],
                              void *userData);
    int callWithFFI(int x, int y);
private:
    static int add(int x, int y);
};