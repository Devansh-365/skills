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
npx skills add Devansh-365/skills --skill example-skill
```

You can also install from the full GitHub URL:

```sh
npx skills add https://github.com/Devansh-365/skills --skill example-skill
```

For local development from this checkout:

```sh
npx skills add . --list
npx skills add . --skill example-skill
```

## Layout

Each skill lives in its own directory under `skills/` and must include a
`SKILL.md` file with YAML frontmatter (`name`, `description`):

```text
skills/
  example-skill/
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

- `example-skill`: Template showing the expected package layout. Replace it
  with a real skill and delete the example once you've added one.
