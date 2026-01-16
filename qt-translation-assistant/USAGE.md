# Qt Translation Assistant

Qt Translation Assistant 是一个用于Qt项目TS（Translation Source）文件的自动化翻译工具，使用AI模型进行翻译。

## 功能特性

- 解析TS文件并识别未翻译的字符串
- 使用AI模型进行批量翻译
- 支持多个AI提供商（OpenAI、Anthropic、DeepSeek等）
- 并行处理以提高翻译效率
- 语言特定的翻译指导（如库尔德语使用阿拉伯文字等）
- 翻译一致性维护
- 错误处理和重试机制

## 安装要求

- Python 3.7+
- requests 库

安装依赖：
```bash
pip install requests
```

## 配置AI提供商

### 方法一：使用交互式配置工具

运行配置向导：
```bash
python config_tool.py
```

按照提示选择AI提供商并输入API密钥。

### 方法二：手动创建配置文件

创建 `qt_translation_config.json` 文件：

```json
{
  "api_url": "https://api.openai.com/v1/chat/completions",
  "api_key": "your-api-key-here",
  "model": "gpt-4-turbo",
  "batch_size": 10,
  "max_workers": 3,
  "max_retries": 2,
  "temperature": 0.3
}
```

## 使用方法

### 翻译整个目录中的TS文件

```bash
python qt_translation_assistant.py /path/to/ts/files/
```

### 翻译单个TS文件

```bash
python qt_translation_assistant.py /path/to/ts/files/ /path/to/specific/file.ts
```

### 使用并行处理（默认启用）

```bash
python qt_translation_assistant.py --parallel /path/to/ts/files/
```

### 创建配置文件模板

```bash
python qt_translation_assistant.py --config
```

## 配置选项

- `api_url`: AI服务的端点URL
- `api_key`: API认证密钥
- `model`: 使用的AI模型名称
- `batch_size`: 每批处理的字符串数量（默认10）
- `max_workers`: 最大并行工作线程数（默认3）
- `max_retries`: 最大重试次数（默认2）
- `temperature`: AI生成的随机性参数（默认0.3）

## 支持的语言

工具对以下语言提供特殊支持：
- 库尔德语（使用阿拉伯文字）
- 中文（简繁体）
- 阿拉伯语（RTL布局）
- 日语（汉字/平假名/片假名）
- 韩语（韩文）
- 泰语（泰文）

## 并行处理

工具支持两种级别的并行处理：
1. 文件级别：同时处理多个TS文件
2. 字符串级别：将单个文件中的字符串分成批次并行翻译

## 故障排除

- 如果翻译失败，请检查API配置是否正确
- 确保AI提供商支持目标语言
- 对于大文件，工具会自动分批处理以避免API限制
- 如果遇到网络问题，工具会自动重试

## 最佳实践

1. 在使用前配置有效的AI提供商
2. 翻译完成后检查质量
3. 保持术语的一致性
4. 定期更新现有翻译