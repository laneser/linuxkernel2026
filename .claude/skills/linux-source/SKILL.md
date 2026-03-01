---
name: linux-source
description: "Manage a local Linux kernel source tree at /tmp/linux for code reference. Use when the user wants to look up kernel source code, search for implementations, read kernel headers, or browse subsystem code. Triggers on: kernel source lookup, 'show me the kernel implementation of X', 'how does the kernel do Y', browsing lib/, drivers/, fs/, net/, mm/, etc."
---

# Linux Kernel Source Reference

Maintain a shallow clone of the latest **stable release** (no RC) of the Linux kernel
at `/tmp/linux` for source code lookup during learning.

## Step 1: Ensure source is available

Check if `/tmp/linux` exists and is a valid git repo, and verify it's on a stable tag:

```bash
test -d /tmp/linux/.git && echo "EXISTS" || echo "MISSING"
```

**If MISSING** — clone and checkout latest stable tag:
```bash
git clone --depth 1 -b master \
  https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git \
  /tmp/linux

# Find and checkout latest stable tag (exclude RC versions)
LATEST_TAG=$(git -C /tmp/linux ls-remote --tags origin 'refs/tags/v*' \
  | grep -v '\-rc' | grep -v '\^{}' \
  | sed 's|.*refs/tags/||' \
  | sort -V | tail -1)
git -C /tmp/linux fetch --depth 1 origin tag "$LATEST_TAG"
git -C /tmp/linux checkout "$LATEST_TAG"
echo "Checked out: $LATEST_TAG"
```

**If EXISTS** — verify it's on a stable tag, update if needed:
```bash
# Check current tag
CURRENT=$(git -C /tmp/linux describe --tags --exact-match 2>/dev/null || echo "no tag")
echo "Current: $CURRENT"

# To update to latest stable:
LATEST_TAG=$(git -C /tmp/linux ls-remote --tags origin 'refs/tags/v*' \
  | grep -v '\-rc' | grep -v '\^{}' \
  | sed 's|.*refs/tags/||' \
  | sort -V | tail -1)
if [ "$CURRENT" != "$LATEST_TAG" ]; then
  git -C /tmp/linux fetch --depth 1 origin tag "$LATEST_TAG"
  git -C /tmp/linux checkout "$LATEST_TAG"
  echo "Updated to: $LATEST_TAG"
else
  echo "Already on latest stable: $LATEST_TAG"
fi
```

Show the current kernel version after clone/update:
```bash
head -5 /tmp/linux/Makefile
```

**IMPORTANT:** The tag version determines the GitHub link base URL. Store the tag
for use in source code references:
```bash
KERNEL_TAG=$(git -C /tmp/linux describe --tags --exact-match)
echo "GitHub base: https://github.com/torvalds/linux/blob/$KERNEL_TAG/"
```

## Step 2: Search and browse

Use the standard tools to search the kernel source:

- **Glob** — find files by pattern: `Glob("/tmp/linux/lib/list_sort.c")`, `Glob("/tmp/linux/drivers/i2c/**/*.c")`
- **Grep** — search code content: `Grep("container_of", path="/tmp/linux/include/linux/")`
- **Read** — read specific files: `Read("/tmp/linux/lib/list_sort.c")`

### Common search patterns

| Goal | Command |
|------|---------|
| Find a file | `Glob("/tmp/linux/**/filename.c")` |
| Find a function definition | `Grep("^static.*function_name", path="/tmp/linux/", type="c")` |
| Find a struct definition | `Grep("^struct struct_name \\{", path="/tmp/linux/include/")` |
| Find a macro | `Grep("#define MACRO_NAME", path="/tmp/linux/include/")` |
| Find Kconfig option | `Grep("config OPTION_NAME", path="/tmp/linux/", glob="Kconfig")` |
| Browse a subsystem | `Glob("/tmp/linux/subsystem/**/*.c")` then read key files |

### Key directories

| Path | Content |
|------|---------|
| `include/linux/` | Core kernel headers |
| `kernel/` | Core kernel code (sched, fork, signal, etc.) |
| `mm/` | Memory management |
| `fs/` | File systems |
| `drivers/` | Device drivers |
| `net/` | Networking |
| `lib/` | Library routines (list_sort, string, etc.) |
| `arch/` | Architecture-specific code |
| `Documentation/` | Kernel documentation |

## Guidelines

- `/tmp/linux` is ephemeral (not persisted across container rebuilds) — re-clone when needed
- Use `--depth 1` to keep disk usage minimal (~2 GB vs ~5 GB full history)
- Do NOT modify the kernel source — it's read-only reference
- **Always checkout a stable tag** (e.g., `v6.19`), never stay on `master` — master changes frequently and line numbers will drift from the tag used in GitHub links
- When quoting kernel code, include the file path, **line number**, and **GitHub link with version tag** (e.g., `https://github.com/torvalds/linux/blob/v6.19/kernel/fork.c#L2291`)
- **Verify line numbers match the checked-out tag** — if the local source is on a different commit than the linked tag, line numbers will be wrong
- For large files, read specific line ranges rather than the entire file
