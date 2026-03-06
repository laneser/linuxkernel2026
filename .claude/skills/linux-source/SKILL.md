---
name: linux-source
description: "Manage a local Linux kernel source tree at /tmp/linux for code reference and git history search. Use when the user wants to look up kernel source code, search for implementations, read kernel headers, browse subsystem code, or search git log for commit history. Triggers on: kernel source lookup, 'show me the kernel implementation of X', 'how does the kernel do Y', browsing lib/, drivers/, fs/, net/, mm/, git log, commit history, 'when was X added/removed'."
---

# Linux Kernel Source Reference

Maintain a **full clone** of the latest **stable release** (no RC) of the Linux kernel
at `/tmp/linux` for source code lookup and git history search.

Full clone（含完整 git history）是必要的——課程作業經常要求用 `git log` 搜尋特定功能的演進過程（如 prefetch 從 list API 移除的原因）。Shallow clone 無法搜 commit history。

## Step 1: Ensure source is available

Check if `/tmp/linux` exists, is a valid git repo, and has full history:

```bash
test -d /tmp/linux/.git && echo "EXISTS" || echo "MISSING"
```

**If MISSING** — full clone and checkout latest stable tag:
```bash
git clone \
  https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git \
  /tmp/linux

# Find and checkout latest stable tag (exclude RC versions)
LATEST_TAG=$(git -C /tmp/linux ls-remote --tags origin 'refs/tags/v*' \
  | grep -v '\-rc' | grep -v '\^{}' \
  | sed 's|.*refs/tags/||' \
  | sort -V | tail -1)
git -C /tmp/linux checkout "$LATEST_TAG"
echo "Checked out: $LATEST_TAG"
```

**If EXISTS but shallow** — unshallow to get full history:
```bash
DEPTH=$(git -C /tmp/linux rev-list --count HEAD)
if [ "$DEPTH" -lt 100 ]; then
  echo "Shallow clone detected ($DEPTH commits). Fetching full history..."
  git -C /tmp/linux fetch --unshallow
  echo "Done. Full history available."
fi
```

**If EXISTS with full history** — verify it's on a stable tag:
```bash
CURRENT=$(git -C /tmp/linux describe --tags --exact-match 2>/dev/null || echo "no tag")
echo "Current: $CURRENT"
```

Show the current kernel version:
```bash
head -5 /tmp/linux/Makefile
```

**IMPORTANT:** The tag version determines the GitHub link base URL:
```bash
KERNEL_TAG=$(git -C /tmp/linux describe --tags --exact-match)
echo "GitHub base: https://github.com/torvalds/linux/blob/$KERNEL_TAG/"
```

## Step 2: Search source code

Use the standard tools:

- **Glob** — find files: `Glob("/tmp/linux/lib/list_sort.c")`
- **Grep** — search content: `Grep("container_of", path="/tmp/linux/include/linux/")`
- **Read** — read files: `Read("/tmp/linux/lib/list_sort.c")`

### Common search patterns

| Goal | Command |
|------|---------|
| Find a file | `Glob("/tmp/linux/**/filename.c")` |
| Find a function definition | `Grep("^static.*function_name", path="/tmp/linux/", type="c")` |
| Find a struct definition | `Grep("^struct struct_name \\{", path="/tmp/linux/include/")` |
| Find a macro | `Grep("#define MACRO_NAME", path="/tmp/linux/include/")` |
| Find Kconfig option | `Grep("config OPTION_NAME", path="/tmp/linux/", glob="Kconfig")` |

## Step 3: Search git history

Full history enables commit log search — essential for understanding why code was added, changed, or removed.

```bash
cd /tmp/linux

# 搜特定檔案的 commit 歷史
git log --oneline -- include/linux/list.h

# 搜 commit message 含特定關鍵字
git log --oneline --grep="prefetch" -- include/linux/list.h

# 搜程式碼的新增或移除（pickaxe search）
git log --oneline -S "prefetch" -- include/linux/list.h

# 看完整 commit 訊息和 diff
git show <hash>

# 看某次 commit 改了哪些檔案
git show --stat <hash>

# 搜特定作者的 commit
git log --oneline --author="Torvalds" -- include/linux/list.h
```

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
- Full clone uses ~4-5 GB disk; `df -h /tmp` to check space before cloning
- Do NOT modify the kernel source — it's read-only reference
- **Always checkout a stable tag** (e.g., `v6.19`), never stay on `master`
- When quoting kernel code, include the file path, **line number**, and **GitHub link with version tag**
- **Verify line numbers match the checked-out tag**
- For large files, read specific line ranges rather than the entire file
