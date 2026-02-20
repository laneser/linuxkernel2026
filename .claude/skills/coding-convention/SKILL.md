---
name: coding-convention
description: C coding style guide based on lab0-c CONTRIBUTING.md (K&R variant). Use when writing, reviewing, or modifying C code in course homework. Enforces consistent style for indentation, naming, comments, control flow, types, and more.
---

# C Coding Convention

C coding style for course homework, derived from [lab0-c CONTRIBUTING.md](https://github.com/sysprog21/lab0-c/blob/master/CONTRIBUTING.md). This is a K&R style variant. See [references/full-style-guide.md](references/full-style-guide.md) for complete rules with code examples.

## When to apply

Apply these rules when writing or modifying C code in `homework/` directories (lab0-c and future assignments). The repository includes a `.clang-format` file and pre-commit hooks that enforce formatting automatically.

## Quick reference

### Layout
- **4 spaces** for indentation — **never tabs** (ASCII 0x9)
- **80 characters** max line width
- Opening `{` on same line as control statements, **separate line** for function definitions

### Naming
- **snake_case** everywhere — no camelCase, no Hungarian notation
- Type names suffixed with `_t` (e.g., `route_info_t`)
- Use English for all names and comments; use American English (`en_US`)

### Comments
- Multi-line: `/*` and `*/` on their own lines, body prefixed with ` *`
- Single-line (inline): C89 style `/* comment */`, two spaces after the statement
- Do not comment out code — use `#if 0` ... `#endif`
- Use `WARNING`, `NOTE`, `TODO` markers for searchable annotations

### Spacing
- One space after `if`, `while`, `for`, `switch`, `return`
- No space after function names, `sizeof`, or macro names
- Spaces around binary and assignment operators; no space around unary operators
- Spaces around ternary `?` and `:`; no space around `->`, `.`, `[]`

### Declarations & initialization
- Do not initialize static/global variables to `0` (compiler does it)
- Initialize pointers to `NULL` when no initial address
- Use C99 designated initializers for structs and arrays
- Declare local variables near first use (C99+), same-type locals on one line
- Trailing comma in struct initialization (helps clang-format)

### Control flow
- **Early return** for error conditions — avoid nesting deeper than 2 levels
- Omit `else` after a branch that returns
- Simple single-line `if` may omit braces; if any branch in an if-else chain uses braces, all must
- `switch`: `case` at same indent as `switch`; add `/* fallthrough */` comment when not breaking

### Functions
- Opening `{` on its own line (K&R function definition style)
- One space after each comma in parameter lists
- Use `restrict` judiciously

### Macros
- Parenthesize the entire body and each parameter usage
- Use `do { ... } while (0)` for multi-statement macros
- Never put `return` inside a macro
- Use each parameter at most once to avoid side effects

### const & static
- `static` for all module-private functions and variables
- `const` over `#define` for numeric constants
- Mark pointer parameters `const` if data is not modified

### Types
- `unsigned` for iterators, `size_t` for sizes, `ssize_t` for size-or-error
- `bool` (from `<stdbool.h>`) for boolean values — convert with relational operators, not casts
- Avoid fixed-width types (`uint8_t` etc.) for general iterators — use them for hardware, protocols, and memory-constrained contexts

### Portability
- Do not assume endianness, `long` size, or `char` signedness
- Avoid unaligned memory access
- Use `_Static_assert` to verify struct sizes when layout matters
- Use `UINT64_C()` / `PRIu64` macros for fixed-width constants and formatting

### Pointer NULL checks
- Both `if (!ptr)` and `if (ptr == NULL)` are acceptable — be consistent within a function

### Object abstraction
- Define struct in `.c`, expose only `typedef` in `.h` (opaque type)
- Separate public (`obj.h`) and private (`obj_impl.h`) headers when needed

## Formatting tool

```bash
clang-format -i *.{c,h}
```

Requires clang-format **v18+**. The repository `.clang-format` enforces these rules automatically.
