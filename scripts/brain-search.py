#!/usr/bin/env python3
"""
brain-search: Semantic search over the Obsidian vault using Ollama embeddings.

Usage:
    python brain-search.py index          # Rebuild the embedding index
    python brain-search.py search "query" # Search for similar notes
    python brain-search.py search "query" --top 10  # Return more results
    python brain-search.py ask "question" # Ask gemma3:1b a question using your notes as context
"""

import json
import os
import sys
from pathlib import Path
import requests
import struct

VAULT_DIR = Path(__file__).resolve().parent.parent
INDEX_FILE = VAULT_DIR / ".brain-index.json"
OLLAMA_URL = "http://localhost:11434"
EMBED_MODEL = "nomic-embed-text"


def get_md_files():
    """Find all markdown files in the vault, excluding dotfiles and templates."""
    for md in sorted(VAULT_DIR.rglob("*.md")):
        rel = md.relative_to(VAULT_DIR)
        # Skip hidden dirs, scripts, and node_modules
        if any(part.startswith(".") for part in rel.parts):
            continue
        if rel.parts[0] in ("scripts",):
            continue
        yield md


def embed(text: str) -> list[float]:
    """Get embedding vector from Ollama."""
    resp = requests.post(
        f"{OLLAMA_URL}/api/embed",
        json={"model": EMBED_MODEL, "input": text},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["embeddings"][0]


def cosine_sim(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def build_index():
    """Embed all markdown files and save the index."""
    index = {}
    files = list(get_md_files())
    print(f"Indexing {len(files)} files...")

    for i, md in enumerate(files, 1):
        rel = str(md.relative_to(VAULT_DIR))
        content = md.read_text(errors="replace")
        # Use first 2000 chars to keep embedding focused
        chunk = content[:2000]
        if not chunk.strip():
            continue
        print(f"  [{i}/{len(files)}] {rel}")
        vec = embed(chunk)
        index[rel] = {
            "title": md.stem,
            "preview": content[:200].replace("\n", " "),
            "embedding": vec,
        }

    with open(INDEX_FILE, "w") as f:
        json.dump(index, f)
    print(f"\nIndex saved: {len(index)} files -> {INDEX_FILE.name}")


def search(query: str, top_n: int = 5):
    """Search the index for notes similar to the query."""
    if not INDEX_FILE.exists():
        print("No index found. Run: python brain-search.py index")
        sys.exit(1)

    with open(INDEX_FILE) as f:
        index = json.load(f)

    query_vec = embed(query)
    scores = []
    for path, entry in index.items():
        sim = cosine_sim(query_vec, entry["embedding"])
        scores.append((sim, path, entry["preview"]))

    scores.sort(reverse=True)
    print(f"\nResults for: \"{query}\"\n")
    for score, path, preview in scores[:top_n]:
        print(f"  {score:.3f}  {path}")
        print(f"         {preview[:100]}...")
        print()


def ask(question: str, top_n: int = 3):
    """Search for relevant notes and ask gemma3:1b to answer based on them."""
    if not INDEX_FILE.exists():
        print("No index found. Run: python brain-search.py index")
        sys.exit(1)

    with open(INDEX_FILE) as f:
        index = json.load(f)

    query_vec = embed(question)
    scores = []
    for path, entry in index.items():
        sim = cosine_sim(query_vec, entry["embedding"])
        scores.append((sim, path))

    scores.sort(reverse=True)
    top_files = scores[:top_n]

    # Read full content of top matches
    context_parts = []
    print(f"Reading {len(top_files)} notes...\n")
    for score, path in top_files:
        full_path = VAULT_DIR / path
        content = full_path.read_text(errors="replace")
        context_parts.append(f"--- {path} (relevance: {score:.3f}) ---\n{content}")

    context = "\n\n".join(context_parts)

    prompt = f"""Based on the following notes from my knowledge base, answer this question.
If the notes don't contain enough information, say so.
Be concise and direct.

NOTES:
{context}

QUESTION: {question}"""

    # Stream response from gemma3:1b
    resp = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={"model": "gemma3:1b", "prompt": prompt, "stream": True},
        stream=True,
        timeout=120,
    )
    resp.raise_for_status()
    for line in resp.iter_lines():
        if line:
            chunk = json.loads(line)
            print(chunk.get("response", ""), end="", flush=True)
            if chunk.get("done"):
                break
    print()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "index":
        build_index()
    elif cmd == "search":
        if len(sys.argv) < 3:
            print("Usage: python brain-search.py search \"your query\"")
            sys.exit(1)
        query = sys.argv[2]
        top_n = 5
        if "--top" in sys.argv:
            top_n = int(sys.argv[sys.argv.index("--top") + 1])
        search(query, top_n)
    elif cmd == "ask":
        if len(sys.argv) < 3:
            print("Usage: python brain-search.py ask \"your question\"")
            sys.exit(1)
        question = sys.argv[2]
        top_n = 3
        if "--top" in sys.argv:
            top_n = int(sys.argv[sys.argv.index("--top") + 1])
        ask(question, top_n)
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
