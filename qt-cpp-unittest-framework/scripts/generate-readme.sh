#!/bin/bash

################################################################################
# 生成 README.md 脚本
################################################################################

set -e

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

generate_readme() {
    rm -f "${AUTOTEST_ROOT}/README.md"

    echo "# AutoTest Framework" >> "${AUTOTEST_ROOT}/README.md"
    echo "" >> "${AUTOTEST_ROOT}/README.md"
    echo "## Quick Start" >> "${AUTOTEST_ROOT}/README.md"
    echo "" >> "${AUTOTEST_ROOT}/README.md"
    echo "### 1. Write Tests" >> "${AUTOTEST_ROOT}/README.md"
    echo "" >> "${AUTOTEST_ROOT}/README.md"
    echo '```cpp' >> "${AUTOTEST_ROOT}/README.md"
    echo "#include <gtest/gtest.h>" >> "${AUTOTEST_ROOT}/README.md"
    echo "#include \"stubext.h\"" >> "${AUTOTEST_ROOT}/README.md"
    echo "#include \"myclass.h\"" >> "${AUTOTEST_ROOT}/README.md"
    echo "" >> "${AUTOTEST_ROOT}/README.md"
    echo "class UT_MyClass : public testing::Test {" >> "${AUTOTEST_ROOT}/README.md"
    echo "public:" >> "${AUTOTEST_ROOT}/README.md"
    echo "    void SetUp() override {" >> "${AUTOTEST_ROOT}/README.md"
    echo "        obj = new MyClass();" >> "${AUTOTEST_ROOT}/README.md"
    echo "    }" >> "${AUTOTEST_ROOT}/README.md"
    echo "" >> "${AUTOTEST_ROOT}/README.md"
    echo "    void TearDown() override {" >> "${AUTOTEST_ROOT}/README.md"
    echo "        stub.clear();" >> "${AUTOTEST_ROOT}/README.md"
    echo "        delete obj;" >> "${AUTOTEST_ROOT}/README.md"
    echo "    }" >> "${AUTOTEST_ROOT}/README.md"
    echo "" >> "${AUTOTEST_ROOT}/README.md"
    echo "    stub_ext::StubExt stub;" >> "${AUTOTEST_ROOT}/README.md"
    echo "    MyClass *obj = nullptr;" >> "${AUTOTEST_ROOT}/README.md"
    echo "};" >> "${AUTOTEST_ROOT}/README.md"
    echo "" >> "${AUTOTEST_ROOT}/README.md"
    echo "TEST_F(UT_MyClass, Calculate_ValidInput_ReturnsCorrectResult) {" >> "${AUTOTEST_ROOT}/README.md"
    echo "    int a = 10, b = 20;" >> "${AUTOTEST_ROOT}/README.md"
    echo "    int expected = 30;" >> "${AUTOTEST_ROOT}/README.md"
    echo "    int result = obj->calculate(a, b);" >> "${AUTOTEST_ROOT}/README.md"
    echo "    EXPECT_EQ(result, expected);" >> "${AUTOTEST_ROOT}/README.md"
    echo "}" >> "${AUTOTEST_ROOT}/README.md"
    echo '```' >> "${AUTOTEST_ROOT}/README.md"
    echo "" >> "${AUTOTEST_ROOT}/README.md"
    echo "### 2. Run Tests" >> "${AUTOTEST_ROOT}/README.md"
    echo "" >> "${AUTOTEST_ROOT}/README.md"
    echo '```bash' >> "${AUTOTEST_ROOT}/README.md"
    echo "cd autotests" >> "${AUTOTEST_ROOT}/README.md"
    echo "./run-ut.sh" >> "${AUTOTEST_ROOT}/README.md"
    echo '```' >> "${AUTOTEST_ROOT}/README.md"
    echo "" >> "${AUTOTEST_ROOT}/README.md"
    echo "## Best Practices" >> "${AUTOTEST_ROOT}/README.md"
    echo "" >> "${AUTOTEST_ROOT}/README.md"
    echo "1. AAA Pattern: Arrange-Act-Assert" >> "${AUTOTEST_ROOT}/README.md"
    echo "2. Test Independence: Each test runs independently" >> "${AUTOTEST_ROOT}/README.md"
    echo "3. Stub Usage: Isolate external dependencies" >> "${AUTOTEST_ROOT}/README.md"
    echo "4. Coverage: Target > 80%" >> "${AUTOTEST_ROOT}/README.md"

    print_success "生成 autotests/README.md"
}

generate_readme
