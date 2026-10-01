---
name: hubspot-cli
description: Manage HubSpot development via the `hs` CLI — projects, apps, CMS assets, HubDB, custom objects, secrets, and sandboxes. Use when creating HubSpot apps, deploying projects, managing CMS themes/modules, working with serverless functions, or syncing local development with HubSpot. Triggers: "hubspot project", "hs cli", "hubspot app", "cms upload", "hubdb", "custom object schema", "hubspot secrets", "hubspot sandbox".
---

# HubSpot CLI

CLI for HubSpot development: projects, apps, CMS, HubDB, custom objects, secrets, sandboxes.

## Quick Reference

```bash
hs --version              # Check CLI version
hs doctor                 # Diagnose config & connectivity
hs account list           # List configured accounts
hs account use <name>     # Switch default account
hs open                   # Open HubSpot in browser
```

## Authentication

```bash
# First-time setup (opens browser for personal access key)
hs init

# Add another account
hs auth

# Use existing key directly
hs auth --personal-access-key "YOUR_KEY"

# OAuth2 (for public apps)
hs auth --auth-type oauth2
```

Config stored at: `~/.hscli/config.yml`

## Projects

Projects are the modern way to build HubSpot apps with UI extensions, serverless functions, and CRM cards.

```bash
# Create new project
hs project create

# List projects in account
hs project list

# Local development (hot reload)
hs project dev

# Watch for changes & auto-upload
hs project watch

# Upload & create new build
hs project upload

# Deploy a build
hs project deploy

# View logs for serverless function
hs project logs

# Download project from HubSpot
hs project download

# Validate before upload
hs project validate

# Install dependencies
hs project install-deps

# Lint UI extensions
hs project lint
```

### Project Structure

```
my-project/
├── hsproject.json           # Project config
├── src/
│   ├── app/
│   │   ├── app.json         # App manifest
│   │   └── extensions/      # UI extensions
│   └── functions/           # Serverless functions
└── package.json
```

## Apps

```bash
# Migrate public app to projects framework
hs app migrate

# Manage app secrets
hs app secret list
hs app secret add <name>
hs app secret update <name>
hs app secret delete <name>
```

## CMS Assets

Manage themes, modules, templates, and files in Design Manager.

```bash
# Upload local → HubSpot
hs cms upload <src> <dest>
hs cms upload ./theme @hubspot/theme

# Download HubSpot → local
hs cms fetch <src> [dest]
hs cms fetch @hubspot/theme ./theme

# Watch & sync changes
hs cms watch <src> <dest>

# List remote files
hs cms list [path]

# Delete remote file/folder
hs cms delete <path>

# Move remote file
hs cms mv <src> <dest>
```

### Themes & Modules

```bash
# Theme commands
hs cms theme --help

# Module commands
hs cms module --help

# Marketplace validation
hs cms module marketplace-validate <path>

# Get default React module
hs cms get-react-module [name] [dest]
```

### Serverless Functions (CMS)

```bash
hs cms function --help
```

## HubDB

HubDB is HubSpot's built-in database for dynamic content.

```bash
# List tables
hs hubdb list

# Create table
hs hubdb create

# Fetch table schema
hs hubdb fetch <table-id> [dest]

# Clear all rows
hs hubdb clear <table-id>

# Delete table
hs hubdb delete <table-id>
```

## Custom Objects

Define custom CRM objects beyond Contacts, Companies, Deals, Tickets.

```bash
# List schemas
hs custom-object list-schemas

# Create schema
hs custom-object create-schema

# Fetch schema
hs custom-object fetch-schema <name> [dest]

# Fetch all schemas
hs custom-object fetch-all-schemas [dest]

# Update schema
hs custom-object update-schema <name>

# Delete schema
hs custom-object delete-schema <name>

# Create object instances
hs custom-object create <name>
```

## Secrets

Secrets for serverless functions (not app secrets).

```bash
hs secret list
hs secret add <name>
hs secret update <name>
hs secret delete <name>
```

## Sandboxes

Development sandboxes for testing.

```bash
hs sandbox create
hs sandbox delete
```

## Test Accounts

```bash
hs test-account --help
```

## MCP Integration (Beta)

Setup HubSpot MCP servers for AI development.

```bash
hs mcp setup
```

## Global Options

```bash
-a, --account <name>    # Use specific account (overrides default)
-c, --config <path>     # Custom config file path
-d, --debug             # Enable debug logging
```

## Common Workflows

### Start New Project

```bash
hs project create
cd my-project
hs project dev
```

### Deploy CMS Theme

```bash
hs cms upload ./my-theme @hubspot/my-theme
hs cms watch ./my-theme @hubspot/my-theme  # For ongoing dev
```

### Export Custom Object Schemas

```bash
mkdir -p schemas
hs custom-object fetch-all-schemas ./schemas
```

### Switch Between Accounts

```bash
hs account list
hs account use production
hs project upload  # Now uploads to production
```

## Docs

- Projects: https://developers.hubspot.com/docs/getting-started/quickstart
- Custom Objects: https://developers.hubspot.com/docs/api-reference/crm-custom-objects-v3/guide
- CLI Reference: https://developers.hubspot.com/docs/reference/cli
