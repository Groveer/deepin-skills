---
name: qt-translation-assistant
description: Use when user requests translating Qt project localization files (TS files), automating translation workflows, or setting up multilingual support for Qt applications. This skill leverages AI models through a subagent architecture to translate TS (Translation Source) files efficiently.
---

# Qt Translation Assistant Skill

## Iron Laws

1. **Never modify original TS files without backup** - Always preserve original content
2. **Validate AI translation quality** - Verify translations are accurate and contextually appropriate
3. **Maintain translation consistency** - Use consistent terminology across all translations
4. **Respect file encoding** - Preserve UTF-8 encoding and special characters

## Red Flags

- User requests translation of non-TS files
- User asks to translate without proper AI configuration
- Requests to overwrite existing translations without verification
- Asks to translate to unsupported language codes

## Rationalization Table

| Excuse | Response |
|--------|----------|
| "Just translate everything quickly" | Quality matters in localization - proper AI configuration and validation required |
| "We don't need consistent terminology" | Inconsistent translations hurt user experience - consistency is critical |
| "Original files don't need backup" | Always preserve originals - translation errors can corrupt content |

## Quick Reference

### Core Commands
```bash
# Translate entire directory of TS files
python translate.py /path/to/ts/files/

# Translate specific file
python translate.py /path/to/ts/files/ /path/to/specific/file.ts

# With custom batch size
python translate.py --batch-size 20 /path/to/ts/files/

# Create configuration file
python translate.py --config

# Direct subagent usage
python -m subagent.translation_subagent --config config.json --strings "Hello" "World" --language zh-CN
```

### Configuration
```json
{
  "api_url": "http://localhost:8080/v1/chat/completions",
  "api_key": "sk-uos-12345",
  "model": "qwen3-coder-flash"
}
```

## Common Mistakes & Fixes

### Mistake: AI provider not configured properly
**Fix**: Run configuration tool or manually create `qt_translation_config.json` with valid API credentials

### Mistake: Large files causing API timeouts
**Fix**: Reduce batch size using `--batch-size` parameter to process smaller chunks

### Mistake: Language codes not detected correctly
**Fix**: Ensure TS files follow standard naming convention (e.g., `project_zh_CN.ts`, `project_de.ts`)

### Mistake: Translation quality issues
**Fix**: Review and refine AI model selection, adjust temperature settings in configuration

## Architecture

This skill uses a subagent architecture:
- **Main Skill**: Handles TS file parsing and result writing
- **Translation Subagent**: Handles AI API calls independently
- **Coordinator**: Manages communication between main skill and subagent

This design improves performance by isolating AI processing and allows for better error handling.

## Key Features

- Smart parsing of TS files to identify incomplete translations
- Subagent architecture for improved performance and error isolation
- Support for multiple AI providers (OpenAI, Anthropic, DeepSeek, local servers)
- Batch processing for efficient translation of multiple strings
- Language-specific translation guidance (scripts, RTL, etc.)
- Consistency preservation across translations