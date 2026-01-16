#!/bin/bash

################################################################################
# 复制 stub-ext 工具脚本
################################################################################

set -e

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

copy_stub_ext() {
    local STUBUTILS_DIR="${AUTOTEST_ROOT}/3rdparty/testutils"
    local SKILL_RESOURCE_DIR="${SCRIPT_DIR}/resources/testutils"

    if [ -d "$STUBUTILS_DIR" ] && [ $(find "$STUBUTILS_DIR" \( -name "*.h" -o -name "*.cpp" \) | wc -l) -ge 6 ]; then
        print_success "stub-ext 工具已存在且完整"
        return 0
    fi

    if [ -d "$SKILL_RESOURCE_DIR" ]; then
        cp -r "$SKILL_RESOURCE_DIR" "${AUTOTEST_ROOT}/3rdparty/"
        local copied_files=$(find "$STUBUTILS_DIR" \( -name "*.h" -o -name "*.cpp" \) | wc -l)
        print_success "stub-ext 工具复制完成 (${copied_files} 个文件）"
        return 0
    else
        echo "ERROR: 无法找到技能资源目录: $SKILL_RESOURCE_DIR"
        echo "技能资源应位于: ~/.claude/skills/qt-cpp-unittest-framework/resources/testutils/"
        return 1
    fi
}

copy_stub_ext
