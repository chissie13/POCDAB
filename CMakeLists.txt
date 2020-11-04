cmake_minimum_required(VERSION 3.1.2)
project("DataOverDAB" LANGUAGES CXX VERSION 0.69)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/products/bin" CACHE PATH "" FORCE)

list(APPEND CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake/modules")

include("${CMAKE_CURRENT_SOURCE_DIR}/cmake/config/Dependencies.cmake")

include_directories("include")
add_subdirectory("src")
