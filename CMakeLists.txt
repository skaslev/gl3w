cmake_minimum_required(VERSION 2.8)

project(gl3w)

execute_process(COMMAND python ${PROJECT_SOURCE_DIR}/gl3w_gen.py)

include_directories(include)

add_library(gl3w src/gl3w.c)

if (UNIX)
  target_link_libraries(gl3w dl)
endif()
