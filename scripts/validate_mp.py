#!/usr/bin/env python3
"""
WeChat Official Account HTML Validator

Validates an HTML file for WeChat Official Account compatibility.
Checks for: external resources, JavaScript, unsupported tags,
inline style compliance, image URL requirements, SVG constraints,
and article size limits.

Usage:
    python validate_mp.py <article.html> [--strict] [--json]

Options:
    --strict    Enable strict mode (warnings become errors)
    --json      Output results as JSON
"""

import re
import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Issue:
    severity: str  # "error" or "warning"
    category: str
    message: str
    line: Optional[int] = None
    snippet: Optional[str] = None


@dataclass
class ValidationResult:
    file_path: str
    issues: List[Issue] = field(default_factory=list)

    @property
    def errors(self) -> List[Issue]:
        return [i for i in self.issues if i.severity == "error"]

    @property
    def warnings(self) -> List[Issue]:
        return [i for i in self.issues if i.severity == "warning"]

    @property
    def passed(self) -> bool:
        return len(self.errors) == 0


# Tags known to be unreliable or blocked in WeChat
BLOCKED_TAGS = [
    "iframe", "script", "link", "form", "input", "button",
    "audio", "canvas", "object", "embed", "video",
    "select", "option", "textarea", "fieldset", "legend",
    "datalist", "output", "progress", "meter", "details",
    "summary", "dialog", "menu", "menuitem",
]

# Deprecated tags that should not be used
DEPRECATED_TAGS = [
    "font", "center", "marquee", "blink", "big", "strike",
    "tt", "frame", "frameset", "noframes",
]

# Supported HTML tags in WeChat
SUPPORTED_TAGS = {
    "div", "section", "p", "h1", "h2", "h3", "h4", "h5", "h6",
    "blockquote", "ul", "ol", "li", "table", "thead", "tbody",
    "tr", "th", "td", "hr", "br", "pre", "code",
    "span", "a", "strong", "b", "em", "i", "u", "del",
    "sub", "sup", "img", "svg", "g", "path", "circle",
    "rect", "ellipse", "line", "polyline", "polygon",
    "text", "tspan", "textPath", "image", "defs", "use",
    "clipPath", "mask", "filter", "linearGradient",
    "radialGradient", "stop", "pattern", "marker",
    "animate", "animateTransform", "animateMotion", "set",
    "feGaussianBlur", "feOffset", "feMerge", "feMergeNode",
    "feColorMatrix", "feFlood", "feComposite", "feDropShadow",
    "foreignObject",  # included for detection but will warn
}

# Font families that are safe for WeChat (system fonts)
SAFE_FONT_FAMILIES = [
    "pingfang sc", "pingfang", "microsoft yahei", "微软雅黑",
    "simsun", "宋体", "stheiti", "华文黑体", "hiragino sans gb",
    "helvetica neue", "helvetica", "arial",
    "segoe ui", "system-ui", "-apple-system", "blinkmacsystemfont",
    "sans-serif", "serif", "monospace", "cursive", "fantasy",
    "noto serif cjk sc", "source han serif sc", "songti sc",
    "stsong", "stkaiti", "kaiti sc", "kaiti",
]

# Event handler attributes to detect (JavaScript injection)
EVENT_HANDLERS = [
    "onclick", "ondblclick", "onmousedown", "onmouseup",
    "onmouseover", "onmouseout", "onmousemove",
    "onkeydown", "onkeyup", "onkeypress",
    "onload", "onunload", "onerror", "onresize",
    "onscroll", "onfocus", "onblur", "onchange",
    "onsubmit", "onreset", "onselect", "oninput",
    "ontouchstart", "ontouchend", "ontouchmove",
    "onanimationstart", "onanimationend",
    "ontransitionend", "onwheel",
]


class WeChatValidator:
    def __init__(self, file_path: str, strict: bool = False):
        self.file_path = file_path
        self.strict = strict
        self.result = ValidationResult(file_path=file_path)
        self.html = ""
        self.lines: List[str] = []

    def validate(self) -> ValidationResult:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.html = f.read()
        except FileNotFoundError:
            self.result.issues.append(Issue("error", "file", f"File not found: {self.file_path}"))
            return self.result
        except Exception as e:
            self.result.issues.append(Issue("error", "file", f"Error reading file: {e}"))
            return self.result

        self.lines = self.html.split("\n")

        self._check_external_resources()
        self._check_javascript()
        self._check_event_handlers()
        self._check_style_blocks()
        self._check_image_urls()
        self._check_fonts()
        self._check_blocked_tags()
        self._check_deprecated_tags()
        self._check_foreign_object()
        self._check_svg_structure()
        self._check_article_size()
        self._check_doctype()

        return self.result

    def _find_line(self, pattern: str, text: Optional[str] = None) -> Optional[int]:
        """Find line number containing a pattern."""
        search_text = text or self.html
        for i, line in enumerate(self.lines, 1):
            if pattern in line:
                return i
        return None

    def _check_external_resources(self):
        """Check for external CSS/JS/font references."""
        # <link> tags
        link_matches = re.finditer(r'<link\b[^>]*>', self.html, re.IGNORECASE)
        for match in link_matches:
            tag = match.group()
            line = self._find_line(tag)
            self.result.issues.append(Issue(
                "error", "external-resource",
                "External <link> tag detected. WeChat does not support external stylesheets.",
                line=line, snippet=tag[:120]
            ))

        # External script src
        script_src = re.finditer(r'<script\b[^>]*src\s*=\s*["\'][^"\']+["\'][^>]*>', self.html, re.IGNORECASE)
        for match in script_src:
            tag = match.group()
            line = self._find_line(tag)
            self.result.issues.append(Issue(
                "error", "external-resource",
                "External <script> tag detected. WeChat blocks all JavaScript.",
                line=line, snippet=tag[:120]
            ))

        # @import in style blocks
        import_matches = re.finditer(r'@import\s+url\(', self.html, re.IGNORECASE)
        for match in import_matches:
            line = self._find_line(match.group())
            self.result.issues.append(Issue(
                "error", "external-resource",
                "@import detected. External font/CSS imports are not supported.",
                line=line, snippet=match.group()[:80]
            ))

        # External font references (URL-based)
        font_urls = re.finditer(r'url\(["\']?https?://[^)]+(?:\.woff2?|\.ttf|\.otf|\.eot)', self.html, re.IGNORECASE)
        for match in font_urls:
            line = self._find_line(match.group())
            self.result.issues.append(Issue(
                "error", "external-resource",
                "External font file reference detected. Only system fonts are supported.",
                line=line, snippet=match.group()[:80]
            ))

    def _check_javascript(self):
        """Check for JavaScript code."""
        # <script> tags (any)
        script_tags = re.finditer(r'<script\b[^>]*>.*?</script>', self.html, re.IGNORECASE | re.DOTALL)
        for match in script_tags:
            tag = match.group()
            line = self._find_line(tag[:50])
            self.result.issues.append(Issue(
                "error", "javascript",
                "<script> tag detected. JavaScript is completely blocked in WeChat.",
                line=line, snippet=tag[:120]
            ))

        # javascript: URLs
        js_urls = re.finditer(r'(?:href|src|action)\s*=\s*["\']\s*javascript:', self.html, re.IGNORECASE)
        for match in js_urls:
            line = self._find_line(match.group())
            self.result.issues.append(Issue(
                "error", "javascript",
                "javascript: URL detected. JavaScript execution is blocked.",
                line=line, snippet=match.group()[:80]
            ))

    def _check_event_handlers(self):
        """Check for JavaScript event handler attributes."""
        for handler in EVENT_HANDLERS:
            pattern = rf'\b{handler}\s*='
            matches = re.finditer(pattern, self.html, re.IGNORECASE)
            for match in matches:
                line = self._find_line(match.group())
                self.result.issues.append(Issue(
                    "error", "javascript",
                    f"Event handler '{handler}' detected. JavaScript events are blocked.",
                    line=line, snippet=match.group()[:80]
                ))

    def _check_style_blocks(self):
        """Check for <style> blocks outside SVG."""
        style_blocks = re.finditer(r'<style\b[^>]*>(.*?)</style>', self.html, re.IGNORECASE | re.DOTALL)
        for match in style_blocks:
            full_tag = match.group()
            # <style> inside SVG is acceptable
            before = self.html[:match.start()]
            last_svg_open = before.rfind("<svg")
            last_svg_close = before.rfind("</svg>")

            if last_svg_open > last_svg_close:
                continue  # Inside SVG — allowed

            line = self._find_line(full_tag[:50])
            severity = "warning" if not self.strict else "error"
            self.result.issues.append(Issue(
                severity, "style",
                "<style> block detected outside SVG. May be stripped by WeChat. Use inline styles.",
                line=line, snippet=full_tag[:120]
            ))

    def _check_image_urls(self):
        """Check image sources are absolute URLs."""
        img_tags = re.finditer(r'<img\b[^>]*>', self.html, re.IGNORECASE)
        for match in img_tags:
            tag = match.group()
            src_match = re.search(r'src\s*=\s*["\']([^"\']+)["\']', tag, re.IGNORECASE)
            if not src_match:
                line = self._find_line(tag)
                self.result.issues.append(Issue(
                    "error", "image",
                    "<img> tag without src attribute.",
                    line=line, snippet=tag[:120]
                ))
                continue

            src = src_match.group(1)

            # Check for local paths
            if src.startswith("./") or src.startswith("../") or src.startswith("/") or src.startswith("file://"):
                line = self._find_line(tag)
                self.result.issues.append(Issue(
                    "error", "image",
                    f"Local image path detected: '{src[:60]}'. Images must use absolute HTTPS URLs.",
                    line=line, snippet=tag[:120]
                ))
                continue

            if not src.startswith("http://") and not src.startswith("https://"):
                line = self._find_line(tag)
                self.result.issues.append(Issue(
                    "error", "image",
                    f"Invalid image URL: '{src[:60]}'. Must be absolute HTTP/HTTPS URL.",
                    line=line, snippet=tag[:120]
                ))

            # Check for base64 images
            if src.startswith("data:image"):
                import base64
                try:
                    data_part = src.split(",", 1)[1] if "," in src else ""
                    decoded = base64.b64decode(data_part, validate=True)
                    size_kb = len(decoded) / 1024
                except Exception:
                    size_kb = len(src) * 0.75 / 1024  # rough estimate

                if size_kb > 32:
                    line = self._find_line(tag)
                    self.result.issues.append(Issue(
                        "error" if size_kb > 100 else "warning",
                        "image",
                        f"Base64 image is {size_kb:.0f}KB. WeChat limits base64 images to ~32KB. Use hosted URL instead.",
                        line=line, snippet=src[:80]
                    ))

            # Check for SVG <image> tags
            svg_images = re.finditer(r'<image\b[^>]*href\s*=\s*["\']([^"\']+)["\']', self.html, re.IGNORECASE)
            for svg_match in svg_images:
                href = svg_match.group(1)
                if href.startswith("data:image"):
                    line = self._find_line(svg_match.group())
                    self.result.issues.append(Issue(
                        "warning", "image",
                        "Base64 image in SVG <image> tag. May increase article size significantly.",
                        line=line, snippet=href[:80]
                    ))

    def _check_fonts(self):
        """Check font-family declarations use safe system fonts."""
        font_declarations = re.finditer(
            r'font-family\s*:\s*([^;}"\']+)',
            self.html, re.IGNORECASE
        )
        for match in font_declarations:
            fonts_str = match.group(1).strip().strip('"\'')
            fonts = [f.strip().strip('"\'') for f in fonts_str.split(",")]

            unsafe_fonts = []
            for font in fonts:
                font_lower = font.lower()
                is_safe = False
                for safe in SAFE_FONT_FAMILIES:
                    if safe in font_lower or font_lower in safe:
                        is_safe = True
                        break
                if not is_safe:
                    unsafe_fonts.append(font)

            if unsafe_fonts and all(f.lower() not in ["inherit", "initial", "unset"] for f in unsafe_fonts):
                line = self._find_line(fonts_str)
                self.result.issues.append(Issue(
                    "warning",
                    "font",
                    f"Potentially unsupported font(s): {', '.join(unsafe_fonts[:3])}. "
                    "WeChat only supports system fonts. Non-system fonts will fallback to default.",
                    line=line
                ))

    def _check_blocked_tags(self):
        """Check for tags known to be blocked in WeChat."""
        for tag in BLOCKED_TAGS:
            pattern = rf'<{tag}\b'
            matches = re.finditer(pattern, self.html, re.IGNORECASE)
            for match in matches:
                line = self._find_line(match.group())
                self.result.issues.append(Issue(
                    "error", "blocked-tag",
                    f"<{tag}> tag detected. This tag is blocked or unreliable in WeChat.",
                    line=line
                ))

    def _check_deprecated_tags(self):
        """Check for deprecated HTML tags."""
        for tag in DEPRECATED_TAGS:
            pattern = rf'<{tag}\b'
            matches = re.finditer(pattern, self.html, re.IGNORECASE)
            for match in matches:
                line = self._find_line(match.group())
                self.result.issues.append(Issue(
                    "warning" if not self.strict else "error",
                    "deprecated-tag",
                    f"<{tag}> tag is deprecated. Replace with semantic HTML + inline styles.",
                    line=line
                ))

    def _check_foreign_object(self):
        """Warn about foreignObject usage in SVG."""
        fo_matches = re.finditer(r'<foreignObject\b', self.html, re.IGNORECASE)
        for match in fo_matches:
            line = self._find_line(match.group())
            self.result.issues.append(Issue(
                "warning" if not self.strict else "error",
                "svg",
                "<foreignObject> detected. Unreliable in WeChat SVG renderer. Consider alternatives.",
                line=line
            ))

    def _check_svg_structure(self):
        """Check SVG elements for WeChat compatibility."""
        # Check for <use> tags (sometimes stripped)
        use_tags = re.finditer(r'<use\b[^>]*>', self.html, re.IGNORECASE)
        for match in use_tags:
            line = self._find_line(match.group())
            self.result.issues.append(Issue(
                "warning", "svg",
                "<use> tag detected. May be stripped in some WeChat versions. Prefer duplicating elements.",
                line=line, snippet=match.group()[:80]
            ))

        # Check for JavaScript in SVG
        svg_scripts = re.finditer(r'<svg\b[^>]*>.*?<script\b.*?</svg>', self.html, re.IGNORECASE | re.DOTALL)
        for match in svg_scripts:
            line = self._find_line(match.group()[:100])
            self.result.issues.append(Issue(
                "error", "svg",
                "<script> inside SVG detected. JavaScript is blocked even within SVG.",
                line=line
            ))

        # Check for href (use xlink:href for maximum WeChat compatibility)
        href_attrs = re.finditer(r'<a\b[^>]*\bhref\s*=', self.html, re.IGNORECASE)
        xlink_attrs = re.finditer(r'<a\b[^>]*\bxlink:href\s*=', self.html, re.IGNORECASE)

        href_count = sum(1 for _ in href_attrs)
        xlink_count = sum(1 for _ in xlink_attrs)

    def _check_article_size(self):
        """Check article size is within limits."""
        size_kb = len(self.html.encode("utf-8")) / 1024

        if size_kb > 2000:
            self.result.issues.append(Issue(
                "error",
                "size",
                f"Article HTML size is {size_kb:.0f}KB. WeChat limit is ~2MB. "
                "Consider reducing content or using image-based layout for long articles.",
            ))
        elif size_kb > 1000:
            self.result.issues.append(Issue(
                "warning",
                "size",
                f"Article HTML size is {size_kb:.0f}KB. Approaching WeChat limits. "
                "Test upload before publishing.",
            ))

        # Check SVG markup size
        svg_sizes = []
        for svg_match in re.finditer(r'<svg\b.*?</svg>', self.html, re.IGNORECASE | re.DOTALL):
            svg_kb = len(svg_match.group().encode("utf-8")) / 1024
            if svg_kb > 200:
                svg_sizes.append(svg_kb)

        if svg_sizes:
            for i, size in enumerate(svg_sizes, 1):
                self.result.issues.append(Issue(
                    "warning",
                    "size",
                    f"SVG #{i} is {size:.0f}KB. Large SVGs may be truncated. Keep under 200KB.",
                ))

    def _check_doctype(self):
        """Check for unnecessary DOCTYPE declarations."""
        if "<!DOCTYPE" in self.html.upper():
            self.result.issues.append(Issue(
                "warning",
                "structure",
                "DOCTYPE declaration detected. WeChat articles do not need DOCTYPE. "
                "Remove for cleaner output.",
            ))


def format_result(result: ValidationResult, strict: bool = False) -> str:
    """Format validation results as human-readable text."""
    lines = []
    lines.append("=" * 60)
    lines.append(f"WeChat Article Validator")
    lines.append(f"File: {result.file_path}")
    lines.append(f"Mode: {'Strict' if strict else 'Standard'}")
    lines.append("=" * 60)

    if not result.issues:
        lines.append("\n✅ All checks passed! Article is WeChat-compatible.")
        return "\n".join(lines)

    errors = result.errors
    warnings = result.warnings

    lines.append(f"\n📊 Summary: {len(errors)} error(s), {len(warnings)} warning(s)")

    if errors:
        lines.append("\n❌ ERRORS (must fix):")
        lines.append("-" * 40)
        for i, issue in enumerate(errors, 1):
            loc = f" (line {issue.line})" if issue.line else ""
            lines.append(f"  [{issue.category}]{loc} {issue.message}")

    if warnings:
        lines.append(f"\n⚠️  WARNINGS:")
        lines.append("-" * 40)
        for i, issue in enumerate(warnings, 1):
            loc = f" (line {issue.line})" if issue.line else ""
            lines.append(f"  [{issue.category}]{loc} {issue.message}")

    if errors:
        lines.append(f"\n❌ Validation FAILED — {len(errors)} error(s) to fix.")
    else:
        lines.append(f"\n✅ Validation PASSED — {len(warnings)} warning(s) to review.")

    return "\n".join(lines)


def format_json(result: ValidationResult) -> str:
    """Format validation results as JSON."""
    return json.dumps({
        "file": result.file_path,
        "passed": result.passed,
        "error_count": len(result.errors),
        "warning_count": len(result.warnings),
        "issues": [
            {
                "severity": i.severity,
                "category": i.category,
                "message": i.message,
                "line": i.line,
                "snippet": i.snippet,
            }
            for i in result.issues
        ]
    }, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Validate HTML for WeChat Official Account compatibility"
    )
    parser.add_argument("file", help="Path to HTML file to validate")
    parser.add_argument("--strict", action="store_true",
                        help="Treat warnings as errors")
    parser.add_argument("--json", action="store_true",
                        help="Output results as JSON")
    args = parser.parse_args()

    validator = WeChatValidator(args.file, strict=args.strict)
    result = validator.validate()

    if args.json:
        print(format_json(result))
    else:
        print(format_result(result, args.strict))

    sys.exit(0 if result.passed else 1)


if __name__ == "__main__":
    main()
