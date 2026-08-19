# Skills

Devansh's personal agent skills, packaged as a multi-skill repository.

Repository: https://github.com/Devansh-365/skills

## Install

List available skills:

```sh
npx skills add Devansh-365/skills --list
```

Install every skill:

```sh
npx skills add Devansh-365/skills --skill '*'
```

Install one skill:

```sh
npx skills add Devansh-365/skills --skill humanizer
```

You can also install from the full GitHub URL:

```sh
npx skills add https://github.com/Devansh-365/skills --skill humanizer
```

For local development from this checkout:

```sh
npx skills add . --list
npx skills add . --skill humanizer
```

## Layout

Each skill lives in its own directory under `skills/` and must include a
`SKILL.md` file with YAML frontmatter (`name`, `description`):

```text
skills/
  humanizer/
    SKILL.md
    references/
    scripts/
    assets/
```

`references/`, `scripts/`, and `assets/` are optional — add them only when a
skill needs supporting docs, helper scripts, or static files.

## Validate

Validate every skill package's metadata, Markdown fences, and local links:

```sh
python -m pip install pyyaml==6.0.3
python scripts/validate_skills.py
```

The same check runs in GitHub Actions on pull requests and pushes to `main`.

## Skills

- `humanizer`: Remove signs of AI-generated writing from text — inflated
  symbolism, promotional language, em dash overuse, rule of three, AI
  vocabulary, and other patterns from Wikipedia's "Signs of AI writing" guide.
