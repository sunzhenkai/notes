#!/usr/bin/env python3
"""
修复 markdown 文件的 header 格式
将 categories/tags 中的行内数组格式 [a, b, c] 展开为多行格式

使用方法:
  python fix_markdown_header.py --preview    # 预览模式，只显示会修改的内容
  python fix_markdown_header.py --execute    # 执行模式，实际修改文件
"""

import os
import re
import glob
import argparse
from pathlib import Path
from typing import Tuple, List


def expand_inline_array(line: str) -> Tuple[str, bool]:
    """
    将行内数组格式展开为多行格式
    例如: "  - [a, b, c]" -> "  - a\n  - b\n  - c"

    返回: (处理后的内容, 是否被修改)
    """
    # 匹配类似 "- [a, b, c]" 的格式
    match = re.match(r"^(\s*)-\s*\[(.+?)\]\s*$", line)
    if not match:
        return line, False

    indent = match.group(1)
    items_str = match.group(2)

    # 分割数组元素，处理逗号分隔（包括带空格的情况）
    items = [item.strip() for item in items_str.split(",")]

    # 展开为多行
    expanded_lines = [f"{indent}- {item}" for item in items if item]

    return "\n".join(expanded_lines), True


def process_frontmatter(
    content: str, preview_mode: bool = False
) -> Tuple[str, List[str], bool]:
    """
    处理 markdown 文件的 frontmatter (YAML header)

    返回: (处理后的内容, 修改说明列表, 是否有修改)
    """
    lines = content.split("\n")
    result_lines = []
    changes = []
    has_changes = False

    in_frontmatter = False
    frontmatter_end = False
    current_key = None  # 当前处理的 key (categories/tags)

    for i, line in enumerate(lines):
        # 检测 frontmatter 开始
        if line.strip() == "---":
            if not in_frontmatter:
                in_frontmatter = True
                result_lines.append(line)
                continue
            else:
                # frontmatter 结束
                in_frontmatter = False
                frontmatter_end = True
                result_lines.append(line)
                continue

        if in_frontmatter:
            # 检测 key (如 categories:, tags:)
            if ":" in line and not line.startswith(" "):
                current_key = line.split(":")[0].strip()

            # 在 frontmatter 中，检查是否需要展开
            expanded, was_modified = expand_inline_array(line)

            if was_modified:
                has_changes = True
                if preview_mode:
                    changes.append(f"  行 {i + 1}: {line.strip()}")
                    changes.append(f"  修改为:")
                    for expanded_line in expanded.split("\n"):
                        changes.append(f"         {expanded_line}")
                    changes.append("")

            result_lines.append(expanded)
        else:
            # 不在 frontmatter 中，保持原样
            result_lines.append(line)

    return "\n".join(result_lines), changes, has_changes


def process_file(filepath: str, preview_mode: bool = False) -> Tuple[bool, List[str]]:
    """
    处理单个 markdown 文件

    返回: (是否被修改, 修改说明列表)
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # 处理 frontmatter
        new_content, changes, has_changes = process_frontmatter(content, preview_mode)

        # 如果内容有变化且不是预览模式，写回文件
        if has_changes and not preview_mode:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)

        return has_changes, changes
    except Exception as e:
        return False, [f"处理文件时出错: {e}"]


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="修复 markdown 文件的 header 格式，将行内数组展开为多行格式"
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="预览模式：只显示会修改的内容，不实际修改文件",
    )
    parser.add_argument("--execute", action="store_true", help="执行模式：实际修改文件")

    args = parser.parse_args()

    # 默认是预览模式
    if not args.execute and not args.preview:
        args.preview = True

    # 获取当前目录
    current_dir = Path(__file__).parent

    # 查找所有 markdown 文件
    md_files = list(current_dir.rglob("*.md"))

    # 排除脚本自身可能生成的文件
    md_files = [f for f in md_files if "node_modules" not in str(f)]

    print(f"找到 {len(md_files)} 个 markdown 文件")

    if args.preview:
        print("🔍 预览模式 - 以下是将要进行的修改:\n")
    else:
        print("⚠️  执行模式 - 正在修改文件...\n")

    modified_count = 0

    for filepath in md_files:
        was_modified, changes = process_file(str(filepath), args.preview)

        if was_modified:
            rel_path = filepath.relative_to(current_dir)
            if args.preview:
                print(f"📝 {rel_path}")
                for change in changes:
                    print(change)
            else:
                print(f"✓ 已处理: {rel_path}")
            modified_count += 1

    if args.preview:
        print(f"\n📊 预览完成！共发现 {modified_count} 个文件需要修改")
        print("\n要执行修改，请运行: python fix_markdown_header.py --execute")
    else:
        print(f"\n✅ 完成！共修改了 {modified_count} 个文件")


if __name__ == "__main__":
    main()
