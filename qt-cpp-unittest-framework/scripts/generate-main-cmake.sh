#!/bin/bash

################################################################################
# 生成主 CMakeLists.txt 脚本
################################################################################

set -e

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

generate_main_cmake() {
    cat > "${AUTOTEST_ROOT}/CMakeLists.txt" << EOF
# CMakeLists.txt for AutoTests
cmake_minimum_required(VERSION 3.10)

project(autotests)

    set(CMAKE_CXX_STANDARD ${CPP_STANDARD})
    set(CMAKE_CXX_STANDARD_REQUIRED ON)

    set(AUTOTEST_ROOT \${CMAKE_CURRENT_SOURCE_DIR})

    list(APPEND CMAKE_MODULE_PATH "\${CMAKE_CURRENT_SOURCE_DIR}/../cmake")
    include(UnitTestUtils)

    option(USE_QT "Enable Qt support" ON)
    option(ENABLE_COVERAGE "Enable code coverage" ON)
    option(ENABLE_ASAN "Enable AddressSanitizer" ON)

    ut_init_test_environment()

    enable_testing()

    message(STATUS "=====================================")
    message(STATUS "AutoTests Configuration:")
    message(STATUS "  Use Qt:        \${USE_QT}")
    message(STATUS "Coverage:      \${ENABLE_COVERAGE}")
    message(STATUS "  ASAN:          \${ENABLE_ASAN}")
    message(STATUS "=====================================")
EOF

    if [ -n "$SUBDIRS" ]; then
        for dir in $SUBDIRS; do
            echo "add_subdirectory_if_exists(${dir})" >> "${AUTOTEST_ROOT}/CMakeLists.txt"
        done
    fi

    if [ ! -z "$STANDALONE_SRC" ] && [ "$STANDALONE_SRC" -gt 0 ]; then
        echo "add_subdirectory_if_exists(libs)" >> "${AUTOTEST_ROOT}/CMakeLists.txt"
    fi

    print_success "生成 autotests/CMakeLists.txt"
}

generate_main_cmake
