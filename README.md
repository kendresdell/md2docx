# md2docx

Convert any Markdown file to a polished `.docx` — available as an **MCP tool** for Claude Code and Cline (VS Code), and as a standalone CLI.

Default style is **TELUS branding** (purple/green, Poppins body, Roboto Slab H1, cover page with logo). A no-cover variant is also included.

---

## MCP Setup (Claude Code & Cline)

### Step 1 — Clone and install

```bash
git clone https://github.com/kendresdell/md2docx.git
cd md2docx
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

Note the full path to your `.venv` Python — you'll need it in the next steps.

```bash
# macOS / Linux
which python    # e.g. /home/you/md2docx/.venv/bin/python

# Windows (PowerShell)
where.exe python   # e.g. C:\Users\you\md2docx\.venv\Scripts\python.exe
```

---

### Step 2 — Claude Code

Run this command (replace paths with your actual clone location):

```bash
claude mcp add --scope user md2docx \
  /path/to/md2docx/.venv/bin/python \
  /path/to/md2docx/server.py
```

**Windows example:**
```bash
claude mcp add --scope user md2docx ^
  C:\Users\you\md2docx\.venv\Scripts\python.exe ^
  C:\Users\you\md2docx\server.py
```

Restart Claude Code. Verify with `/mcp` — you should see **md2docx** listed.

---

### Step 3 — Cline (VS Code)

Open the Cline panel → **MCP Servers** → **Edit MCP Settings**, and add:

```json
{
  "md2docx": {
    "command": "/path/to/md2docx/.venv/bin/python",
    "args": ["/path/to/md2docx/server.py"],
    "disabled": false,
    "autoApprove": []
  }
}
```

**Windows example:**
```json
{
  "md2docx": {
    "command": "C:\\Users\\you\\md2docx\\.venv\\Scripts\\python.exe",
    "args": ["C:\\Users\\you\\md2docx\\server.py"],
    "disabled": false,
    "autoApprove": []
  }
}
```

Save and restart VS Code. The **md2docx** server will appear in Cline's MCP panel.

---

## Available MCP Tools

| Tool | Input | Description |
|------|-------|-------------|
| `convert_markdown_to_docx` | `markdown_text`, `output_path`, `style_path`* | Convert Markdown text to DOCX |
| `convert_md_file_to_docx` | `input_path`, `output_path`, `style_path`* | Convert a `.md` file on disk to DOCX |

`*` optional — defaults to `style_telus.json` (TELUS branding with cover page)

**Example prompt to Claude:**
> Convert this markdown to a docx and save it to `/home/me/docs/report.docx`

> Convert this markdown to a docx using style_telus_no_cover.json and save it to `/home/me/docs/report.docx`

---

## CLI Usage

```bash
# Default style (style_telus.json — TELUS branding, with cover page)
python md2docx.py input.md output.docx

# No cover page
python md2docx.py input.md output.docx --style style_telus_no_cover.json

# Custom style
python md2docx.py input.md output.docx --style style_default.json
```

```
positional arguments:
  input          Input Markdown file (.md)
  output         Output Word document (.docx)

optional arguments:
  --style FILE, -s FILE
                 JSON style guide (default: style_telus.json)
```

---

## Style Guides

| File | Description |
|------|-------------|
| `style_telus.json` | TELUS branding — purple/green, Poppins + Roboto Slab, **with cover page** |
| `style_telus_no_cover.json` | Same TELUS branding, **no cover page** |
| `style_default.json` | Minimal style — Poppins body, no cover, no footer |
| `style_personal.json` | Dark personal style — cover enabled, black background |

Copy any style file, rename it, and edit to create your own. All colours are `"#RRGGBB"` hex strings.

### Style Guide Reference

#### `document`

| Key | Type | Description |
|-----|------|-------------|
| `page_size` | string | `"letter"` or `"A4"` |
| `line_spacing` | float | Line spacing multiplier (e.g. `1.15`) |
| `margins.top_cm` | float | Top margin in centimetres |
| `margins.bottom_cm` | float | Bottom margin in centimetres |
| `margins.left_cm` | float | Left margin in centimetres |
| `margins.right_cm` | float | Right margin in centimetres |

#### `fonts`

| Key | Description |
|-----|-------------|
| `body` | Font for body text, H2–H4, lists, tables |
| `h1_override` | Font for H1 only (`""` to use `body`) |
| `cover_title` | Font for the cover page title |
| `footer` | Font for the footer |

#### `headings` — one entry per level: `h1`, `h2`, `h3`, `h4`

| Key | Type | Description |
|-----|------|-------------|
| `size` | int | Font size in points |
| `color` | string | Text color (`"#RRGGBB"`) |
| `bold` | bool | Bold weight |
| `italic` | bool | Italic style |

#### `body` / `blockquote` / `code_inline` / `code_block`

| Key | Description |
|-----|-------------|
| `size` | Font size in points |
| `color` | Text color |
| `border_color` | (`blockquote` only) Left border color |
| `bg_color` | (`blockquote` only) Background color |

#### `table`

| Key | Description |
|-----|-------------|
| `header_bg` | Header row background color |
| `header_text` | Header row text color |
| `body_text` | Body row text color |
| `header_size` | Header font size in points |
| `body_size` | Body font size in points |

#### `cover`

| Key | Type | Description |
|-----|------|-------------|
| `enabled` | bool | `true` to render a cover page, `false` to skip |
| `bg_color` | string | Cover background color |
| `logo_path` | string | Path to logo image (relative to the style JSON file, or absolute) |
| `logo_width_cm` | float | Logo width in centimetres |
| `title` | string | Cover page title text |
| `title_size` | int | Cover title font size in points |
| `title_color` | string | Cover title text color |
| `top_spacer_pt` | float | Vertical space above logo in points |

Logo is silently skipped if the file does not exist — no error is raised.

#### `footer`

| Key | Description |
|-----|-------------|
| `label` | Footer text (appears on every page) |
| `size` | Footer font size in points |
| `color` | Footer text color |

Note: page numbers are always rendered in the footer regardless of whether a `footer` key is present.

---

## Requirements

Python 3.8+ — install all dependencies with:

```bash
pip install -r requirements.txt
```

Dependencies: `mistune>=3`, `python-docx>=1.1`, `lxml>=4.9`, `mcp>=1.0`
