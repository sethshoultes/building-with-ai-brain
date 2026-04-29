# Brain Vault — Claude Code Operating Manual

This is Seth's Obsidian knowledge base at `~/brain`. When working in this vault, follow these conventions exactly.

## Vault Structure

| Folder | Purpose | Template |
|--------|---------|----------|
| `journal/` | Daily logs — what happened, decisions, frustrations | Date-named: `YYYY-MM-DD.md` |
| `learnings/` | Hard-won lessons from building | `templates/learning.md` |
| `projects/` | Living project notes | `templates/project.md` |
| `repos/` | Repository reference cards | `templates/repo.md` |
| `runbooks/` | Step-by-step operational procedures | Freeform with numbered steps |
| `scripts/` | Automation scripts (bash, python) | N/A — executable files |
| `templates/` | Note templates for Obsidian | N/A |
| `claude-memory/` | Synced Claude Code memories (auto-managed) | N/A — don't edit manually |
| `copilot/` | Copilot-related files | N/A |
| `backups/` | Vault backups | N/A |

## Note Creation Rules

### Frontmatter is mandatory
Every `.md` note must have YAML frontmatter. Follow the template for each type:

- **Learnings**: `title`, `date`, `source`, `tags`
- **Projects**: `name`, `status`, `repo`, `url`, `created`, `updated`, `tags`
- **Repos**: `name`, `url`, `status`, `language`, `created`, `last_active`, `tags`
- **Journal**: `date`, `tags`
- **Runbooks**: `title`, `date`, `tags` (minimum)

### File naming
- Journal entries: `YYYY-MM-DD.md`
- Everything else: `kebab-case.md` (lowercase, hyphens)
- Names should be descriptive and grep-friendly

### Wikilinks
- **A note without links is a bug.** Every note should link to at least one related note.
- Use `[[note-name]]` syntax (Obsidian wikilinks)
- Link learnings to the project that spawned them
- Link runbooks to the systems they operate on
- Link journal entries to projects/learnings created that day

### Tags
- Use lowercase, hyphenated tags: `#pipeline`, `#great-minds`, `#architecture`
- Tags go in frontmatter `tags: []` array, not inline
- Common tags: `architecture`, `pipeline`, `strategy`, `debugging`, `infrastructure`, `ai`, `wordpress`, `obsidian`

## Skills Available

These skills are installed in `.claude/skills/obsidian-skills/`:
- **obsidian-markdown** — OFM syntax (wikilinks, callouts, embeds, properties)
- **obsidian-cli** — Vault operations via Obsidian CLI
- **json-canvas** — Create/edit `.canvas` files
- **obsidian-bases** — Create/edit `.base` database views
- **defuddle** — Extract clean markdown from web pages (use instead of WebFetch for URLs)

## Session Workflow

### Starting a session
The SessionStart hook automatically injects:
- Current date
- Recent git activity in the vault
- Active projects
- Recent journal entry

### Saving knowledge
Route content to the right place:
- **"I learned that..."** → `learnings/` using the learning template
- **"Here's how to..."** → `runbooks/` with numbered steps
- **"Project update..."** → Update existing `projects/*.md` or create new
- **"Today I..."** → `journal/YYYY-MM-DD.md`

### Ending a session
Ask yourself:
- Any new notes need wikilinks added?
- Any learnings from this session worth capturing?
- Should the journal be updated?

## Rules

1. **Never modify `.obsidian/`** — Plugin configs are managed by Obsidian
2. **Never edit `claude-memory/`** — Auto-synced by `scripts/sync-memories.sh`
3. **Preserve frontmatter** — Never delete or corrupt existing YAML
4. **Use git mv** — Never delete + recreate to move files (loses history)
5. **Templates are sacred** — Read them, don't modify them
6. **Search before creating** — Use Grep/Glob to check if a note already exists
7. **Atomic notes** — One concept per note in `learnings/`, one procedure per note in `runbooks/`

## Hooks

| Hook | Trigger | What it does |
|------|---------|-------------|
| SessionStart | Every session | Injects vault context (date, git log, active projects, latest journal) |
| UserPromptSubmit | Every message | Classifies content type and suggests routing |
| PostToolUse | After Write/Edit on .md | Validates frontmatter and wikilinks |

## Obsidian REST API

The Local REST API is running on `https://127.0.0.1:27124/` and `http://127.0.0.1:27123/`.
Use it via MCP tools when Obsidian is open for: search, file ops, periodic notes, tag listing.
For direct file operations, use the filesystem (Read/Write/Edit) — it's faster and doesn't require Obsidian to be running.
