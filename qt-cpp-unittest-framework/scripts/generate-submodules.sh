#!/bin/bash

################################################################################
# 生成子模块 CMakeLists.txt 脚本
################################################################################

set -e

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

generate_submodule_cmake() {
    if [ ! -z "$SUBDIRS_WITH_SOURCE" ]; then
        for dir in $SUBDIRS_WITH_SOURCE; do
            local cmake_file="${AUTOTEST_ROOT}/${dir}/CMakeLists.txt"

            cat > "${cmake_file}" << EOF
# CMakeLists.txt for ${dir} test
cmake_minimum_required(VERSION 3.10)

file(GLOB_RECURSE TEST_SOURCES "*.cpp" "*.h")
file(GLOB_RECURSE SOURCE_FILES
    "../${dir}/*.cpp"
    "../${dir}/*.h"
)
list(FILTER SOURCE_FILES EXCLUDE REGEX ".*/main\.cpp\$")

ut_create_test_executable(test-${dir}
    SOURCES \${TEST_SOURCES} \${SOURCE_FILES}
)

target_include_directories(test-${dir} PRIVATE "../${dir}")

message(STATUS "Submodule: Created test for ${dir}")
EOF

            print_success "生成 ${dir}/CMakeLists.txt"
        done
    fi

    if [ ! -z "$STANDALONE_SRC" ] && [ "$STANDALONE_SRC" -gt 0 ]; then
        local libs_cmake="${AUTOTEST_ROOT}/libs/CMakeLists.txt"

        cat > "${libs_cmake}" << 'EOF'
# CMakeLists.txt for standalone sources test
cmake_minimum_required(VERSION 3.10)

file(GLOB_RECURSE STANDALONE_SOURCES
    "../src/src/*.cpp"
    "../src/src/*.h"
)
list(FILTER STANDALONE_SOURCES EXCLUDE REGEX ".*/main\.cpp\$")

ut_create_test_executable(test-libs
    SOURCES ${STANDALONE_SOURCES}
)

message(STATUS "Submodule: Created test for libs")
EOF

        print_success "生成 libs/CMakeLists.txt"
    fi
}

generate_submodule_cmake
