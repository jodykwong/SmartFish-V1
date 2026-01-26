#!/usr/bin/env python3
"""
修复章节JSON中的嵌套JSON文本问题
"""
import json
import re
from pathlib import Path

def extract_nested_json_text(text: str) -> str:
    """提取嵌套JSON中的纯文本"""
    if not text or not isinstance(text, str):
        return text or ""
    
    stripped = text.strip()
    if not (stripped.startswith("{") and stripped.endswith("}")):
        return text
    
    try:
        data = json.loads(stripped)
        if not isinstance(data, dict):
            return text
        
        doc_type = data.get("type")
        if doc_type not in ("doc", "paragraph", "text"):
            return text
        
        extracted_texts = []
        recursive_extract_text(data, extracted_texts)
        
        if extracted_texts:
            return " ".join(extracted_texts)
        return text
    except (json.JSONDecodeError, Exception):
        return text

def recursive_extract_text(node, result):
    """递归提取文本"""
    if isinstance(node, str):
        if node.strip():
            result.append(node.strip())
    elif isinstance(node, dict):
        if "text" in node and isinstance(node["text"], str):
            text_val = node["text"].strip()
            if text_val and not (text_val.startswith("{") and text_val.endswith("}")):
                result.append(text_val)
        if "content" in node:
            recursive_extract_text(node["content"], result)
    elif isinstance(node, list):
        for item in node:
            recursive_extract_text(item, result)

def fix_inlines(inlines):
    """修复inlines中的嵌套JSON"""
    if not isinstance(inlines, list):
        return inlines
    
    for inline in inlines:
        if isinstance(inline, dict) and "text" in inline:
            inline["text"] = extract_nested_json_text(inline["text"])
    return inlines

def fix_blocks(blocks):
    """递归修复blocks"""
    if not isinstance(blocks, list):
        return blocks
    
    for block in blocks:
        if not isinstance(block, dict):
            continue
        
        # 修复paragraph的inlines
        if "inlines" in block:
            fix_inlines(block["inlines"])
        
        # 递归处理嵌套blocks
        if "blocks" in block and isinstance(block["blocks"], list):
            fix_blocks(block["blocks"])
        
        # 处理list items
        if "items" in block and isinstance(block["items"], list):
            for item in block["items"]:
                if isinstance(item, list):
                    fix_blocks(item)
        
        # 处理table cells
        if "rows" in block and isinstance(block["rows"], list):
            for row in block["rows"]:
                if isinstance(row, dict) and "cells" in row:
                    for cell in row["cells"]:
                        if isinstance(cell, dict) and "blocks" in cell:
                            fix_blocks(cell["blocks"])
    
    return blocks

def main():
    run_id = "report-26e44774"
    chapters_dir = Path(f"final_reports/chapters/{run_id}")
    
    fixed_count = 0
    
    for i in range(1, 8):
        chapter_dir = chapters_dir / f"{i*10:03d}-section-{i}-0"
        chapter_file = chapter_dir / "chapter.json"
        
        if not chapter_file.exists():
            continue
        
        with open(chapter_file, 'r', encoding='utf-8') as f:
            chapter_data = json.load(f)
        
        # 修复blocks
        if "blocks" in chapter_data:
            fix_blocks(chapter_data["blocks"])
        
        # 保存修复后的文件
        with open(chapter_file, 'w', encoding='utf-8') as f:
            json.dump(chapter_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 修复章节 {i}: {chapter_data.get('title', 'N/A')}")
        fixed_count += 1
    
    print(f"\n共修复 {fixed_count} 个章节文件")

if __name__ == "__main__":
    main()
