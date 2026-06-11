#!/usr/bin/env python3
"""
MCP server for md2docx — TELUS branding.

Exposes two tools:
  - convert_markdown_to_docx  : convert Markdown text → DOCX
  - convert_md_file_to_docx   : convert a .md file on disk → DOCX

Both tools use TELUS branding by default. Pass cover_page=False to omit the cover page.

Run via stdio (default) — compatible with Claude Code and Cline.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("md2docx")

_SCRIPT          = str(Path(__file__).parent / "md2docx.py")
_STYLE_COVER     = str(Path(__file__).parent / "style_telus.json")
_STYLE_NO_COVER  = str(Path(__file__).parent / "style_telus_no_cover.json")


@mcp.tool()
def convert_markdown_to_docx(
    markdown_text: str,
    output_path: str,
    cover_page: bool = True,
) -> str:
    """Convert Markdown text to a DOCX file using TELUS branding.

    Args:
        markdown_text: Markdown content to convert.
        output_path: Absolute path where the .docx file will be saved.
        cover_page: Include a TELUS cover page. Defaults to True. Pass False to omit it.

    Returns:
        Confirmation message with the saved file path.
    """
    style = _STYLE_COVER if cover_page else _STYLE_NO_COVER
    title = Path(output_path).stem.replace('_', ' ').replace('-', ' ')
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", encoding="utf-8", delete=False
    )
    try:
        tmp.write(markdown_text)
        tmp.close()
        result = subprocess.run(
            [sys.executable, _SCRIPT, tmp.name, output_path, "--style", style, "--title", title],
            capture_output=True,
            text=True,
            stdin=subprocess.DEVNULL,
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr or result.stdout)
        return f"Saved → {output_path}"
    finally:
        Path(tmp.name).unlink(missing_ok=True)


@mcp.tool()
def convert_md_file_to_docx(
    input_path: str,
    output_path: str,
    cover_page: bool = True,
) -> str:
    """Convert a Markdown file on disk to a DOCX file using TELUS branding.

    Args:
        input_path: Absolute path to the input .md file.
        output_path: Absolute path where the .docx file will be saved.
        cover_page: Include a TELUS cover page. Defaults to True. Pass False to omit it.

    Returns:
        Confirmation message with the saved file path.
    """
    style = _STYLE_COVER if cover_page else _STYLE_NO_COVER
    title = Path(output_path).stem.replace('_', ' ').replace('-', ' ')
    result = subprocess.run(
        [sys.executable, _SCRIPT, input_path, output_path, "--style", style, "--title", title],
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout)
    return f"Saved → {output_path}"


if __name__ == "__main__":
    mcp.run()
