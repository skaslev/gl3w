cmake_minimum_required(VERSION 2.8)
project(gl3w C)
enable_testing()

find_package(PythonInterp 2.6 REQUIRED)
execute_process(COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/gl3w_gen.py
                WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR})

include_directories(${CMAKE_CURRENT_BINARY_DIR}/include)

add_library(gl3w ${CMAKE_CURRENT_BINARY_DIR}/src/gl3w.c)
if (UNIX AND NOT APPLE)
  target_link_libraries(gl3w dl)
endif()

add_executable(gl3w_test ${CMAKE_CURRENT_SOURCE_DIR}/src/test.c)
target_link_libraries(gl3w_test gl3w glut GL)
add_test(NAME gl3w_test COMMAND gl3w_test)

set(OPENGL_INCLUDE_DIR ${CMAKE_CURRENT_BINARY_DIR}/include)
