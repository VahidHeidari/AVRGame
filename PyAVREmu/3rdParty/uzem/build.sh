#!/bin/bash

#BUILD_TYPE="Debug"
BUILD_TYPE="Release"
#BUILD_TYPE="RelWithDebInfo"

BUILD_DIR="$BUILD_TYPE"
OUTPUT_DIR=".."

echo "Building..."
mkdir -p "$BUILD_DIR"
cd "$BUILD_DIR"

clear &&									\
cmake -DCMAKE_BUILD_TYPE=$BUILD_TYPE .. &&	\
make

echo "Building is completed."

