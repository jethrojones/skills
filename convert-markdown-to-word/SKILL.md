---
name: convert-markdown-to-word
description: Converts Markdown (.md) files to Word (.docx) format using pandoc. Use when you need to convert Markdown files to Word for sharing or Google Drive upload.
---

# Convert Markdown to Word Skill

## Purpose
Converts Markdown (.md) files to Word (.docx) format for sharing, uploading to Google Drive, or opening in Microsoft Word/Google Docs.

## Prerequisites
- pandoc must be installed (`which pandoc` to verify)
- If not installed: `brew install pandoc`

## Input
- One or more `.md` file paths, OR
- A directory containing `.md` files

## Your Task

### Convert Specific Files

To convert specific files:
```bash
pandoc "filename.md" -f markdown -t docx -o "filename.docx"
```

### Convert to a Specific Output Folder

Create output folder and convert:
```bash
mkdir -p google-drive-ready
pandoc "filename.md" -f markdown -t docx -o "google-drive-ready/filename.docx"
```

### Convert All Markdown Files in Directory

To convert all .md files (excluding skill files) to a google-drive-ready folder:
```bash
mkdir -p google-drive-ready
find . -name "*.md" -type f ! -name "*skill*" ! -name "*SKILL*" ! -path "*/google-drive-ready/*" ! -path "*/.claude/*" -exec bash -c 'filename=$(basename "$1"); pandoc "$1" -f markdown -t docx -o "google-drive-ready/${filename%.md}.docx"' _ {} \;
```

### Verify Conversion

Count converted files:
```bash
ls -1 google-drive-ready/*.docx 2>/dev/null | wc -l
```

List the converted files:
```bash
ls -la google-drive-ready/
```

## Example Usage

**Single file:**
```bash
pandoc "Goals 6-1.md" -f markdown -t docx -o "Goals 6-1.docx"
```

**Multiple specific files to output folder:**
```bash
mkdir -p google-drive-ready
pandoc "Goals 6-1.md" -f markdown -t docx -o "google-drive-ready/Goals 6-1.docx"
pandoc "Goals 6-2.md" -f markdown -t docx -o "google-drive-ready/Goals 6-2.docx"
pandoc "Goals 6-3.md" -f markdown -t docx -o "google-drive-ready/Goals 6-3.docx"
```

## Quality Checks

After conversion, verify:
- All .md files have corresponding .docx files
- File count matches expected number
- Markdown formatting is preserved in Word (headers, lists, bold, italic)

## Notes

- Original .md files are preserved (not deleted)
- If a .docx file already exists, it will be overwritten
- The `google-drive-ready` folder is the standard output location for files ready to upload
- Skill files (.claude/skills/) are automatically excluded from batch conversion
