# Qt Translation Assistant Subagent 架构说明

## 概述
Qt Translation Assistant 现在使用subagent架构，将AI调用逻辑与TS文件处理逻辑分离，提高了性能和可维护性。

## 架构组成

### 1. 主技能 (qt_translation_assistant_subagent.py)
- 负责解析TS文件和写入翻译结果
- 调用协调器来处理翻译任务
- 处理TS文件的读取和XML解析

### 2. 翻译Subagent (subagent/translation_subagent.py)
- 独立的AI调用服务
- 通过命令行接口接收翻译请求
- 直接与AI提供商API通信
- 返回标准化的JSON格式结果

### 3. 协调器 (subagent/translation_coordinator.py)
- 在主技能和subagent之间进行通信
- 管理批处理逻辑
- 处理临时文件和进程调用

## 工作流程

1. 主技能解析TS文件，找出需要翻译的字符串
2. 主技能调用协调器，传递字符串列表和目标语言
3. 协调器将翻译请求打包成临时文件
4. 协调器启动subagent进程，传入配置和请求文件
5. Subagent调用AI API进行翻译
6. Subagent将结果写入输出文件
7. 协调器读取结果并返回给主技能
8. 主技能将翻译结果写入TS文件

## 性能优势

1. **进程隔离**: AI调用在独立进程中进行，不会阻塞主程序
2. **资源管理**: 更好地控制内存和网络资源
3. **错误隔离**: AI调用失败不会影响主程序
4. **可扩展性**: 可以轻松替换不同的AI提供商
5. **批处理优化**: 有效管理批处理大小和频率

## 使用方法

### 安装依赖
```bash
pip install requests
```

### 创建配置文件
```bash
python qt_translate.py --config
```

### 编辑配置文件
编辑 `qt_translation_config.json` 文件，填入AI提供商的API URL、密钥和模型信息。

### 翻译TS文件
```bash
# 翻译目录中的所有TS文件
python qt_translate.py /path/to/ts/files/

# 翻译单个TS文件
python qt_translate.py /path/to/ts/files/ /path/to/specific/file.ts

# 使用自定义批处理大小
python qt_translate.py --batch-size 20 /path/to/ts/files/
```

## 配置文件格式

```json
{
  "api_url": "https://api.openai.com/v1/chat/completions",
  "api_key": "your-api-key-here",
  "model": "gpt-4-turbo"
}
```

## 批处理说明

- 默认批处理大小为10个字符串
- 可通过 `--batch-size` 参数调整
- 较大的批次可以提高效率，但可能受AI提供商限制
- 较小的批次响应更快，适合调试

## 错误处理

- 网络错误会自动重试
- API限流错误会被捕获和报告
- JSON解析错误会尝试多种解析方法
- 临时文件会在使用后清理

## 扩展性

这种架构使得添加新的AI提供商变得简单：
1. 修改配置文件支持新的提供商格式
2. Subagent会自动使用新配置进行API调用
3. 无需修改主技能代码

## 最佳实践

1. 根据AI提供商的速率限制调整批处理大小
2. 定期检查API使用量和成本
3. 保留原始TS文件的备份
4. 验证翻译结果的质量
5. 使用版本控制系统跟踪翻译更改