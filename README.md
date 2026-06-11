# md2docx

Convert any Markdown file to a polished `.docx` with TELUS branding — usable as an **MCP server** inside OpenCode, Claude Code, or Cline, and as a **standalone CLI**.

**The only decision you ever make: cover page or no cover page.**  
Everything else — TELUS colours, logo, fonts, footer — is applied automatically.

---

## What it produces

- Purple TELUS cover page with the official logo and the document title (taken from the filename automatically)
- `Confidential — TELUS` footer on every page
- TELUS brand colours, Poppins body font, Roboto Slab headings
- Full Markdown support: headings, lists, tables, code blocks, blockquotes

---

## Step 1 — Clone and install

```bash
git clone https://github.com/kendresdell/md2docx.git
cd md2docx
```

Create a virtual environment and install dependencies:

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Note the full path to your venv Python — you'll need it for the MCP config:

```bash
# macOS / Linux — copy this output
which python
# e.g.  /home/you/md2docx/.venv/bin/python

# Windows (PowerShell) — copy this output
where.exe python
# e.g.  C:\Users\you\md2docx\.venv\Scripts\python.exe
```

---

## Step 2 — Set up as an MCP server

Pick the tool you use.

---

### OpenCode

Edit (or create) your global OpenCode config file:

- **macOS / Linux**: `~/.config/opencode/opencode.json`
- **Windows**: `C:\Users\<you>\.config\opencode\opencode.json`

Add the `md2docx` entry inside the `"mcp"` block:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "md2docx": {
      "type": "local",
      "command": [
        "/path/to/md2docx/.venv/bin/python",
        "/path/to/md2docx/server.py"
      ],
      "enabled": true
    }
  }
}
```

**Windows example** (use double backslashes):
```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "md2docx": {
      "type": "local",
      "command": [
        "C:\\Users\\you\\md2docx\\.venv\\Scripts\\python.exe",
        "C:\\Users\\you\\md2docx\\server.py"
      ],
      "enabled": true
    }
  }
}
```

Restart OpenCode. The `md2docx` tools will be available immediately.

> **Note:** If you already have an `opencode.json` with other settings, just add the `"mcp"` block — don't replace the whole file.

---

### Claude Code

```bash
claude mcp add --scope user md2docx \
  /path/to/md2docx/.venv/bin/python \
  /path/to/md2docx/server.py
```

**Windows (run as a single line):**
```
claude mcp add --scope user md2docx C:\Users\you\md2docx\.venv\Scripts\python.exe C:\Users\you\md2docx\server.py
```

Restart Claude Code and verify with `/mcp` — you should see **md2docx** listed.

---

### Cline (VS Code)

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

Save and restart VS Code.

---

## Using the tools

Once installed, just ask the AI naturally:

> "Convert this markdown to a docx and save it to `/Users/me/docs/report.docx`"

> "Convert this markdown to a docx without a cover page and save it to `/Users/me/docs/report.docx`"

> "Convert the file `/Users/me/notes.md` to docx and save it to `/Users/me/docs/notes.docx`"

The cover title is set automatically from the output filename — `report.docx` becomes **"Report"** on the cover page.

### Available tools

| Tool | Use when |
|------|----------|
| `convert_markdown_to_docx` | You have Markdown text to convert |
| `convert_md_file_to_docx` | You have a `.md` file already on disk |

| Parameter | Type | Description |
|-----------|------|-------------|
| `markdown_text` | string | The Markdown content (`convert_markdown_to_docx` only) |
| `input_path` | string | Absolute path to the `.md` file (`convert_md_file_to_docx` only) |
| `output_path` | string | Absolute path where the `.docx` will be saved |
| `cover_page` | bool | `true` = TELUS cover page (default), `false` = no cover |

---

## CLI usage

If you prefer the command line:

```bash
# With cover page (default)
python md2docx.py report.md report.docx

# Without cover page
python md2docx.py report.md report.docx --no-cover
```

---

## Customising the style

All TELUS branding lives in `style_telus.json`. To adjust colours, margins, font sizes, or the footer text, edit that file directly. All colours use `"#RRGGBB"` hex format.

To create a team variant (e.g. for a specific squad), copy `style_telus.json`, rename it, and pass it via the hidden `--style` flag in the CLI.

---

## Requirements

- Python 3.8+
- Dependencies (installed via `pip install -r requirements.txt`): `mistune>=3`, `python-docx>=1.1`, `lxml>=4.9`, `mcp>=1.0`
- The fonts **Poppins** and **Roboto Slab** should be installed on the machine opening the `.docx` for best results. Word will substitute if they are missing.
