"""Generate a lesson HTML file from Markdown using the shared Bài 1 template."""

from __future__ import annotations

import argparse
import html
import importlib.util
import pathlib
import re
import sys
from typing import Dict


def get_markdown_converter():
    spec = importlib.util.find_spec("markdown")
    if spec is None:
        return None
    import markdown

    return markdown.Markdown(extensions=["extra", "sane_lists", "smarty"])


def normalize_text(text: str) -> str:
    cleaned = html.unescape(text)
    cleaned = re.sub(r"<[^>]+>", " ", cleaned)
    cleaned = re.sub(r"^[\s>*#`\-+\d\.)]+", "", cleaned)
    cleaned = re.sub(r"[.,:;–—•→()<>]", " ", cleaned)
    cleaned = re.sub(r"[`*_]+", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()


def apply_inline_formatting(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    return text


def fallback_markdown(text: str) -> str:
    html_lines: list[str] = []
    list_stack: list[tuple[str, int]] = []

    def close_lists(target_indent: int = 0) -> None:
        while list_stack and list_stack[-1][1] >= target_indent:
            tag, _ = list_stack.pop()
            html_lines.append(f"</{tag}>")

    for raw_line in text.splitlines():
        if not raw_line.strip():
            close_lists(0)
            continue

        stripped = raw_line.lstrip(" ")
        indent = len(raw_line) - len(stripped)

        if stripped.startswith("#"):
            close_lists(0)
            level = len(stripped) - len(stripped.lstrip("#"))
            content = stripped[level:].strip()
            level = min(level, 6)
            html_lines.append(
                f"<h{level}>{apply_inline_formatting(content)}</h{level}>"
            )
            continue

        if stripped.startswith("---"):
            close_lists(0)
            html_lines.append('<hr class="my-6 border-slate-200" />')
            continue

        bullet_match = re.match(r"[-*]\s+(.*)", stripped)
        ordered_match = re.match(r"(\d+)\.\s+(.*)", stripped)

        if bullet_match or ordered_match:
            tag = "ul" if bullet_match else "ol"
            content = bullet_match.group(1) if bullet_match else ordered_match.group(2)

            while list_stack and indent < list_stack[-1][1]:
                tag_to_close, _ = list_stack.pop()
                html_lines.append(f"</{tag_to_close}>")

            if not list_stack or indent > list_stack[-1][1] or list_stack[-1][0] != tag:
                list_stack.append((tag, indent))
                html_lines.append(f"<{tag}>")

            html_lines.append(f"<li>{apply_inline_formatting(content)}</li>")
            continue

        if list_stack and indent >= list_stack[-1][1]:
            html_lines.append(
                f"<p class=\"ml-6\">{apply_inline_formatting(stripped)}</p>"
            )
            continue

        close_lists(0)
        html_lines.append(f"<p>{apply_inline_formatting(stripped)}</p>")

    close_lists(0)
    return "\n".join(html_lines)


def verify_full_coverage(source_markdown: str, rendered_html: str) -> None:
    plain_html = normalize_text(rendered_html)
    missing: list[str] = []
    for line in source_markdown.splitlines():
        normalized = normalize_text(line)
        if not normalized or normalized == "---":
            continue
        tokens = normalized.split()
        if tokens and not all(token in plain_html for token in tokens):
            missing.append(normalized)
    if missing:
        message = "\n - ".join(["Nội dung thiếu (so với Markdown gốc):"] + missing)
        sys.exit(message)


def derive_initials(name: str) -> str:
    parts = [p for p in name.split() if p]
    if not parts:
        return "?"
    initials = "".join(p[0] for p in parts[:2]).upper()
    return initials


def render_template(template: str, replacements: Dict[str, str]) -> str:
    result = template
    for key, value in replacements.items():
        result = result.replace(f"{{{{{key}}}}}", value)
    return result


def build_html(args: argparse.Namespace) -> str:
    raw_text = pathlib.Path(args.input).read_text(encoding="utf-8")
    md_converter = get_markdown_converter()
    if md_converter is None:
        content_html = fallback_markdown(raw_text)
    else:
        content_html = md_converter.convert(raw_text)

    if not args.skip_coverage_check:
        verify_full_coverage(raw_text, content_html)

    template = pathlib.Path(args.template).read_text(encoding="utf-8")

    replacements = {
        "PAGE_TITLE": args.page_title,
        "COURSE_TAG": args.course_tag,
        "HEADER_LESSON": args.header_lesson,
        "MODULE_BADGE": args.module_badge,
        "HERO_TITLE": args.hero_title,
        "HERO_DECK": args.hero_deck,
        "INSTRUCTOR_INITIALS": derive_initials(args.instructor_name),
        "INSTRUCTOR_NAME": args.instructor_name,
        "INSTRUCTOR_META": args.instructor_meta,
        "CONTENT_HTML": content_html,
        "BACK_LINK": args.back_link,
        "NEXT_LINK": args.next_link,
    }

    html_output = render_template(template, replacements)
    return html_output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sinh HTML bài học từ Markdown")
    parser.add_argument("--input", required=True, help="Đường dẫn file Markdown gốc")
    parser.add_argument("--output", required=True, help="Đường dẫn file HTML muốn xuất")
    parser.add_argument(
        "--template",
        default="templates/lesson_template.html",
        help="Đường dẫn template HTML (mặc định: templates/lesson_template.html)",
    )
    parser.add_argument("--page-title", required=True, help="Tiêu đề thẻ <title>")
    parser.add_argument("--course-tag", required=True, help="Tên khóa học hiển thị trên header")
    parser.add_argument("--header-lesson", required=True, help="Nhãn bài học ở header")
    parser.add_argument("--module-badge", required=True, help="Badge module ở hero")
    parser.add_argument("--hero-title", required=True, help="Tiêu đề chính trên trang")
    parser.add_argument("--hero-deck", default="", help="Mô tả ngắn dưới tiêu đề")
    parser.add_argument("--instructor-name", required=True, help="Tên giảng viên")
    parser.add_argument(
        "--instructor-meta",
        default="",
        help="Dòng mô tả phụ (ngày, khóa học...) dưới tên giảng viên",
    )
    parser.add_argument(
        "--back-link",
        default="Index.html",
        help="Liên kết quay lại danh sách (mặc định Index.html)",
    )
    parser.add_argument(
        "--next-link",
        default="#",
        help="Liên kết sang bài kế tiếp (mặc định #)",
    )
    parser.add_argument(
        "--skip-coverage-check",
        action="store_true",
        help="Bỏ qua bước kiểm tra 100% nội dung (không khuyến khích)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    html_output = build_html(args)
    pathlib.Path(args.output).write_text(html_output, encoding="utf-8")
    print(
        f"✅ Đã tạo {args.output} từ {args.input} bằng template {args.template}"
    )


if __name__ == "__main__":
    main()
