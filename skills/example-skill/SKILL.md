---
name: example-skill
description: Template skill showing the expected package layout. Replace this with your own skill and delete the example once you've added a real one.
---

# Example Skill

This is a placeholder skill package that shows the expected layout for this
repository. Duplicate this directory to start a new skill, then remove the
example once you have at least one real skill in place.

## Layout

```text
skills/example-skill/
  SKILL.md        # required: frontmatter (name, description) + instructions
  references/      # optional: supporting docs loaded on demand
  scripts/         # optional: helper scripts the skill can run
  assets/          # optional: templates, fixtures, static files
```

## Writing a skill

- `name` must be lowercase, hyphen-separated, and match the directory name.
- `description` should say what the skill does and when to use it — this is
  what triggers the skill being loaded, so be specific.
- Keep the body focused: what to do, in what order, and any hard constraints.
  Put long reference material in `references/` instead of inline.
