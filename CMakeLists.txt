cmake_minimum_required(VERSION 3.1.3 FATAL_ERROR)

project(gl3w)

set(CMAKE_VERBOSE_MAKEFILE false)
set(CMAKE_POSITION_INDEPENDENT_CODE ON) # -fPIC

set(SOURCE_DIR ${CMAKE_CURRENT_BINARY_DIR}/src)
set(HEADER_DIR ${CMAKE_CURRENT_BINARY_DIR}/include)

set(HEADER_FILES
	"${HEADER_DIR}/GL/gl3w.h"
	"${HEADER_DIR}/GL/glcorearb.h"
	"${HEADER_DIR}/KHR/khrplatform.h"
)

set(SOURCE_FILES
	"${SOURCE_DIR}/gl3w.c"
)

# add and depend on OpenGL
find_package(OpenGL REQUIRED)

# find python interpreter
find_package(PythonInterp REQUIRED)

if(CMAKE_VERSION VERSION_LESS 3.8.0)
	set(EXTERNAL_INCLUDE_DIRS ${EXTERNAL_INCLUDE_DIRS} ${OPENGL_INCLUDE_DIR})
	set(EXTERNAL_LIBRARIES ${EXTERNAL_LIBRARIES} ${OPENGL_LIBRARIES})
else()
	# Since CMake 3.8 the IMPORTED targets available
	set(EXTERNAL_LIBRARIES ${EXTERNAL_LIBRARIES} OpenGL::GL OpenGL::GLU)
endif()
# add command to create the header and source files
add_custom_command(
	OUTPUT
		"${SOURCE_DIR}/gl3w.c"
		"${HEADER_DIR}/GL/gl3w.h"
		"${HEADER_DIR}/GL/glcorearb.h"
		"${HEADER_DIR}/KHR/khrplatform.h"
	COMMAND "${PYTHON_EXECUTABLE}" ${CMAKE_CURRENT_SOURCE_DIR}/gl3w_gen.py
	DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/gl3w_gen.py
	WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
)

# add pseudo target that depends on the generated files
add_custom_target(
	gl3w_gen ALL
	DEPENDS
		"${SOURCE_DIR}/gl3w.c"
		"${HEADER_DIR}/GL/gl3w.h"
		"${HEADER_DIR}/GL/glcorearb.h"
		"${HEADER_DIR}/KHR/khrplatform.h"
)

# create gl3w target
add_library(${PROJECT_NAME} INTERFACE)

# make gl3w target depend on the generator target
add_dependencies(${PROJECT_NAME} gl3w_gen)

include(GNUInstallDirs)

# let remote project know about source and header files
foreach(SOURCE_FILE ${SOURCE_FILES})
	get_filename_component(SOURCE_FILENAME ${SOURCE_FILE} NAME)
	target_sources(${PROJECT_NAME} INTERFACE
		$<BUILD_INTERFACE:${SOURCE_FILE}>
		$<INSTALL_INTERFACE:${CMAKE_INSTALL_DATAROOTDIR}/${PROJECT_NAME}/${SOURCE_FILENAME}>)
	install(FILES "${SOURCE_FILE}"
		DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/${PROJECT_NAME})
endforeach()
foreach(HEADER_FILE ${HEADER_FILES})
	get_filename_component(HEADER_FILENAME ${HEADER_FILE} NAME)
	file(RELATIVE_PATH HEADER_PATH "${HEADER_DIR}" "${HEADER_FILE}")
	get_filename_component(HEADER_PATH ${HEADER_PATH} PATH)
	install(FILES "${HEADER_FILE}"
		DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}/${PROJECT_NAME}/${HEADER_PATH}")
endforeach()

target_include_directories(${PROJECT_NAME} INTERFACE
	$<BUILD_INTERFACE:${HEADER_DIR}>
	$<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}/${PROJECT_NAME}>
)
if(DEFINED EXTERNAL_INCLUDE_DIRS)
	target_include_directories(${PROJECT_NAME} INTERFACE ${EXTERNAL_INCLUDE_DIRS})
endif()
# let remote project know which libraries need to be linked
target_link_libraries(${PROJECT_NAME} INTERFACE ${EXTERNAL_LIBRARIES} ${CMAKE_DL_LIBS})

set(MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
set(BUILD_CMAKE_DIR "${CMAKE_CURRENT_BINARY_DIR}/cmake")

# export targets for remote projects (i.e. make find_package(gl3w) work)
configure_file(
	"${MODULE_PATH}/${PROJECT_NAME}-config.cmake"
	"${BUILD_CMAKE_DIR}/${PROJECT_NAME}-config.cmake"
	COPYONLY
)

install(TARGETS ${PROJECT_NAME} EXPORT ${PROJECT_NAME}-targets)

install(FILES "${MODULE_PATH}/${PROJECT_NAME}-config.cmake"
	DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/${PROJECT_NAME})
install(EXPORT ${PROJECT_NAME}-targets
	DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/${PROJECT_NAME})

export(
	TARGETS ${PROJECT_NAME}
	FILE "${BUILD_CMAKE_DIR}/${PROJECT_NAME}-targets.cmake"
)

export(PACKAGE ${PROJECT_NAME})
