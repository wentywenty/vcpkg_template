#include "target.hpp"

#include <iostream>


void Target::sayHello() { std::cout << "Hello, World!" << std::endl; }

int main() {
    Target target;
    target.sayHello();
    return 0;
}
