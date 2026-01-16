#!/bin/bash

################################################################################
# 项目结构检测脚本
# 用途：检测项目的源码目录、C++标准、Qt/DTK支持等
################################################################################

set -e

print_info() {
    echo -e "${CYAN}[i]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

detect_project_structure() {
    # 检查 CMakeLists.txt
    if [ ! -f "${PROJECT_ROOT}/CMakeLists.txt" ]; then
        echo "ERROR: 未找到 CMakeLists.txt，这不是一个有效的 CMake 项目"
        exit 1
    fi

    # 检测源码目录
    SRC_DIRS=("src" "source" "lib" "libs")
    SOURCE_DIR=""
    for dir in "${SRC_DIRS[@]}"; do
        if [ -d "${PROJECT_ROOT}/${dir}" ]; then
            SOURCE_DIR="${PROJECT_ROOT}/${dir}"
            break
        fi
    done

    if [ -z "$SOURCE_DIR" ]; then
        SOURCE_DIR="${PROJECT_ROOT}"
    fi

    # 分析源码目录结构
    SUBDIRS=""
    STANDALONE_SRC=""
    SUBDIRS_WITH_SOURCE=""

    if [ -d "$SOURCE_DIR" ]; then
        ALL_SUBDIRS=$(find "$SOURCE_DIR" -maxdepth 1 -type d ! -path "$SOURCE_DIR" ! -name "test*" ! -name "3rdparty" -exec basename {} \; | sort)

        for dir in $ALL_SUBDIRS; do
            local dir_path="${SOURCE_DIR}/${dir}"
            local source_count=$(find "$dir_path" -maxdepth 1 -type f \( -name "*.cpp" -o -name "*.h" \) ! -name "main.cpp" ! -name "test_*" 2>/dev/null | wc -l)

            if [ "$source_count" -gt 0 ]; then
                if [ -z "$SUBDIRS" ]; then
                    SUBDIRS="$dir"
                else
                    SUBDIRS="$SUBDIRS $dir"
                fi
                if [ -z "$SUBDIRS_WITH_SOURCE" ]; then
                    SUBDIRS_WITH_SOURCE="$dir"
                else
                    SUBDIRS_WITH_SOURCE="$SUBDIRS_WITH_SOURCE $dir"
                fi
            fi
        done

        STANDALONE_SRC=$(find "$SOURCE_DIR" -maxdepth 1 -type f \( -name "*.cpp" -o -name "*.h" \) ! -name "main.cpp" ! -name "test_*" | wc -l)
    fi

    # 检测 Qt/DTK/C++标准
    USE_QT=false
    if grep -q "Qt[56]" "${PROJECT_ROOT}/CMakeLists.txt" 2>/dev/null || \
       grep -q "find_package(Qt" "${PROJECT_ROOT}/CMakeLists.txt" 2>/dev/null || \
       grep -q "Qt[56]" "$SOURCE_DIR"/* 2>/dev/null; then
         USE_QT=true
      fi

    CPP_STANDARD="14"
    if grep -q "CMAKE_CXX_STANDARD.*17" "${PROJECT_ROOT}/CMakeLists.txt" 2>/dev/null; then
        CPP_STANDARD="17"
    elif grep -q "CMAKE_CXX_STANDARD.*20" "${PROJECT_ROOT}/CMakeLists.txt" 2>/dev/null; then
        CPP_STANDARD="20"
    fi

    USE_DTK=false
    if grep -qi "DTK\|dtk" "${PROJECT_ROOT}/CMakeLists.txt" 2>/dev/null; then
        USE_DTK=true
    fi

    # 输出变量到临时文件
    cat > "${AUTOTEST_ROOT}/.project_config" << VARSEOF
SOURCE_DIR=$SOURCE_DIR
SUBDIRS="$SUBDIRS"
SUBDIRS_WITH_SOURCE="$SUBDIRS_WITH_SOURCE"
STANDALONE_SRC=$STANDALONE_SRC
USE_QT=$USE_QT
CPP_STANDARD=$CPP_STANDARD
USE_DTK=$USE_DTK
VARSEOF
}

# 执行检测
detect_project_structure
