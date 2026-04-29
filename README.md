# building-with-ai-brain

A **public skeleton** for a personal Obsidian knowledge vault wired to Claude Code as persistent memory. Clone it as a starting point for your own vault — the structure, the operating manual at `CLAUDE.md`, the note templates, the semantic search script, and a handful of already-public learnings as exemplars.

The *real* vault behind this skeleton stays private. This repo is the canonical reference companion to the recipe at [sethshoultes.com/recipes/claude-code-brain-vault.html](https://sethshoultes.com/recipes/claude-code-brain-vault.html) and the installable Agent Skill at [`set-up-claude-code-with-brain-vault`](https://github.com/sethshoultes/building-with-ai-skills/blob/main/skills/set-up-claude-code-with-brain-vault/SKILL.md).

## Why this exists

Posts on [sethshoultes.com](https://sethshoultes.com/blog) reference brain-vault learnings by URL. Those URLs used to point at a private repo, which 404'd for everyone but me. This is the public skeleton — same shape, same conventions, exemplar content, no personal context. Now the references resolve.

## Use it

### As a starting point for your own vault

```bash
# Clone as your own vault
git clone https://github.com/sethshoultes/building-with-ai-brain.git ~/brain
cd ~/brain
git remote remove origin                          # disconnect from this repo
gh repo create my-brain --private --source=.      # create your own private repo
git push -u origin main
```

Now you have a structured vault with the operating manual, the templates, and a few example learnings to model your own notes against. Add your own — start by emptying the example `learnings/` and `runbooks/`.

### As a reference

If you just want to see how a Claude-Code-wired brain vault is shaped, browse the directories:

| Folder | Purpose |
|---|---|
| `CLAUDE.md` | The operating manual every Claude Code session loads |
| `templates/` | Note templates (`learning.md`, `project.md`, `repo.md`) |
| `scripts/brain-search.py` | Local semantic search over the vault using Ollama embeddings |
| `learnings/` | Example hard-won lessons (six exemplars from the live blog) |
| `runbooks/` | Example operational procedure (one exemplar) |
| `journal/`, `projects/`, `repos/` | Empty placeholders showing the structure |

The full setup walkthrough — Obsidian, Ollama, Git plugin, hooks, the `/brain` skill — is at [sethshoultes.com/recipes/claude-code-brain-vault.html](https://sethshoultes.com/recipes/claude-code-brain-vault.html).

## Structure

```
building-with-ai-brain/
├── CLAUDE.md             ← operating manual
├── README.md             ← this file
├── LICENSE               ← MIT
├── templates/            ← Obsidian + /brain skill templates
│   ├── learning.md
│   ├── project.md
│   └── repo.md
├── scripts/
│   └── brain-search.py   ← semantic search via Ollama embeddings
├── learnings/            ← exemplar lessons learned (~5)
├── runbooks/             ← exemplar procedures (~1)
├── journal/              ← (empty in skeleton; YYYY-MM-DD.md in practice)
├── projects/             ← (empty in skeleton)
├── repos/                ← (empty in skeleton)
└── backups/              ← (empty in skeleton; for vault snapshots)
```

## What's NOT in here

- Real journal entries
- Personal project notes
- Anything mentioning specific clients, in-flight work, or credentials
- The full set of brain learnings (~30 in the live vault as of writing); only the ones already discussed publicly in blog posts
- The `claude-memory/` directory (Claude Code synced memories — auto-managed, not portable)

## The exemplar learnings

These are real learnings from the live brain vault, copied over because they're already discussed publicly in blog posts on sethshoultes.com:

| Learning | Discussed in |
|---|---|
| `multi-agent-essay-production-recipe.md` | [The Recipe That Wrote Itself](https://sethshoultes.com/blog/the-recipe-that-wrote-itself.html), [Skills as SOPs](https://sethshoultes.com/blog/skills-as-sops.html) |
| `hooks-as-temporal-grammar-of-tool-systems.md` | [What's on the Desk](https://sethshoultes.com/blog/whats-on-the-desk.html) |
| `github-pages-rebuild-race-breaks-post-publish-webhooks.md` | [The Avatar Reads First](https://sethshoultes.com/blog/the-avatar-reads-first.html) |
| `cross-model-persona-portability.md` | [Three Sessions Running](https://sethshoultes.com/blog/agentic-economy-three-sessions-running.html) |
| `orchestrator-and-writer-are-different-ai-roles.md` | [The Bible Reads First](https://sethshoultes.com/blog/the-bible-reads-first.html) |

Each one is a real-world pattern with the gotcha, the why, and how to apply.

## Setup walkthrough

The full how-to lives at the recipe page — [sethshoultes.com/recipes/claude-code-brain-vault.html](https://sethshoultes.com/recipes/claude-code-brain-vault.html). The short version:

1. Clone this repo as your own vault (instructions above).
2. Open it as an Obsidian vault and enable the Git plugin (10-min auto-push).
3. Pull the `nomic-embed-text` Ollama model and run `python3 scripts/brain-search.py index`.
4. Install the `/brain` skill at `~/.claude/skills/brain/SKILL.md` (template in the skill repo: [`set-up-claude-code-with-brain-vault`](https://github.com/sethshoultes/building-with-ai-skills/blob/main/skills/set-up-claude-code-with-brain-vault/SKILL.md)).
5. Wire the SessionStart and Stop hooks in `~/.claude/settings.json`.
6. Push to your own private GitHub repo.

## Companion artifacts

- **Recipe (long-form how-to):** [sethshoultes.com/recipes/claude-code-brain-vault.html](https://sethshoultes.com/recipes/claude-code-brain-vault.html)
- **Agent Skill (installable):** [`set-up-claude-code-with-brain-vault`](https://github.com/sethshoultes/building-with-ai-skills/blob/main/skills/set-up-claude-code-with-brain-vault/SKILL.md)
- **Companion essay:** [Skills as SOPs](https://sethshoultes.com/blog/skills-as-sops.html) — the argument for treating processes as installable artifacts
- **Companion essay:** [What's on the Desk](https://sethshoultes.com/blog/whats-on-the-desk.html) — what the brain vault feels like in day-to-day use
- **Cookbook playbook:** [`great-minds-cookbook/recipes/multi-agent-essay-production`](https://github.com/sethshoultes/great-minds-cookbook/tree/main/recipes/multi-agent-essay-production) — exercises the same brain-vault pattern at the production scale

## License

MIT — see [LICENSE](./LICENSE). The exemplar learnings and runbook were originally written by Seth Shoultes for personal use; copying, adapting, and republishing them under MIT is the explicit intent of this repo.

## Author

[Seth Shoultes](https://sethshoultes.com) · [GitHub](https://github.com/sethshoultes) · [LinkedIn](https://www.linkedin.com/in/shoultes/)
