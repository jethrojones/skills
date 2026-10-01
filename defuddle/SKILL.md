---
name: defuddle
description: Read and extract clean content from URLs using the defuddle CLI. Use when given a URL to read, when fetching web page content, or when the user asks to read/parse/extract content from a website. Converts cluttered web pages to clean markdown or JSON with metadata.
---

# Defuddle

Extract readable content from web pages, stripping ads, navigation, comments, and other clutter.

## Commands

```bash
# Get clean markdown (default for reading)
defuddle parse <url> --markdown

# Get JSON with full metadata (title, author, published, word count)
defuddle parse <url> --json

# Extract specific property
defuddle parse <url> --property title

# Parse local HTML file
defuddle parse page.html --markdown

# Save to file
defuddle parse <url> --markdown --output result.md
```

## When to Use

- User provides a URL and wants to understand its content
- Reading documentation, articles, or blog posts
- Extracting structured data from web pages

## Response Properties (JSON mode)

- `content` - Cleaned HTML
- `title` - Page title
- `description` - Meta description
- `author` - Author name
- `published` - Publication date
- `wordCount` - Word count
- `domain` - Source domain

## Notes

- Requires Node.js. Install: `npm install -g defuddle jsdom`
- Some dynamic/JS-heavy pages may not extract fully (fall back to `web_fetch` or browser tools)
