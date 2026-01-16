#!/bin/bash

################################################################################
# 生成测试运行脚本
################################################################################

set -e

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

generate_test_runner_script() {
    cat > "${AUTOTEST_ROOT}/run-ut.sh" << 'EOF'
#!/bin/bash

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

print_step() {
    echo -e "${BLUE}[STEP $1]${NC} $2"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

show_usage() {
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  --from-step <N>    从步骤 N 开始执行 (1-5)"
    echo "  -h, --help         显示帮助信息"
    echo ""
    echo "步骤:"
    echo "  1. 准备构建环境"
    echo "  2. 配置 CMake"
    echo "  3. 编译测试"
    echo "  4. 运行测试"
    echo "  5. 生成覆盖率报告"
}

START_STEP=1
while [[ $# -gt 0 ]]; do
    case $1 in
        --from-step)
            START_STEP="$2"
            shift 2
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
    esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BUILD_DIR="${PROJECT_ROOT}/build-autotests"
REPORT_DIR="${BUILD_DIR}/test-reports"

echo "========================================"
echo "  AutoTest Runner"
echo "========================================"
echo "项目根目录: $PROJECT_ROOT"
echo "构建目录: $BUILD_DIR"

TEST_PASSED=false

if [ $START_STEP -le 1 ]; then
    print_step 1 "准备构建环境..."
    if [ -d "$BUILD_DIR" ]; then
        rm -rf "$BUILD_DIR"
    fi
    mkdir -p "$BUILD_DIR" "$REPORT_DIR"
    print_success "构建环境准备完成"
fi

if [ $START_STEP -le 2 ]; then
    print_step 2 "配置 CMake..."
    cd "$BUILD_DIR"
    cmake "$SCRIPT_DIR" -DCMAKE_BUILD_TYPE=Debug -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
    print_success "CMake 配置完成"
fi

if [ $START_STEP -le 3 ]; then
    print_step 3 "编译测试..."
    cd "$BUILD_DIR"
    cmake --build . -j $(nproc)
    print_success "编译完成"
fi

if [ $START_STEP -le 4 ]; then
    print_step 4 "运行测试..."
    cd "$BUILD_DIR"
    if ctest --output-on-failure > "$REPORT_DIR/test_output.log" 2>&1; then
        print_success "所有测试通过"
        TEST_PASSED=true
    else
        print_error "部分测试失败"
    fi
fi

if [ $START_STEP -le 5 ]; then
    print_step 5 "生成覆盖率报告..."
    set +e
    if command -v lcov &> /dev/null; then
        cd "$BUILD_DIR"
        mkdir -p coverage
        lcov --directory . --capture --output-file coverage/total.info > "$REPORT_DIR/coverage_output.log" 2>&1 || true
        if [ -f "coverage/total.info" ]; then
            lcov --extract "coverage/total.info" "*/src/*" --output-file coverage/filtered.info >> "$REPORT_DIR/coverage_output.log" 2>&1 || true
            lcov --remove "coverage/filtered.info" "*/test*" "*/autotests/*" --output-file coverage/filtered.info >> "$REPORT_DIR/coverage_output.log" 2>&1 || true
        fi
        if [ -f "coverage/filtered.info" ] && [ -s "coverage/filtered.info" ]; then
            genhtml --output-directory coverage/html --title "Coverage Report" coverage/filtered.info >> "$REPORT_DIR/coverage_output.log" 2>&1
            if [ $? -eq 0 ]; then
                print_success "覆盖率报告生成完成"
                print_success "覆盖率报告: $BUILD_DIR/coverage/html/index.html"
            fi
        fi
    else
        print_error "lcov 未安装"
    fi
    set -e
fi

echo ""
if [ "$TEST_PASSED" = true ]; then
    print_success "测试执行完成！"
else
    print_error "测试有失败"
fi

if [ "$TEST_PASSED" != true ]; then
    exit 1
fi
EOF

    chmod +x "${AUTOTEST_ROOT}/run-ut.sh"
    print_success "生成 autotests/run-ut.sh"
}

generate_test_runner_script
