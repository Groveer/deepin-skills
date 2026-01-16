#!/usr/bin/env python3
"""
Qt Translation Assistant (Subagent版本)
用于解析TS文件中未完成的翻译，通过subagent调用AI进行翻译并自动写入结果
"""

import os
import re
import sys
import json
from xml.etree import ElementTree as ET
from pathlib import Path
from typing import Dict, List, Tuple

# 导入subagent协调器
from subagent.translation_coordinator import TranslationCoordinator


def find_unfinished_translations(ts_file_path):
    """
    查找TS文件中未完成的翻译
    返回: [{'source': str, 'translation_elem': element, 'context': str, 'full_message': element}, ...]
    """
    with open(ts_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 预处理XML内容，处理可能的格式问题
    try:
        # 尝试找到第一个完整的TS块
        import re
        ts_match = re.search(r'(<\?xml[^\?]*\?>\s*)?(<!DOCTYPE[^>]*>\s*)?<TS[^>]*>.*?</TS>', content, re.DOTALL)
        if ts_match:
            content = ts_match.group(0)

        # 使用字符串替换修复常见的XML问题
        content = content.replace(' encoding="UTF-8"', '')

        # 解析XML来获取完整的上下文
        import io
        tree = ET.parse(io.StringIO(content))
        root = tree.getroot()

        results = []
        # 遍历所有的context
        for context in root.findall('context'):
            context_name = context.find('name').text if context.find('name') is not None else 'Unknown'

            # 在每个context中查找message
            for message in context.findall('message'):
                translation_elem = message.find('translation')
                if translation_elem is not None and translation_elem.get('type') == 'unfinished':
                    source_elem = message.find('source')
                    if source_elem is not None:
                        results.append({
                            'source': source_elem.text or '',
                            'translation_elem': translation_elem,
                            'context': context_name,
                            'full_message': message
                        })

        return results
    except ET.ParseError as e:
        print(f"无法解析XML文件: {ts_file_path}, 错误: {e}")
        return []
    except Exception as e:
        print(f"处理XML文件时发生错误: {ts_file_path}, 错误: {e}")
        return []


def get_language_from_filename(filename):
    """从文件名中提取语言代码"""
    # 例如: xxx_de.ts -> de
    #      xxx_zh_CN.ts -> zh_CN
    #      xxx.ts -> unknown (英文文件，不需要翻译)
    name = Path(filename).stem
    if '_' in name:
        parts = name.split('_')
        if len(parts) >= 2:
            lang_part = '_'.join(parts[1:])
            return lang_part
    # 如果没有语言后缀，返回'unknown'表示英文原文件
    return 'unknown'


def get_example_translations(language_code, ts_file):
    """获取已有的翻译示例来增加目标语言的确定性"""
    examples = []

    # 尝试从各种源文件中获取翻译示例
    files_to_check = [ts_file]  # 首先检查当前文件

    # 添加相似语言文件（如 ku_IQ.ts, ku_IR.ts 等）
    base_name = Path(ts_file).stem
    if '_' in base_name:
        base_lang = base_name.split('_')[1] # 例如 'ku' from 'dde-cooperation_ku'
    else:
        base_lang = base_name

    ts_dir = Path(ts_file).parent
    similar_files = list(ts_dir.glob(f"*_{base_lang}_*.ts"))
    other_lang_files = list(ts_dir.glob(f"*{base_lang}*.ts"))

    # 构建检查顺序：当前文件 -> 相似文件 -> 其他语言文件
    files_to_check = [ts_file]
    files_to_check.extend(similar_files)
    for other_file in other_lang_files:
        if other_file not in files_to_check:
            files_to_check.append(other_file)

    # 遍历所有文件寻找已翻译的内容
    for file_to_check in files_to_check:
        try:
            # 尝试解析文件，如果失败则尝试更宽松的方法
            try:
                tree = ET.parse(file_to_check)
                root = tree.getroot()
            except ET.ParseError:
                # 如果直接解析失败，尝试预处理文件内容
                with open(file_to_check, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 简单的预处理：尝试找到第一个有效的<TS>标签内容
                import re
                # 找到第一个完整的TS块
                ts_match = re.search(r'(<\?xml[^\?]*\?>\s*)?(<!DOCTYPE[^>]*>\s*)?<TS[^>]*>.*?</TS>', content, re.DOTALL)
                if ts_match:
                    ts_content = ts_match.group(0)
                    # 检查是否有多个根元素，如果有，只取第一个
                    if ts_content.count('<TS') > 1:
                        # 找到第一个完整的TS块
                        first_end = ts_content.find('</TS>') + 4
                        if first_end > 3:  # 确保找到了结束标签
                            ts_content = ts_content[:first_end]

                import io
                tree = ET.parse(io.StringIO(ts_content))
                root = tree.getroot()

            # 遍历所有message元素寻找已翻译的内容
            for message in root.iter('message'):
                source_elem = message.find('source')
                translation_elem = message.find('translation')
                if (source_elem is not None and translation_elem is not None and
                    translation_elem.text and translation_elem.get('type') != 'unfinished'):
                    example_tuple = (source_elem.text or '', translation_elem.text)
                    if example_tuple not in examples:  # 避免重复
                        examples.append(example_tuple)
                    if len(examples) >= 5:  # 只取前5个示例
                        break

            if len(examples) >= 3:  # 如果已经有足够示例，就停止
                break

        except ET.ParseError:
            continue
        except Exception:
            continue

    return examples


def write_translations_back(ts_file_path, translation_results):
    """
    将翻译结果写回TS文件
    translation_results: [{'source': '原文', 'translation': '译文'}, ...]
    """
    # 使用XML解析来处理翻译替换，这样可以正确处理XML实体
    tree = ET.parse(ts_file_path)
    root = tree.getroot()

    # 创建源文本到翻译文本的映射字典，用于快速查找
    translation_map = {item['source']: item['translation'] for item in translation_results}

    # 遍历所有message元素
    for message in root.iter('message'):
        source_elem = message.find('source')
        translation_elem = message.find('translation')

        if (source_elem is not None and translation_elem is not None and
            translation_elem.get('type') == 'unfinished'):

            source_text = source_elem.text or ''

            # 检查是否在翻译映射中
            if source_text in translation_map:
                # 更新translation元素：移除type属性，设置新的翻译文本
                if 'type' in translation_elem.attrib:
                    del translation_elem.attrib['type']
                translation_elem.text = translation_map[source_text]

    # 写回文件，保持原有的XML格式和编码
    # 使用原始的XML声明和DOCTYPE
    with open(ts_file_path, 'r', encoding='utf-8') as f:
        original_content = f.read()

    # 找到XML声明和DOCTYPE
    xml_declaration = ''
    doctype = ''
    content_lines = original_content.split('\\n')

    for i, line in enumerate(content_lines):
        if line.strip().startswith('<?xml'):
            xml_declaration = line
        elif line.strip().startswith('<!DOCTYPE'):
            doctype = line
        elif line.strip().startswith('<TS'):
            break

    # 生成新的XML内容
    import io
    from xml.dom import minidom

    # 方法1: 使用ElementTree直接写入（保持基本格式）
    output = io.StringIO()
    # 临时保存，然后读取以获取字符串格式
    tree.write(output, encoding='unicode', xml_declaration=False)
    new_content = output.getvalue()

    # 重新解析以获得更好的格式
    dom = minidom.parseString(new_content.encode('utf-8'))
    pretty_xml = dom.toprettyxml(indent="    ", encoding=None)
    # 移除多余的空行
    lines = pretty_xml.split('\\n')
    pretty_xml = '\\n'.join([line for line in lines if line.strip()])

    # 替换根元素的开始标签以保持TS版本等属性
    if '<TS ' in pretty_xml:
        # 找到原始的TS标签
        import re
        ts_match = re.search(r'<TS[^>]*>', original_content)
        if ts_match:
            original_ts_tag = ts_match.group(0)
            # 替换新的TS标签
            pretty_xml = re.sub(r'<TS[^>]*>', original_ts_tag, pretty_xml, count=1)

    # 组合最终内容
    final_content = ""
    if xml_declaration:
        final_content += xml_declaration + '\\n'
    if doctype:
        final_content += doctype + '\\n'
    final_content += pretty_xml

    # 写回文件
    with open(ts_file_path, 'w', encoding='utf-8') as f:
        f.write(final_content)


def translate_single_file_with_subagent(ts_file_path: str, config_path: str, batch_size: int = 10):
    """使用subagent翻译单个文件"""
    print(f"处理文件: {ts_file_path}")

    unfinished_items = find_unfinished_translations(ts_file_path)

    if not unfinished_items:
        print("  没有找到未完成的翻译")
        return True, []  # 成功, 无失败文件

    print(f" 找到 {len(unfinished_items)} 个未完成的翻译")

    language_code = get_language_from_filename(os.path.basename(ts_file_path))
    print(f"  语言代码: {language_code}")

    # 如果语言代码是'unknown'，表示这是英文原文件，直接将原文作为翻译结果
    if language_code == 'unknown':
        print(f"  检测到英文原文件，将原文直接写入...")
        translation_results = []
        for item in unfinished_items:
            translation_results.append({
                'source': item['source'],
                'translation': item['source']  # 英文原文件，直接使用原文
            })

        # 写入翻译结果
        write_translations_back(ts_file_path, translation_results)
        print(f" 翻译结果已写入文件: {ts_file_path}")

        # 显示翻译结果
        for result in translation_results:
            print(f"  '{result['source']}' -> '{result['translation']}'")
        return True, []  # 成功, 无失败文件

    print(f" 开始使用subagent翻译字符串...")

    # 准备待翻译的字符串列表
    strings_to_translate = [item['source'] for item in unfinished_items]

    # 创建翻译协调器
    coordinator = TranslationCoordinator(config_path)

    try:
        # 通过subagent翻译字符串
        translation_results = coordinator.translate_strings_via_subagent(
            strings_to_translate,
            language_code,
            ts_file_path,
            batch_size=batch_size
        )

        # 验证翻译结果数量是否匹配
        if len(translation_results) != len(unfinished_items):
            print(f"  警告: 翻译结果数量不匹配，期望{len(unfinished_items)}，得到{len(translation_results)}")
            return False, [ts_file_path]

        # 写入翻译结果
        write_translations_back(ts_file_path, translation_results)
        print(f" 所有翻译结果已写入文件: {ts_file_path}")

        # 显示部分翻译结果
        for i, result in enumerate(translation_results[:5]):  # 只显示前5个
            print(f"  '{result['source']}' -> '{result['translation']}'")
        if len(translation_results) > 5:
            print(f"  ... 还有 {len(translation_results) - 5} 个翻译")

        return True, []

    except Exception as e:
        print(f"  翻译过程中出错: {str(e)}")
        return False, [ts_file_path]


def process_translations_directory_with_subagent(directory_path: str, config_path: str, batch_size: int = 10):
    """使用subagent处理整个翻译目录"""
    # 只查找根目录下的TS文件，不递归查找子目录
    ts_files = list(Path(directory_path).glob('*.ts'))

    print(f"找到 {len(ts_files)} 个TS文件")

    # 过滤掉英文文件（en.ts, en_US.ts等），但保留zh_CN.ts
    filtered_ts_files = []
    for ts_file in ts_files:
        if 'en' in str(ts_file).lower() and not str(ts_file).endswith('zh_CN.ts'):
            continue
        filtered_ts_files.append(ts_file)

    print(f"过滤后剩余 {len(filtered_ts_files)} 个需要翻译的文件")

    # 逐个处理文件（可以在这里添加并行处理逻辑）
    for ts_file in filtered_ts_files:
        print(f"\\n处理文件: {ts_file}")

        # 翻译单个文件
        success, failed_files = translate_single_file_with_subagent(
            str(ts_file), config_path, batch_size
        )

        if success:
            print(f"✓ 文件 {ts_file} 翻译成功")
        else:
            print(f"✗ 文件 {ts_file} 翻译失败: {failed_files}")


def load_config(config_path: str = "qt_translation_config.json") -> dict:
    """加载配置文件"""
    if not os.path.exists(config_path):
        print(f"配置文件 {config_path} 不存在")
        return None

    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    return config


def create_config_file(config_path: str = "qt_translation_config.json"):
    """创建配置文件模板"""
    config = {
        "api_url": "https://api.openai.com/v1/chat/completions",
        "api_key": "your-api-key-here",
        "model": "gpt-3.5-turbo"
    }

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print(f"已创建 {config_path}，请编辑其中的API配置")


def main():
    if len(sys.argv) < 2:
        print("用法: python qt_translation_assistant_subagent.py <directory_path> [ts_file_path]")
        print("  --config: 创建配置文件模板")
        print("  --batch-size: 设置批处理大小 (默认10)")
        print("  directory_path: 翻译文件目录路径")
        print("  ts_file_path: 可选，指定单个TS文件路径")
        return

    # 检查配置参数
    if '--config' in sys.argv:
        config_path = 'qt_translation_config.json'
        # 检查是否指定了自定义配置文件路径
        for i, arg in enumerate(sys.argv):
            if arg == '--config' and i + 1 < len(sys.argv) and not sys.argv[i + 1].startswith('--'):
                config_path = sys.argv[i + 1]
                break
        create_config_file(config_path)
        return

    # 解析批处理大小
    batch_size = 10
    if '--batch-size' in sys.argv:
        idx = sys.argv.index('--batch-size')
        if idx + 1 < len(sys.argv):
            try:
                batch_size = int(sys.argv[idx + 1])
            except ValueError:
                print("错误: 批处理大小必须是数字")
                return

    # 检查配置文件
    config_path = 'qt_translation_config.json'
    config = load_config(config_path)
    if not config:
        print("错误: 无法加载配置文件。请使用 --config 参数创建配置文件。")
        return

    # 获取参数（移除配置相关参数）
    args = [arg for arg in sys.argv[1:] if arg != '--config' and arg != '--batch-size' and arg != str(batch_size)]

    if len(args) < 1:
        print("错误: 缺少文件或目录参数")
        return

    # 检查第一个参数是目录还是文件
    if os.path.isfile(args[0]):
        # 处理单个文件
        ts_file_path = args[0]
        translate_single_file_with_subagent(ts_file_path, config_path, batch_size)

    elif os.path.isdir(args[0]):
        # 处理整个目录或单个文件
        directory_path = args[0]

        if len(args) == 2 and os.path.isfile(args[1]):
            # 处理单个文件
            ts_file_path = args[1]
            translate_single_file_with_subagent(ts_file_path, config_path, batch_size)
        elif len(args) == 1:
            # 处理整个目录
            if os.path.exists(directory_path):
                process_translations_directory_with_subagent(directory_path, config_path, batch_size)
            else:
                print(f"目录不存在: {directory_path}")
        else:
            print("错误: 参数数量不正确")
    else:
        print(f"路径不存在: {args[0]}")


if __name__ == "__main__":
    main()