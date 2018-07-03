if(CMAKE_VERSION VERSION_GREATER_EQUAL 3.8.0)
	include(CMakeFindDependencyMacro)
	find_dependency(OpenGL REQUIRED)
endif()

include("${CMAKE_CURRENT_LIST_DIR}/gl3w-targets.cmake")
