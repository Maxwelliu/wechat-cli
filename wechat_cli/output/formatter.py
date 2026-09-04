"""输出格式化 — JSON (大模型友好) / Text (人类可读)"""

import json
import sys


def output_json(data, file=None):
    target = file or sys.stdout
    try:
        json.dump(data, target, ensure_ascii=False, indent=2)
        target.write('\n')
    except UnicodeEncodeError:
        content = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
        if hasattr(target, 'buffer'):
            target.buffer.write(content.encode('utf-8', errors='replace'))
        else:
            target.write(content.encode(getattr(target, 'encoding', 'utf-8') or 'utf-8', errors='replace').decode(getattr(target, 'encoding', 'utf-8') or 'utf-8'))


def output_text(text, file=None):
    target = file or sys.stdout
    try:
        target.write(text)
        if not text.endswith('\n'):
            target.write('\n')
    except UnicodeEncodeError:
        if not text.endswith('\n'):
            text = text + '\n'
        if hasattr(target, 'buffer'):
            target.buffer.write(text.encode('utf-8', errors='replace'))
        else:
            target.write(text.encode(getattr(target, 'encoding', 'utf-8') or 'utf-8', errors='replace').decode(getattr(target, 'encoding', 'utf-8') or 'utf-8'))


def output(data, fmt='json', file=None):
    if fmt == 'json':
        output_json(data, file)
    else:
        if isinstance(data, str):
            output_text(data, file)
        elif isinstance(data, dict) and 'text' in data:
            output_text(data['text'], file)
        else:
            output_json(data, file)
