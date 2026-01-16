#!/bin/bash

################################################################################
# AutoTest Framework Generator v4.3.0
# 主脚本：调度各个子脚本完成框架生成
################################################################################

set -e

VERSION="4.3.0"

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

print_header() {
    echo -e "${CYAN}"
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║     AutoTest Framework Generator v${VERSION}                      ║"
    echo "║          智能 C++/Qt 单元测试框架生成器                           ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_step() {
    echo -e "${BLUE}[STEP $1]${NC} $2"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

show_usage() {
    cat << EOF
用法: $0 [选项] [项目根目录]

选项:
    -h, --help              显示帮助信息
    -v, --version           显示版本信息
    -p, --project-dir DIR   项目根目录（默认为当前目录）
    -s, --script-dir DIR    工具脚本目录（用于定位 stub 源文件）

示例:
    # 基本用法（在当前目录）
    $0

    # 指定项目目录
    $0 -p /path/to/project

    # 指定工具目录
    $0 -p /path/to/project -s /path/to/tools

EOF
}

main() {
    print_header

    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_usage
                exit 0
                ;;
            -v|--version)
                echo "AutoTest Framework Generator v${VERSION}"
                exit 0
                ;;
            -p|--project-dir)
                PROJECT_ROOT="$(cd "$2" && pwd)"
                shift 2
                ;;
            -s|--script-dir)
                SCRIPT_DIR="$(cd "$2" && pwd)"
                shift 2
                ;;
            *)
                print_error "未知选项: $1"
                show_usage
                exit 1
                ;;
        esac
    done

    PROJECT_ROOT="${PROJECT_ROOT:-$(pwd)}"
    AUTOTEST_ROOT="${PROJECT_ROOT}/autotests"
    SCRIPT_DIR="${SCRIPT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}"

    print_step 1 "创建测试目录结构..."
    mkdir -p "${AUTOTEST_ROOT}"
    mkdir -p "${AUTOTEST_ROOT}/3rdparty/testutils"
    print_success "目录结构创建完成"

    print_step 2 "检测项目结构..."
    export PROJECT_ROOT AUTOTEST_ROOT SCRIPT_DIR
    export RED GREEN BLUE CYAN NC
    "${SCRIPT_DIR}/scripts/detect-project.sh"

    source "${AUTOTEST_ROOT}/.project_config"
    print_success "项目结构检测完成"

    print_step 3 "复制 stub-ext Mock 工具..."
    "${SCRIPT_DIR}/scripts/copy-stubs.sh"

    print_step 4 "生成子模块 CMakeLists.txt..."
    "${SCRIPT_DIR}/scripts/generate-submodules.sh"

    print_step 5 "生成 CMake 测试工具..."
    "${SCRIPT_DIR}/scripts/generate-cmake-utils.sh"

    print_step 6 "生成测试主 CMakeLists.txt..."
    "${SCRIPT_DIR}/scripts/generate-main-cmake.sh"

    print_step 7 "生成测试运行脚本..."
    "${SCRIPT_DIR}/scripts/generate-runner.sh"

    print_step 8 "生成文档..."
    "${SCRIPT_DIR}/scripts/generate-readme.sh"

    rm -f "${AUTOTEST_ROOT}/.project_config"

    echo ""
    echo "========================================"
    print_success "测试框架生成完成！"
    echo "========================================"
    echo ""
    echo "生成的文件："
    echo "  📁 ${AUTOTEST_ROOT}/"
    echo "  ├─ 3rdparty/testutils/     # Stub Mock 工具"
    echo "  ├─ CMakeLists.txt         # 测试构建配置"
    echo "  ├─ run-ut.sh             # 测试运行脚本"
    echo "  ├─ libs/                 # 库测试"
    echo "  ├─ plugins/              # 插件测试"
    echo "  ├─ services/             # 服务测试"
    echo "  └─ README.md            # 使用文档"
    echo ""
    echo "  📁 ${PROJECT_ROOT}/cmake/"
    echo "  └─ UnitTestUtils.cmake     # CMake 测试工具"
    echo ""
    echo "下一步："
    echo "  1. cd ${AUTOTEST_ROOT}"
    echo "  2. 根据需要编写测试用例（参考 README.md）"
    echo "  3. ./run-ut.sh 运行测试"
    echo ""
    echo "文档："
    echo "  📖 ${AUTOTEST_ROOT}/README.md"
    echo ""
}

main "$@"
