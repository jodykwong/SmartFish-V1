"""
Report Engine提示词模块。

集中导出各阶段系统提示词与辅助函数，其他模块可直接from prompts import。
"""

from .prompts import (
    SYSTEM_PROMPT_TEMPLATE_SELECTION,
    SYSTEM_PROMPT_HTML_GENERATION,
    SYSTEM_PROMPT_CHAPTER_JSON,
    SYSTEM_PROMPT_CHAPTER_JSON_REPAIR,
    SYSTEM_PROMPT_CHAPTER_JSON_RECOVERY,
    SYSTEM_PROMPT_DOCUMENT_LAYOUT,
    SYSTEM_PROMPT_WORD_BUDGET,
    SYSTEM_PROMPT_CHAPTER_OUTLINE,
    SYSTEM_PROMPT_SUBSECTION_CONTENT,
    output_schema_template_selection,
    input_schema_html_generation,
    chapter_generation_input_schema,
    build_chapter_user_prompt,
    build_chapter_repair_prompt,
    build_chapter_recovery_payload,
    build_document_layout_prompt,
    build_word_budget_prompt,
    build_chapter_outline_prompt,
    build_subsection_content_prompt,
)

__all__ = [
    "SYSTEM_PROMPT_TEMPLATE_SELECTION",
    "SYSTEM_PROMPT_HTML_GENERATION",
    "SYSTEM_PROMPT_CHAPTER_JSON",
    "SYSTEM_PROMPT_CHAPTER_JSON_REPAIR",
    "SYSTEM_PROMPT_DOCUMENT_LAYOUT",
    "SYSTEM_PROMPT_WORD_BUDGET",
    "SYSTEM_PROMPT_CHAPTER_JSON_RECOVERY",
    "SYSTEM_PROMPT_CHAPTER_OUTLINE",
    "SYSTEM_PROMPT_SUBSECTION_CONTENT",
    "output_schema_template_selection",
    "input_schema_html_generation",
    "chapter_generation_input_schema",
    "build_chapter_user_prompt",
    "build_chapter_repair_prompt",
    "build_chapter_recovery_payload",
    "build_document_layout_prompt",
    "build_word_budget_prompt",
    "build_chapter_outline_prompt",
    "build_subsection_content_prompt",
]
