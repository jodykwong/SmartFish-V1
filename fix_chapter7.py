#!/usr/bin/env python3
"""
快速组装脚本：使用已有的7章数据直接生成HTML报告
"""
import os
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from loguru import logger

def main():
    run_id = "report-26e44774"
    chapters_dir = Path(f"final_reports/chapters/{run_id}")
    
    logger.info(f"使用现有运行: {run_id}")
    
    # 加载所有7章
    chapters = []
    for i in range(1, 8):
        chapter_dir = chapters_dir / f"{i*10:03d}-section-{i}-0"
        chapter_file = chapter_dir / "chapter.json"
        if chapter_file.exists():
            with open(chapter_file, 'r', encoding='utf-8') as f:
                chapter_data = json.load(f)
                chapters.append(chapter_data)
                logger.success(f"✓ 加载章节 {i}: {chapter_data.get('title', 'N/A')}")
    
    logger.info(f"共加载 {len(chapters)} 个章节")
    
    # 加载布局
    layout_file = chapters_dir / "document_layout.json"
    with open(layout_file, 'r', encoding='utf-8') as f:
        layout = json.load(f)
    
    # 组装Document IR
    document_ir = {
        "reportId": run_id,
        "title": layout.get("title", "AI应用创业报告"),
        "toc": layout.get("toc", []),
        "chapters": chapters,
        "meta": layout.get("meta", {}),
    }
    
    # 保存IR
    ir_path = Path("final_reports") / f"document_ir_{run_id}.json"
    with open(ir_path, 'w', encoding='utf-8') as f:
        json.dump(document_ir, f, ensure_ascii=False, indent=2)
    logger.success(f"✓ Document IR 已保存: {ir_path}")
    
    # 渲染HTML
    from ReportEngine.renderers import HTMLRenderer
    renderer = HTMLRenderer()
    html_content = renderer.render(document_ir)
    
    html_path = Path("final_reports") / f"final_report_{run_id}.html"
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    logger.success(f"✓ HTML报告已保存: {html_path}")
    
    logger.info("\n" + "=" * 60)
    logger.success("✓ 报告组装完成！")
    logger.info(f"HTML文件: {html_path}")
    logger.info("=" * 60)

if __name__ == "__main__":
    main()
