#!/usr/bin/env python3
"""
翻译 Subagent 服务
接收翻译请求并通过配置的AI提供商进行翻译
"""

import json
import requests
import argparse
import sys
import os
from pathlib import Path


class TranslationSubagent:
    def __init__(self, config_path="qt_translation_config.json"):
        """
        初始化翻译子代理
        :param config_path: 配置文件路径
        """
        self.config = self.load_config(config_path)

    def load_config(self, config_path):
        """加载配置文件"""
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"配置文件不存在: {config_path}")

        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def call_llm_api(self, prompt: str) -> str:
        """
        调用LLM API进行翻译
        :param prompt: 提示词
        :return: API返回的响应文本
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {self.config['api_key']}"
        }

        data = {
            'model': self.config.get('model', 'gpt-3.5-turbo'),
            'messages': [
                {'role': 'user', 'content': prompt}
            ],
            'temperature': self.config.get('temperature', 0.3),
            'max_tokens': 4000
        }

        response = requests.post(
            self.config['api_url'],
            headers=headers,
            json=data,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        else:
            raise Exception(f"API调用失败: {response.status_code} - {response.text}")

    def translate_strings(self, strings_list: list, target_language: str, source_file: str = "") -> list:
        """
        翻译字符串列表
        :param strings_list: 待翻译的字符串列表
        :param target_language: 目标语言
        :param source_file: 源文件路径（用于上下文）
        :return: 翻译结果列表
        """
        if not strings_list:
            return []

        # 构建提示词
        prompt = self._build_translation_prompt(strings_list, target_language, source_file)

        # 调用LLM API
        response_text = self.call_llm_api(prompt)

        # 解析响应
        return self._parse_translation_response(response_text, strings_list)

    def _build_translation_prompt(self, strings_list: list, target_language: str, source_file: str) -> str:
        """
        构建翻译提示词
        :param strings_list: 待翻译的字符串列表
        :param target_language: 目标语言
        :param source_file: 源文件路径
        :return: 构建好的提示词
        """
        prompt = f"""请将以下字符串翻译为{target_language}语言。
目标语言: {target_language}
源文件: {source_file if source_file else 'Unknown'}

字符串列表:
"""

        for i, string in enumerate(strings_list, 1):
            prompt += f"\n{i}. {string}\n"

        prompt += f"""

请按以下JSON格式返回翻译结果:
{json.dumps([{'source': s, 'translation': 'your translation here'} for s in strings_list], ensure_ascii=False, indent=2)}

重要说明:
- 严格按照JSON格式返回
- 保持翻译的准确性
- 保持术语的一致性
- 不要在JSON之外添加其他文本
"""
        return prompt

    def _parse_translation_response(self, response_text: str, original_strings: list) -> list:
        """
        解析LLM返回的翻译结果
        :param response_text: LLM返回的文本
        :param original_strings: 原始字符串列表
        :return: 翻译结果列表
        """
        import re

        # 尝试直接解析JSON
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            pass

        # 尝试提取JSON部分
        json_match = re.search(r'\[(?:[^][]++|\[(?:[^][]++|\[[^][]*\])*\])*\]', response_text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass

        # 如果无法解析JSON，返回原始字符串（这通常不应该发生）
        print("警告: 无法解析翻译响应，返回原始字符串")
        return [{'source': s, 'translation': s} for s in original_strings]


def main():
    parser = argparse.ArgumentParser(description='翻译 Subagent 服务')
    parser.add_argument('--config', type=str, default='qt_translation_config.json',
                       help='配置文件路径')
    parser.add_argument('--input', type=str, help='输入JSON文件路径')
    parser.add_argument('--output', type=str, help='输出JSON文件路径')
    parser.add_argument('--strings', type=str, nargs='+', help='待翻译的字符串')
    parser.add_argument('--language', type=str, required=True, help='目标语言')
    parser.add_argument('--source-file', type=str, default='', help='源文件路径')

    args = parser.parse_args()

    # 初始化翻译子代理
    subagent = TranslationSubagent(args.config)

    # 确定输入字符串
    if args.input:
        # 从文件读取
        with open(args.input, 'r', encoding='utf-8') as f:
            input_data = json.load(f)
            strings_to_translate = input_data.get('strings', [])
            target_language = input_data.get('language', args.language)
            source_file = input_data.get('source_file', args.source_file)
    elif args.strings:
        # 从命令行参数获取
        strings_to_translate = args.strings
        target_language = args.language
        source_file = args.source_file
    else:
        print("错误: 必须提供输入文件或字符串")
        sys.exit(1)

    try:
        # 执行翻译
        results = subagent.translate_strings(strings_to_translate, target_language, source_file)

        # 输出结果
        if args.output:
            # 保存到文件
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"翻译结果已保存到: {args.output}")
        else:
            # 输出到标准输出
            print(json.dumps(results, ensure_ascii=False, indent=2))

    except Exception as e:
        print(f"翻译过程中出现错误: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()