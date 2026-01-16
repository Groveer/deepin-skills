#!/usr/bin/env python3
"""
翻译服务协调器
用于主技能与翻译subagent之间的通信
"""

import subprocess
import json
import tempfile
import os
from pathlib import Path
from typing import List, Dict


class TranslationCoordinator:
    def __init__(self, config_path="qt_translation_config.json"):
        """
        初始化翻译协调器
        :param config_path: 配置文件路径
        """
        self.config_path = config_path

    def translate_strings_via_subagent(self, strings_list: List[str], target_language: str,
                                      source_file: str = "", batch_size: int = 10) -> List[Dict[str, str]]:
        """
        通过subagent翻译字符串列表
        :param strings_list: 待翻译的字符串列表
        :param target_language: 目标语言
        :param source_file: 源文件路径
        :param batch_size: 批处理大小
        :return: 翻译结果列表
        """
        all_results = []

        # 分批处理
        for i in range(0, len(strings_list), batch_size):
            batch = strings_list[i:i + batch_size]
            batch_results = self._translate_batch(batch, target_language, source_file)
            all_results.extend(batch_results)

        return all_results

    def _translate_batch(self, batch: List[str], target_language: str, source_file: str) -> List[Dict[str, str]]:
        """
        翻译单个批次的字符串
        :param batch: 批次字符串列表
        :param target_language: 目标语言
        :param source_file: 源文件路径
        :return: 翻译结果
        """
        # 创建临时输入文件
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json', encoding='utf-8') as temp_input:
            input_data = {
                'strings': batch,
                'language': target_language,
                'source_file': source_file
            }
            json.dump(input_data, temp_input, ensure_ascii=False, indent=2)
            temp_input_path = temp_input.name

        # 创建临时输出文件
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json', encoding='utf-8') as temp_output:
            temp_output_path = temp_output.name

        try:
            # 调用subagent
            cmd = [
                'python', '-m', 'subagent.translation_subagent',
                '--config', self.config_path,
                '--input', temp_input_path,
                '--output', temp_output_path,
                '--language', target_language
            ]

            if source_file:
                cmd.extend(['--source-file', source_file])

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

            if result.returncode != 0:
                raise Exception(f"Subagent调用失败: {result.stderr}")

            # 读取翻译结果
            with open(temp_output_path, 'r', encoding='utf-8') as f:
                results = json.load(f)

            return results

        finally:
            # 清理临时文件
            os.unlink(temp_input_path)
            os.unlink(temp_output_path)

    def translate_single_string(self, string: str, target_language: str, source_file: str = "") -> str:
        """
        翻译单个字符串
        :param string: 待翻译的字符串
        :param target_language: 目标语言
        :param source_file: 源文件路径
        :return: 翻译结果
        """
        cmd = [
            'python', '-m', 'subagent.translation_subagent',
            '--config', self.config_path,
            '--strings', string,
            '--language', target_language
        ]

        if source_file:
            cmd.extend(['--source-file', source_file])

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            raise Exception(f"Subagent调用失败: {result.stderr}")

        # 解析输出
        try:
            results = json.loads(result.stdout.strip())
            if results and len(results) > 0:
                return results[0]['translation']
            else:
                return string  # 如果没有翻译结果，返回原文
        except json.JSONDecodeError:
            return string  # 如果解析失败，返回原文


def create_subagent_launcher():
    """
    创建subagent启动器，使其可以通过模块方式运行
    """
    launcher_content = '''#!/usr/bin/env python3
"""Subagent启动器"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from subagent.translation_subagent import main

if __name__ == "__main__":
    main()
'''

    with open('/home/zero/work/repo/deepin-skills/qt-translation-assistant/subagent/__main__.py', 'w', encoding='utf-8') as f:
        f.write(launcher_content)


# 创建协调器的__init__.py文件
coordinator_init_content = '''"""
翻译服务协调器模块
"""

from .translation_coordinator import TranslationCoordinator, create_subagent_launcher

__all__ = ['TranslationCoordinator', 'create_subagent_launcher']
'''

with open('/home/zero/work/repo/deepin-skills/qt-translation-assistant/subagent/__init__.py', 'w', encoding='utf-8') as f:
    f.write(coordinator_init_content)