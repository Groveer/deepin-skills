#!/usr/bin/env python3
"""
Qt Translation Assistant - 配置工具
用于交互式配置AI提供商和翻译设置
"""

import json
import os
from pathlib import Path


def load_config_template():
    """加载配置模板"""
    config_path = Path(__file__).parent / "config_template.json"
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # 返回默认配置
        return {
            "default_providers": {
                "openai": {
                    "api_url": "https://api.openai.com/v1/chat/completions",
                    "api_key": "your-openai-api-key-here",
                    "model": "gpt-4-turbo"
                },
                "anthropic": {
                    "api_url": "https://api.anthropic.com/v1/messages",
                    "api_key": "your-anthropic-api-key-here",
                    "model": "claude-3-5-sonnet-20241022"
                },
                "deepseek": {
                    "api_url": "https://api.deepseek.com/v1/chat/completions",
                    "api_key": "your-deepseek-api-key-here",
                    "model": "deepseek-chat"
                }
            },
            "current_provider": "deepseek",
            "translation_settings": {
                "batch_size": 10,
                "max_workers": 3,
                "max_retries": 2,
                "temperature": 0.3
            },
            "language_specific_rules": {
                "ku": {
                    "script": "arabic",
                    "guidance": "FOR KURDISTANI LANGUAGE: Use ARABIC SCRIPT (NOT Latin script) - this is CRITICAL"
                },
                "zh": {
                    "script": "chinese",
                    "guidance": "FOR CHINESE LANGUAGE: Use appropriate traditional or simplified characters as shown in examples"
                },
                "ar": {
                    "script": "arabic_rtl",
                    "guidance": "FOR ARABIC LANGUAGE: Use RTL script and proper Arabic typography"
                },
                "ja": {
                    "script": "japanese",
                    "guidance": "FOR JAPANESE LANGUAGE: Use appropriate kanji, hiragana, and katakana as shown in examples"
                },
                "ko": {
                    "script": "hangul",
                    "guidance": "FOR KOREAN LANGUAGE: Use appropriate Hangul characters"
                }
            }
        }


def save_user_config(config, filepath="qt_translation_config.json"):
    """保存用户配置"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"配置已保存到 {filepath}")


def interactive_config_setup():
    """交互式配置设置"""
    print("=== Qt Translation Assistant 配置向导 ===\\n")

    # 加载模板配置
    template_config = load_config_template()

    print("请选择AI提供商:")
    providers = list(template_config["default_providers"].keys())
    for i, provider in enumerate(providers, 1):
        print(f"{i}. {provider.capitalize()}")

    print(f"{len(providers)+1}. 使用自定义提供商")

    while True:
        try:
            choice = input(f"请输入选项 (1-{len(providers)+1}): ").strip()
            choice_num = int(choice)
            if 1 <= choice_num <= len(providers):
                selected_provider = providers[choice_num - 1]
                break
            elif choice_num == len(providers) + 1:
                selected_provider = "custom"
                break
            else:
                print(f"无效选项，请输入 1 到 {len(providers)+1} 之间的数字")
        except ValueError:
            print("请输入有效数字")

    # 如果选择了自定义提供商
    if selected_provider == "custom":
        print("\\n请输入自定义提供商信息:")
        api_url = input("API URL: ").strip()
        api_key = input("API Key: ").strip()
        model = input("Model name: ").strip()

        user_config = {
            "api_url": api_url,
            "api_key": api_key,
            "model": model
        }
    else:
        # 使用预设提供商
        provider_info = template_config["default_providers"][selected_provider]
        print(f"\\n您选择了 {selected_provider.capitalize()} 提供商")
        print(f"API URL: {provider_info['api_url']}")
        print(f"Model: {provider_info['model']}")

        api_key = input(f"请输入 {selected_provider.capitalize()} API Key: ").strip()

        user_config = {
            "api_url": provider_info["api_url"],
            "api_key": api_key,
            "model": provider_info["model"]
        }

    # 询问是否使用默认翻译设置
    print("\\n当前翻译设置:")
    default_settings = template_config["translation_settings"]
    for key, value in default_settings.items():
        print(f"  {key}: {value}")

    use_defaults = input("\\n是否使用默认翻译设置？(y/n, 默认y): ").strip().lower()

    if use_defaults in ['', 'y', 'yes']:
        translation_settings = default_settings
    else:
        print("\\n请输入自定义翻译设置:")
        batch_size = input(f"批次大小 (默认 {default_settings['batch_size']}): ").strip()
        batch_size = int(batch_size) if batch_size else default_settings['batch_size']

        max_workers = input(f"最大工作线程数 (默认 {default_settings['max_workers']}): ").strip()
        max_workers = int(max_workers) if max_workers else default_settings['max_workers']

        max_retries = input(f"最大重试次数 (默认 {default_settings['max_retries']}): ").strip()
        max_retries = int(max_retries) if max_retries else default_settings['max_retries']

        temperature = input(f"温度参数 (默认 {default_settings['temperature']}): ").strip()
        temperature = float(temperature) if temperature else default_settings['temperature']

        translation_settings = {
            "batch_size": batch_size,
            "max_workers": max_workers,
            "max_retries": max_retries,
            "temperature": temperature
        }

    # 合并配置
    final_config = {**user_config, **translation_settings}

    # 询问配置文件保存路径
    config_path = input("\\n请输入配置文件保存路径 (默认: qt_translation_config.json): ").strip()
    if not config_path:
        config_path = "qt_translation_config.json"

    # 保存配置
    save_user_config(final_config, config_path)

    print("\\n=== 配置完成 ===")
    print(f"已配置提供商: {selected_provider if selected_provider != 'custom' else 'Custom Provider'}")
    print(f"模型: {final_config['model']}")
    print(f"配置文件: {config_path}")
    print("\\n现在您可以使用以下命令开始翻译:")
    print(f"python qt_translation_assistant.py <ts_directory_path>")


if __name__ == "__main__":
    interactive_config_setup()