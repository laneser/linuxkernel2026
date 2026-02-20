# C Coding Style — Full Reference

> Source: [lab0-c CONTRIBUTING.md](https://github.com/sysprog21/lab0-c/blob/master/CONTRIBUTING.md)
> Style: K&R variant for Modern C

---

## Indentation

4 spaces, never tabs. Single space before/after comparison and assignment operators. Single space after every comma.

```c
for (int i = 0; i < 10; i++) {
    printf("%d\n", i);
    /* some operations */
}
```

## Line length

80 characters max. Wrap longer lines as needed.

## Comments

Multi-line:
```c
/*
 * This is a multi-line comment.
 */

/* One line comment. */
```

Inline (two spaces before):
```c
    return (uintptr_t) val;  /* return a bitfield */
```

Do not comment out code. Use `#if 0` ... `#endif` instead.

Searchable markers:
- `WARNING` — risk of changing this code
- `NOTE` — explains "why" rather than "how"
- `TODO` — area still under construction

## Spacing and brackets

Keywords (`if`, `while`, `for`, `switch`, `return`) followed by a space:
```c
do {
    /* some operations */
} while (condition);
```

Functions, `sizeof`, and macros — no space:
```c
unsigned total_len = offsetof(obj_t, items[n]);
unsigned obj_len = sizeof(obj_t);
```

Operators:
```c
/* Assignment and binary — spaces around */
count += 1;
current_conf = prev_conf | (1 << START_BIT);

/* Unary — no space */
bonus++;
if (!play)
    return STATE_QUITE;

/* Ternary — spaces around ? and : */
return (a > b) ? a : b;

/* Structure/member/array — no space */
obj->field;
arr[i];
```

## Parentheses

Use parentheses to clarify precedence, especially with `&&` and `||`:
```c
if ((count > 100) && (detected == false)) {
    character = C_ASSASSIN;
}
```

## Variable names

snake_case. No camelCase, no Hungarian notation. Descriptive globals, concise locals.

### Pointer declarations
```c
const char *name;                    /* pointer to const data */
conf_t * const cfg;                  /* const pointer */
const uint8_t * const charmap;       /* const pointer to const data */
const void * restrict key;           /* restrict pointer */
```

### Same-type locals on one line
```c
void func(void)
{
    char a, b;  /* OK */
}
```

### Trailing comma in struct init
```c
screen_t s = {
    .width = 640,
    .height = 480,   /* trailing comma */
};
```

## Type definitions

Typedef structs, not pointers. Suffix with `_t`. Struct name may be omitted within translation unit:
```c
typedef struct {
    unsigned if_index;
    unsigned addr_len;
    addr_t next_hop;
} route_info_t;
```

## Initialization

Do not initialize static/global to 0. Use C99 designated initializers:
```c
static const crypto_ops_t openssl_ops = {
    .create = openssl_crypto_create,
    .destroy = openssl_crypto_destroy,
    .encrypt = openssl_crypto_encrypt,
    .decrypt = openssl_crypto_decrypt,
    .hmac = openssl_crypto_hmac,
};
```

Initialize pointers to NULL. Declare local variables near first use (C99+).

## Control structures

### Early return (preferred)
```c
int inspect(obj_t *obj)
{
    if (!cond)
        return -1;

    /* Main logic here */
    ...
    return 0;
}
```

### Avoid redundant else
```c
/* Good */
if (flag & F_FEATURE_X) {
    ...
    return 0;
}
return -1;
```

### if statements — K&R style
```c
if (a == b) {
    ..
} else if (a < b) {
    ...
} else {
    ...
}
```

Simple one-line may omit braces:
```c
if (!valid)
    return -1;
```

If any branch uses braces, all branches must use braces.

Wrap long conditions with +4 indent:
```c
if (some_long_expression &&
        another_expression) {
    ...
}
```

### switch statements
```c
switch (expr) {
case A:
    ...
    break;
case B:
    /* fallthrough */
case C:
    ...
    break;
}
```

## Function definitions

Opening brace on its own line:
```c
ssize_t hex_write(FILE *stream, const void *buf, size_t len)
{
    ...
}
```

## Function-like macros

```c
#define SET_POINT(p, x, y)      \
    do {                        \
        (p)->px = (x);          \
        (p)->py = (y);          \
    } while (0)
```

Rules:
- Parenthesize body and each parameter
- `do-while(0)` for multi-statement
- Never put `return` in a macro
- Use each parameter at most once

## const and static

```c
/* static for module-private */
static bool verify_range(uint16_t x, uint16_t y);

/* const over #define */
const uint8_t max_skill_level = 100;

/* const pointer parameter */
static bool is_valid_cmd(const char *cmd);
```

## Object abstraction

Header (`obj.h`) — public, opaque:
```c
#ifndef _OBJ_H_
#define _OBJ_H_

typedef struct obj;

obj_t *obj_create(void);
void obj_destroy(obj_t *);

#endif
```

Source (`obj.c`) — private, full definition:
```c
#include "obj.h"

struct obj {
    int value;
};

obj_t *obj_create(void)
{
    return calloc(1, sizeof(obj_t));
}

void obj_destroy(obj_t *obj)
{
    free(obj);
}
```

## Types

- `unsigned` for iterators
- `size_t` for sizes, `ssize_t` for size-or-error
- `bool` for booleans (convert with relational operators, not casts)
- Avoid fixed-width types for general iterators

```c
#include <stdbool.h>
bool inside = (value < expected_range);
```

## Portability

Do not assume endianness, `long` size, or `char` signedness.

Use C99 macros for fixed-width constants and formatting:
```c
/* Good */
#define SOME_CONSTANT (UINT64_C(1) << 48)
printf("val %" PRIu64 "\n", SOME_CONSTANT);

/* Bad */
#define SOME_CONSTANT (1ULL << 48)
printf("val %lld\n", SOME_CONSTANT);
```

Verify struct layout:
```c
_Static_assert(sizeof(mytimer_t) == 8,
               "mytimer_t struct size incorrect (expected 8 bytes)");
```

Avoid unaligned access. Do not use bitwise operators on signed integers. Append `U` to unsigned `#define` constants.
