# md2docx

Convert any Markdown file to a polished `.docx` with TELUS branding — available as an **MCP tool** for Claude Code and Cline (VS Code), and as a standalone CLI.

The only choice you need to make: **cover page or no cover page.**

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

```bash
claude mcp add --scope user md2docx \
  /path/to/md2docx/.venv/bin/python \
  /path/to/md2docx/server.py
```

**Windows example:**
```
claude mcp add --scope user md2docx C:\Users\you\md2docx\.venv\Scripts\python.exe C:\Users\you\md2docx\server.py
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

## Using the MCP Tools

Two tools are available. Both use TELUS branding. The only parameter you need is `cover_page`.

| Tool | When to use |
|------|-------------|
| `convert_markdown_to_docx` | You have Markdown text to convert |
| `convert_md_file_to_docx` | You have a `.md` file already on disk |

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `markdown_text` | string | yes (tool 1) | The Markdown content to convert |
| `input_path` | string | yes (tool 2) | Absolute path to the `.md` file |
| `output_path` | string | yes | Absolute path where the `.docx` will be saved |
| `cover_page` | bool | no | `true` = include TELUS cover page (default), `false` = no cover |

**Example prompts to Claude:**

> Convert this markdown to a docx and save it to `/home/me/docs/report.docx`

> Convert this markdown to a docx without a cover page and save it to `/home/me/docs/report.docx`

> Convert the file `/home/me/notes.md` to docx with a cover page at `/home/me/docs/notes.docx`

---

## CLI Usage

```bash
# With cover page (default)
python md2docx.py input.md output.docx

# Without cover page
python md2docx.py input.md output.docx --no-cover
```

---

## Customising the Style

The TELUS style is defined in `style_telus.json`. To adjust colours, fonts, margins, or the cover title, edit that file directly. All colours are `"#RRGGBB"` hex strings.

The cover title defaults to a placeholder — update `cover.title` in `style_telus.json` per document if needed.

---

## Requirements

Python 3.8+ — install all dependencies with:

```bash
pip install -r requirements.txt
```

Dependencies: `mistune>=3`, `python-docx>=1.1`, `lxml>=4.9`, `mcp>=1.0`
