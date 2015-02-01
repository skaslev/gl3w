cmake_minimum_required(VERSION 2.8)

option(BUILD_TESTS "build test examples" OFF)

project(gl3w)

include_directories(include)

add_library(gl3w src/gl3w.c)

if (UNIX)
  target_link_libraries(gl3w dl)
endif()

if (BUILD_TESTS)
  find_package(OpenGL REQUIRED)
  find_package(GLUT REQUIRED)
  
  include_directories(${GLUT_INCLUDE_DIR})
  
  add_executable(gl3wtest
    src/test.c
    )
  target_link_libraries(gl3wtest
    gl3w
    ${GLUT_glut_LIBRARY}
    ${OPENGL_gl_LIBRARY}
    )
endif (BUILD_TESTS)
