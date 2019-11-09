cmake_minimum_required(VERSION 2.8)

## Use the variable PROJECT_NAME for changing the target name
set( PROJECT_NAME "ToolpathGenerator" )

## Set our project name
project(${PROJECT_NAME})

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14 -O0")
# Find CGAL
# Add -O0 to remove optimizations when using gcc
IF(CMAKE_COMPILER_IS_GNUCC)
    set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -O0")
    set(CMAKE_C_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG} -O0")
ENDIF(CMAKE_COMPILER_IS_GNUCC)

find_package(CGAL REQUIRED COMPONENTS CORE) # If the dependency is required, use REQUIRED option - if it's not found CMake will issue an error
include( ${CGAL_USE_FILE} )

## Use all the *.cpp files we found under this folder for the project
FILE(GLOB SRCS "*.cpp" "*.c")
FILE(GLOB HEADER_FILES "*.hpp" "*.h")
#set(HEADER_FILES ${YOUR_DIRECTORY}/FileParser.h ${YOUR_DIRECTORY}/PolyWithHolesCreator.h ${YOUR_DIRECTORY}/WritePolysIntoFile.h)

message(STATUS SRCS)
## Define the executable
add_executable(${PROJECT_NAME} ${SRCS} ${HEADER_FILES})
target_link_libraries(${PROJECT_NAME} ${CGAL_LIBS} CGAL::CGAL CGAL::CGAL_Core)