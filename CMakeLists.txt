# cmake lists file for gl3w
cmake_minimum_required(VERSION 2.8)

project(libgl3w)

set(LIBRARY_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/lib)
# set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin)


include_directories(include/)

if (WIN32)
	add_library(gl3w src/gl3w include/GL3/gl3w.h include/GL3/gl3.h)
#	add_executable(test_static src/test)
#	target_link_libraries(test_static STATIC gl3w glut)
else (WIN32)
	add_library(gl3w src/gl3w)
endif (WIN32)

# todo: add test executable
