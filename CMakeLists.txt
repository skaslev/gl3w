cmake_minimum_required(VERSION 2.8)

project(gl3w)

include_directories(include)

add_library(gl3w src/gl3w.c)

if (UNIX)
  target_link_libraries(gl3w dl)
endif()
