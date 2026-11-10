# Prompt Master

A Claude Code mod that rewrites your draft prompt into a clearer, more specific one before you send it.

- **✨ Prompt Master** button just above the prompt box: type a draft, click it, and the rewritten prompt replaces your draft so you can review it and press Enter.
- **↩ Undo** puts your original draft back.
- `/promptmaster <text>` does the same from the keyboard (with no text, it rewrites the current draft).

It keeps your intent, file names, code and constraints, and adds structure: goal, context, requirements and what "done" looks like.

## Install

At the prompt of a Claude Code terminal session:

```
/plugin install prompt-master --marketplace marc-neumann-boop/minor-damage
```

Answer `y` to add the marketplace, then press Enter to pick the user scope.

From a shell:

```
claude plugin install prompt-master --marketplace marc-neumann-boop/minor-damage
```

In the desktop app: click **+** next to the prompt box → **Plugins** → **Add marketplace** with `marc-neumann-boop/minor-damage` → **Add plugin**.
