cmake_minimum_required(VERSION 3.2)
project(UZEM)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17 -fPIC")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -pedantic")

set(UZEM_SOURCES
	${CMAKE_SOURCE_DIR}/avr8.cpp
	${CMAKE_SOURCE_DIR}/uzem.cpp
	${CMAKE_SOURCE_DIR}/uzerom.cpp)

add_executable(uzem ${UZEM_SOURCES})

