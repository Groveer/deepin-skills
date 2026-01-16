# Qt Translation Assistant (Subagent Architecture)

Automated translation tool for Qt projects using AI models to translate TS (Translation Source) files. Uses a subagent architecture for improved performance and modularity.

## Features

- **Smart Parsing**: Identifies incomplete translations in Qt TS files
- **AI-Powered Translation**: Uses advanced language models for accurate translations
- **Subagent Architecture**: Decouples AI processing for better performance
- **Batch Processing**: Efficiently translates multiple strings in batches
- **Consistency**: Maintains translation consistency across the project
- **Multi-Language Support**: Handles special language requirements (scripts, RTL, etc.)

## Architecture

This tool uses a subagent architecture:
- **Main Skill**: Handles TS file parsing and result writing
- **Translation Subagent**: Handles AI API calls independently
- **Coordinator**: Manages communication between main skill and subagent

This design improves performance by isolating AI processing and allows for better error handling.

## Installation

1. Ensure Python 3.7+ is installed
2. Install dependencies:
   ```bash
   pip install requests
   ```

## Configuration

The tool uses `qt_translation_config.json` for AI provider settings:

```json
{
  "api_url": "http://localhost:8080/v1/chat/completions",
  "api_key": "sk-uos-12345",
  "model": "qwen3-coder-flash"
}
```

Create the config file:
```bash
python translate.py --config
```

## Usage

### Translate entire directory:
```bash
python translate.py /path/to/ts/files/
```

### Translate specific file:
```bash
python translate.py /path/to/ts/files/ /path/to/specific/file.ts
```

### With custom batch size:
```bash
python translate.py --batch-size 20 /path/to/ts/files/
```

## Supported Languages

- Kurdish (with Arabic script support)
- Chinese (Traditional/Simplified)
- Arabic (RTL support)
- Japanese (Kanji/Hiragana/Katakana)
- Korean (Hangul)
- Thai (Thai script)
- And many more...

## Configuration Options

The script intelligently extracts translation examples from existing translations to maintain consistency. It also provides language-specific guidance to ensure proper script usage and terminology.

## Troubleshooting

- If translations fail, check your API configuration in `qt_translation_config.json`
- Ensure your AI provider supports the target language
- Large files are processed in batches to avoid API limits
- Use appropriate batch sizes based on your AI provider's rate limits