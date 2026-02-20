# The Seven Rules of a Great Git Commit Message

> Source: https://cbea.ms/git-commit/

1. **Separate subject from body with a blank line**
2. **Limit the subject line to 50 characters** (72 hard limit)
3. **Capitalize the subject line**
4. **Do not end the subject line with a period**
5. **Use the imperative mood in the subject line**
6. **Wrap the body at 72 characters**
7. **Use the body to explain _what_ and _why_ vs. _how_**

## Subject line test

A properly formed subject line should complete:

> "If applied, this commit will **your subject line here**"

Good:
- Refactor subsystem X for readability
- Update getting started documentation
- Remove deprecated methods

Bad:
- Fixed bug with Y _(past tense)_
- Changing behavior of X _(gerund)_
- More fixes for broken stuff _(vague)_
- fix: resolve null pointer crash _(conventional commit prefix)_
- Update qtest.c _(filename only)_
- Fix _(single word)_
- Implement `q_sort` function _(backticks in subject)_
- Add sorting (merge sort) _(parentheses in subject)_

## Body format

```
Summarize changes in around 50 characters or less

More detailed explanatory text, if necessary. Wrap it to about 72
characters or so. The blank line separating the summary from the
body is critical.

Explain the problem that this commit is solving. Focus on why you
are making this change as opposed to how (the code explains that).

 - Bullet points are okay, too

 - Typically a hyphen is used for the bullet, preceded by a single
   space, with blank lines in between

Close #123
See also: #456, #789
```
