# AGENTS.md

## Repo at a Glance

Single-purpose Python tool: converts Markdown to `.docx`. Two entry points:
- `md2docx.py` — CLI
- `server.py` — MCP server (used by Claude Code / Cline)

No tests, no CI, no build system. Everything lives in the root.

---

## Commands

```bash
# Install
pip install -r requirements.txt   # mistune>=3, python-docx>=1.1, lxml>=4.9, mcp>=1.0

# CLI — default style is style_telus.json (cover page enabled)
python md2docx.py input.md output.docx

# CLI — no cover page
python md2docx.py input.md output.docx --style style_telus_no_cover.json

# CLI — explicit style
python md2docx.py input.md output.docx --style style_default.json
```

Verify changes by doing a real conversion and opening the `.docx` — there are no tests.

---

## Known Issues in Stale Docs (CLAUDE.md and README.md may lag)

- **CLI default style**: `main()` resolves `style_telus.json` as the default (line 750).
- **Server default style**: `server.py` sets `_DEFAULT_STYLE = style_telus.json` (line 22). Both CLI and server share the same default.
- **Cover page IS rendered** when `COVER_ENABLED=True`; `render_cover_page()` is called at line 759.
- **Footer is always rendered**: `_add_page_numbers()` is called unconditionally in `setup_document()` (line 738), regardless of the `footer` key in the style JSON. The `footer` key only controls the label text and size.
- **Logo**: `Telus_logo.png` in the repo root is the TELUS logo. `style_telus.json` references it by that name. Logo is silently skipped if the file doesn't exist (line 357 checks `COVER_LOGO_PATH.exists()`).
- **Fonts**: All styles use Poppins (body) and Roboto Slab (H1). Any "Calibri" claim in old docs is wrong.

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
| 745–769 | `main()` entry point |

**mistune is used in AST mode** (`renderer='ast'`), not HTML. The `table` plugin must be present — it is passed at init in `main()`.

Silently skipped: `block_html` tokens (line 691), images in `render_inline()` (line 415). `thematic_break` only renders if `RENDER_THEMATIC_BREAKS=True` (default: `False`).

---

## Style JSON Files

| File | Notes |
|------|-------|
| `style_telus.json` | **Default.** TELUS branding, cover enabled, references `logo.png`. |
| `style_telus_no_cover.json` | Same TELUS branding, `cover.enabled: false`. |
| `style_default.json` | No cover, no footer key. Poppins body, Roboto Slab H1. Minipass brand colours. |
| `style_personal.json` | Dark personal style, cover enabled, logo `no-logo.png` (silently skipped). |

To create a new style: copy any style file, rename, edit. All colours are `"#RRGGBB"` hex strings.

`cover.enabled` defaults to `False` when the key is absent (see `build_style_constants()` line 158: `cov.get('enabled', False)`). The module-level `COVER_ENABLED = True` at line 59 is always overridden at load time.

Extra blockquote fields (`italic`, `border_width`, `border_space`, `space_before`, `space_after`) exist in `style_telus.json` and `style_personal.json` but are **not consumed** by the script — adding support requires changes to `build_style_constants()` and the relevant `render_*` function.

---

## MCP Server (`server.py`)

- Uses `FastMCP` from the `mcp` package.
- Default style: `style_telus.json` (line 22).
- `convert_markdown_to_docx` writes a temp `.md` file then calls `md2docx.py` via `subprocess.run`.
- `convert_md_file_to_docx` calls `md2docx.py` directly on an existing file path.

---

## Gotchas

- `.docx` output files are gitignored — don't commit them.
- `Telus_logo.png` in the repo root is the TELUS logo used by `style_telus.json`. If it goes missing, the cover page renders without a logo (no error).
- `style_personal.json` references `no-logo.png` which doesn't exist — logo is silently skipped.
- Footer page numbers render unconditionally — the `footer` JSON key only controls text and size, not whether `_add_page_numbers()` runs.
- The `cover.title` in `style_telus.json` is placeholder text — teammates should update it per document or pass a custom style.
