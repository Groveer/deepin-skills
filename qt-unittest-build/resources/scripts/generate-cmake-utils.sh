#!/bin/bash

################################################################################
# 生成 CMake 测试工具脚本
################################################################################

set -e

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

generate_cmake_test_utils() {
    mkdir -p "${AUTOTEST_ROOT}/cmake"

    cat > "${AUTOTEST_ROOT}/cmake/UnitTestUtils.cmake" << 'CMAKEEOF'
# UnitTestUtils.cmake - Universal C++ Unit Test CMake Utilities
# Version: 4.2.0

cmake_minimum_required(VERSION 3.10)

set(CPP_STUB_SRC "" CACHE INTERNAL "Stub source files for testing")
set(UT_TEST_CXX_FLAGS "" CACHE INTERNAL "Test-specific CXX flags")

function(add_subdirectory_if_exists dir)
    if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/${dir}/CMakeLists.txt")
        add_subdirectory(${dir})
    elseif(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/${dir}")
        message(STATUS "UT: Subdirectory ${dir} exists but has no CMakeLists.txt")
    else()
        message(STATUS "UT: Subdirectory ${dir} does not exist, skipping")
    endif()
endfunction()

function(ut_init_test_environment)
    message(STATUS "UT: Initializing test environment...")
    find_package(GTest REQUIRED)
    include_directories(${GTEST_INCLUDE_DIRS})

    if(USE_QT)
        find_package(Qt6 COMPONENTS Test QUIET)
        if(NOT Qt6Test_FOUND)
            find_package(Qt5 COMPONENTS Test QUIET)
        endif()
        if(Qt6Test_FOUND OR Qt5Test_FOUND)
            if(Qt6Test_FOUND)
                message(STATUS "UT: Using Qt6 Test")
            else()
                message(STATUS "UT: Using Qt5 Test")
            endif()
        endif()
    endif()

    link_libraries(${GTEST_LIBRARIES} ${GTEST_MAIN_LIBRARIES} pthread stdc++fs)
    add_definitions(-DDEBUG_STUB_INVOKE)
    ut_setup_test_stubs()
    ut_setup_coverage()
    message(STATUS "UT: Test environment initialized")
endfunction()

function(ut_setup_test_stubs)
    if(NOT EXISTS "${AUTOTEST_ROOT}/3rdparty/stub")
        message(WARNING "UT: stub not found, stub functionality will be limited")
        return()
    endif()

    message(STATUS "UT: Setting up test stubs...")

    file(GLOB STUB_SRC_FILES
        "${AUTOTEST_ROOT}/3rdparty/stub/*.h"
        "${AUTOTEST_ROOT}/3rdparty/stub/*.hpp"
        "${AUTOTEST_ROOT}/3rdparty/stub/*.cpp"
    )

    if(STUB_SRC_FILES)
        set(CPP_STUB_SRC ${STUB_SRC_FILES} CACHE INTERNAL "Stub source files")
        message(STATUS "UT: Found stub files:")
        foreach(stub_file ${STUB_SRC_FILES})
            message(STATUS "    ${stub_file}")
        endforeach()

        include_directories(
            "${AUTOTEST_ROOT}/3rdparty/stub"
        )
        message(STATUS "UT: Stub tools configured")
    else()
        message(WARNING "UT: No stub source files found")
    endif()
endfunction()

function(ut_setup_coverage)
    message(STATUS "UT: Setting up code coverage...")
    set(TEST_FLAGS "-fno-inline;-fno-access-control;-O0")
    list(APPEND TEST_FLAGS "-fprofile-arcs;-ftest-coverage;-lgcov")

    if(ENABLE_ASAN AND CMAKE_BUILD_TYPE STREQUAL "Debug")
        list(APPEND TEST_FLAGS "-fsanitize=undefined,address,leak;-fno-omit-frame-pointer")
        message(STATUS "UT: ASAN enabled (undefined,address,leak)")
    endif()

    set(UT_TEST_CXX_FLAGS ${TEST_FLAGS} CACHE INTERNAL "Test-specific CXX flags")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fno-inline -fno-access-control -O0 -fprofile-arcs -ftest-coverage -lgcov" PARENT_SCOPE)

    if(ENABLE_ASAN AND CMAKE_BUILD_TYPE STREQUAL "Debug")
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=undefined,address,leak -fno-omit-frame-pointer" PARENT_SCOPE)
    endif()

    message(STATUS "UT: Coverage configured")
    message(STATUS "  - Test flags: ${TEST_FLAGS}")
endfunction()

function(ut_create_test_executable test_name)
    set(options "")
    set(oneValueArgs "")
    set(multiValueArgs SOURCES HEADERS DEPENDENCIES LINK_LIBRARIES)
    cmake_parse_arguments(TEST "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

    message(STATUS "UT: Creating test executable: ${test_name}")

    set(ALL_SOURCES ${TEST_SOURCES})
    if(TEST_HEADERS)
        list(APPEND ALL_SOURCES ${TEST_HEADERS})
    endif()
    if(CPP_STUB_SRC)
        list(APPEND ALL_SOURCES ${CPP_STUB_SRC})
    endif()

    add_executable(${test_name} ${ALL_SOURCES})

    if(UT_TEST_CXX_FLAGS)
        target_compile_options(${test_name} PRIVATE ${UT_TEST_CXX_FLAGS})
        message(STATUS "UT: Applied test flags to ${test_name}: ${UT_TEST_CXX_FLAGS}")
    endif()

    if(UT_TEST_NO_DEBUG)
        target_compile_definitions(${test_name} PRIVATE QT_NO_DEBUG)
    endif()


    if(TEST_LINK_LIBRARIES)
        target_link_libraries(${test_name} PRIVATE ${TEST_LINK_LIBRARIES})
    endif()

    if(ENABLE_ASAN AND CMAKE_BUILD_TYPE STREQUAL "Debug")
        target_link_libraries(${test_name} PRIVATE
            -fsanitize=undefined,address,leak
            -fprofile-arcs
            -ftest-coverage
            -lgcov
        )
    else()
        target_link_libraries(${test_name} PRIVATE
            -fprofile-arcs
            -ftest-coverage
            -lgcov
        )
    endif()

    add_test(NAME ${test_name} COMMAND ${test_name})

    message(STATUS "UT: Created test executable: ${test_name}")
endfunction()

message(STATUS "UT: Unit test utilities loaded")
CMAKEEOF

    print_success "生成 cmake/UnitTestUtils.cmake"
}

generate_cmake_test_utils
