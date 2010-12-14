# cmake lists file for gl3w
cmake_minimum_required(VERSION 2.8)

project(libgl3w)

include_directories(include/)

if (WIN32)
	add_library(ggl3w src/gl3w include/GL3/gl3w.h include/GL3/gl3.h)
else (WIN32)
	add_library(gl3w src/gl3w)
endif (WIN32)
