cmake_minimum_required(VERSION 3.10)

# 设置输出编码为 UTF-8
if(MSVC)
    add_compile_options(/utf-8)
    add_compile_options("$<$<C_COMPILER_ID:MSVC>:/utf-8>")
    add_compile_options("$<$<CXX_COMPILER_ID:MSVC>:/utf-8>")
endif()

# 定义项目名称
project(vcpkg_template)

# 设置C++标准
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# ##################################################################
# 找依赖包
# ##################################################################

find_package(libffi CONFIG REQUIRED)
find_path(LIBFFI_INCLUDE_DIR ffi.h PATH_SUFFIXES libffi)

# ##################################################################
# 添加子项目
# ##################################################################

# 添加头文件目录
include_directories(
    ${CMAKE_SOURCE_DIR}/include
    ${LIBFFI_INCLUDE_DIR}
)

# 添加源文件
set(SOURCES
    src/target.cpp
)

# ##################################################################
# 生成项目
# ##################################################################

# 生成可执行文件
add_executable(${PROJECT_NAME} ${SOURCES})

# 添加链接库
target_link_libraries(${PROJECT_NAME} PRIVATE libffi)
target_include_directories(${PROJECT_NAME} PRIVATE ${LIBFFI_INCLUDE_DIR})

# ##################################################################
# 后续工作
# ##################################################################

# # 忽略警告
# if(MSVC)
#     target_compile_options(target PRIVATE /wd4828)
# endif()

# 设置生成器表达式以确保包含 Debug 和 Release 配置
set(CMAKE_CONFIGURATION_TYPES "Debug;Release" CACHE STRING "" FORCE)

# 设置平台
# set(CMAKE_GENERATOR_PLATFORM "Win32" CACHE STRING "" FORCE)
