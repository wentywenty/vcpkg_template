#include "target.hpp"
#include <iostream>
#include <ffi.h>

void Target::sayHello() {
    std::cout << "Testing FFI functionality!" << std::endl;
}

int Target::add(int x, int y) {
    return x + y;
}

void Target::testFFICallback(ffi_cif *cif, void *ret, void* args[],
                           void *userData) {
    *(int*)ret = add(*(int*)args[0], *(int*)args[1]);
}

int Target::callWithFFI(int x, int y) {
    ffi_cif cif;
    ffi_type *args[2];
    void *values[2];
    int rc;

    // 准备参数类型
    args[0] = &ffi_type_sint;
    args[1] = &ffi_type_sint;

    // 准备FFI调用接口
    if (ffi_prep_cif(&cif, FFI_DEFAULT_ABI, 2,
                     &ffi_type_sint, args) != FFI_OK) {
        std::cerr << "Failed to prepare FFI CIF" << std::endl;
        return -1;
    }

    int arg1 = x;
    int arg2 = y;
    values[0] = &arg1;
    values[1] = &arg2;

    // 进行FFI调用
    ffi_call(&cif, FFI_FN(testFFICallback), &rc, values);
    return rc;
}

int main() {
    Target target;
    target.sayHello();
    
    // 测试FFI调用
    int result = target.callWithFFI(10, 20);
    std::cout << "FFI call result (10 + 20): " << result << std::endl;
    
    return 0;
}