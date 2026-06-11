# AGENTS.md

## Repo at a Glance

Single-purpose Python tool: converts Markdown to `.docx` with TELUS branding. Two entry points:
- `md2docx.py` — CLI
- `server.py` — MCP server (used by Claude Code, Cline, OpenCode, etc.)

No tests, no CI, no build system. Everything lives in the root.

---

## Commands

```bash
# Install
pip install -r requirements.txt   # mistune>=3, python-docx>=1.1, lxml>=4.9, mcp>=1.0

# CLI — with cover page (default)
python md2docx.py input.md output.docx

# CLI — no cover page
python md2docx.py input.md output.docx --no-cover
```

Verify changes by doing a real conversion and opening the `.docx` — there are no tests.

---

## Key Behaviours

- **CLI default**: `style_telus.json`, cover page on, title derived from input filename stem.
- **Server default**: same — `style_telus.json`, cover on, title derived from output filename stem.
- **Cover title**: auto-set to the filename stem (underscores/hyphens → spaces). Overridable via hidden `--title` flag.
- **Cover page IS rendered** when `COVER_ENABLED=True`; `render_cover_page()` called at line 768.
- **Footer is always rendered**: `_add_page_numbers()` is called unconditionally in `setup_document()` (line 738). The `footer` key only controls label text and size, not whether footer runs.
- **Logo**: `Telus_logo.png` in the repo root. Silently skipped if missing (line 357: `COVER_LOGO_PATH.exists()`).
- **Fonts**: Poppins (body), Roboto Slab (H1) — across all styles.
- **`--style` flag** exists but is hidden from `--help` — for advanced overrides only.

---

## Architecture (single file: `md2docx.py`)

Pipeline: `mistune AST → render_block() dispatcher → python-docx Document`

| Lines | Component |
|-------|-----------|
| 29–73 | Module-level style globals — all styling flows through these |
| 77–184 | `load_style()` / `build_style_constants()` — reads JSON, overwrites globals |
| 188–306 | Helpers: `_apply_run`, `_set_cell_bg`, `_set_table_borders`, etc. |
| 309–373 | `_add_cover_background()` (309) + `render_cover_page()` (346) |
| 378–447 | `render_inline()` — recursive inline AST walker |
| 451–656 | Block renderers: heading, paragraph, blockquote, list, table, hr, code_block |
| 660–707 | `render_block()` dispatcher + `_next_nonblank_type()` |
| 712–740 | `setup_document()` — margins, spacing, Normal style |
| 745–778 | `main()` entry point |

**mistune is used in AST mode** (`renderer='ast'`), not HTML. The `table` plugin must be present — passed at init in `main()`.

Silently skipped: `block_html` tokens (line 691), images in `render_inline()` (line 415). `thematic_break` only renders if `RENDER_THEMATIC_BREAKS=True` (default: `False`).

---

## Style JSON Files

| File | Notes |
|------|-------|
| `style_telus.json` | **Default and only style.** TELUS branding, cover enabled, `Telus_logo.png`. |
| `style_telus_no_cover.json` | Same TELUS branding, `cover.enabled: false`. Used internally by `--no-cover`. |

To create a custom style: copy `style_telus.json`, rename, edit. All colours are `"#RRGGBB"` hex strings. Pass via hidden `--style` flag.

`cover.enabled` defaults to `False` when the key is absent (`build_style_constants()` line 158).

Extra blockquote fields (`italic`, `border_width`, `border_space`, `space_before`, `space_after`) exist in `style_telus.json` but are **not consumed** — adding support requires changes to `build_style_constants()` and the relevant `render_*` function.

---

## MCP Server (`server.py`)

- Uses `FastMCP` from the `mcp` package.
- Two tools: `convert_markdown_to_docx` (text input) and `convert_md_file_to_docx` (file path input).
- Both take `cover_page: bool = True` — the only parameter users need.
- Calls `md2docx.py` via `subprocess.run`, passing `--style` and `--title` internally.

---

## Gotchas

- `.docx` output files are gitignored — don't commit them.
- `Telus_logo.png` must stay in the repo root — if deleted, cover renders without logo (no error).
- Footer renders unconditionally — `footer` JSON key only controls text/size.
- Cover title in `style_telus.json` (`"TELUS — Document Title"`) is a fallback; at runtime it is always overridden by the filename stem unless `--title` is explicitly passed.
