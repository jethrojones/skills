---
name: convert-word-to-markdown
description: Converts Word (.docx) files to Markdown (.md) format using pandoc. Use when you need to convert Word documents to Markdown for processing.
---

# Convert Word to Markdown Skill

## Purpose
Converts Word (.docx) files to Markdown (.md) format so they can be processed, edited, or used with other tools.

## Prerequisites
- pandoc must be installed (`which pandoc` to verify)
- If not installed: `brew install pandoc`

## Input
- One or more `.docx` file paths, OR
- A directory containing `.docx` files

## Your Task

### Convert Specific Files

To convert specific files:
```bash
pandoc "filename.docx" -f docx -t markdown -o "filename.md"
```

### Convert All DOCX Files in Directory

To convert all .docx files in the current directory:
```bash
find . -name "*.docx" -type f -exec sh -c 'pandoc "$1" -f docx -t markdown -o "${1%.docx}.md"' _ {} \;
```

### Verify Conversion

Count converted files:
```bash
find . -name "*.md" -type f | wc -l
```

List the converted files:
```bash
find . -name "*.md" -type f
```

## Example Usage

**Single file:**
```bash
pandoc "Goals 6-1.docx" -f docx -t markdown -o "Goals 6-1.md"
```

**Multiple specific files:**
```bash
pandoc "Goals 6-1.docx" -f docx -t markdown -o "Goals 6-1.md"
pandoc "Goals 6-2.docx" -f docx -t markdown -o "Goals 6-2.md"
pandoc "Goals 6-3.docx" -f docx -t markdown -o "Goals 6-3.md"
```

**All files in directory:**
```bash
find . -name "*.docx" -type f -exec sh -c 'pandoc "$1" -f docx -t markdown -o "${1%.docx}.md"' _ {} \;
```

## Quality Checks

After conversion, verify:
- All .docx files have corresponding .md files
- Markdown formatting is preserved (headers, lists, bold, italic)
- No conversion errors occurred

## Notes

- Original .docx files are preserved (not deleted)
- If a .md file already exists, it will be overwritten
- Complex Word formatting may not convert perfectly to Markdown
