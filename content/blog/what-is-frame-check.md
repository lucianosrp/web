+++
title = "What is Frame Check?"
date = "2026-05-11"
draft = false
[taxonomies]
tags = ["GitHub", "Python"]
+++

It all started at PyCon Hong Kong 2025 where I was asked if I had ideas for a sprint.
Back then, I'd had some experience contributing to Narwhals, which is a compatibility layer for dataframe libraries.
I'll cover Narwhals in a separate post, but briefly: it lets users write code in a single syntax (matching Polars' API) and makes it compatible with all major dataframe libraries (pandas, Polars, Dask, Spark, etc.) with no overhead. Around the same time, I was diving into Language Server Protocols (LSPs) and how they improve developer experience. This intersection of open source, dataframe libraries, and LSPs led me to build `frame-check`—a static checker for dataframes.



## Why the need for a static checker

If you're a regular Python developer, you're likely familiar with static type checkers like mypy or pyright. These tools catch type errors before runtime, making your code more reliable. Combined with LSPs, you get real-time feedback as you type, speeding up development. But type checking has limits. As code grows complex, we often fall back to runtime validation with libraries like Pydantic. I found myself wishing for the same column-level safety net for pandas DataFrames—something that catches errors the moment you type them. The open question was whether that's even possible without running the code. My hunch was that it is, because pandas code gives away more than you'd think.


## My intuition

Here's the observation the whole project rests on: even though Python is a dynamic language, most real-world pandas code is written in a surprisingly static style. Column names are almost always string literals. DataFrames are created from literal dictionaries or from `read_csv`-style calls whose arguments are right there in the source. Transformations are chains of well-known methods. We rarely compute column names at runtime—and when we do, it's the exception, not the rule.

That means most pandas code contains enough structural information to analyze it without running it. By tracking which columns (Series) are accessed, created, or removed, we can define an "ephemeral schema"—a snapshot of the DataFrame's shape at each point in the code—and flag illegal column access. While runtime checks add overhead and can sometimes slow code down, this kind of static analysis catches the same errors before execution, for free. Beyond that, we can flag potential typos and suggest column renames when we detect likely mistakes.

Note that I said *most* pandas code, not *all*. If a column name comes from user input or a computed variable, no static tool can know it—the same way mypy gives up on `Any`. That's fine: like type checkers, the goal is to be useful on the common case and stay quiet on the rest, not to prove your program correct.

To see how much information is actually sitting in the source, consider the following example:

```python
df['name_lower'] = df['Name'].str.lower()
df['age_group'] = df['Age'].apply(lambda x: 'adult' if x >= 18 else 'minor')
df['full_name'] = df['first_name'] + ' ' + df['last_name']
df['has_email'] = df['email'].notna()
```

By inspecting the code, we can trace each column's dependencies: 
- `name_lower` requires `Name`
- `age_group` requires `Age`
- `full_name` needs both `first_name` and `last_name`
- `has_email` depends on `email`

In our ephemeral schema, we map all column dependencies:
```
name_lower -> Name
age_group -> Age
full_name -> first_name, last_name
has_email -> email
```

We can ultimately go up the code and trace all dependencies. Something like:
```
name_lower
└── Name
    └── Source: df = pd.read_csv('users.csv')
age_group
└── Age
    └── Source: df = pd.read_csv('users.csv')
full_name
├── first_name
│   └── Source: df = pd.read_csv('users.csv')
└── last_name
    └── Source: df = pd.read_csv('users.csv')
has_email
└── email
    └── Source: df = pd.read_csv('users.csv')
```

The dataframe might have more columns, but we are only interested in the ones being used! Ultimately, without executing any code, we can already determine the dependencies between columns, and the initial and final states of the dataframe.


The dataframe should _at least_ have these columns:
- `Name`
- `Age`
- `first_name`
- `last_name`
- `email`


...and might end up with these additional columns:
- `name_lower`
- `age_group`
- `full_name`
- `has_email`

All of that from just reading the code. That was the intuition—now it needed to become a tool.

## How it works

The design follows directly from the intuition above: if the information is in the source, all we need to do is read the source carefully. frame-check doesn't run your code. It parses it into an Abstract Syntax Tree (AST) using Python's built-in `ast` module and walks it from top to bottom, the same way mypy or ruff do.

While walking the tree, a `Checker` keeps an eye out for a few things:

- **Imports** — is `pandas` imported, and under which alias?
- **DataFrame creation** — `pd.DataFrame({...})`, `pd.read_csv(...)`, `pd.read_parquet(...)` and friends. Each of these tells us the initial set of columns (or at least gives us a hint, like `usecols=` in `read_csv`).
- **Assignments** — `df["c"] = ...`, `df.assign(...)`, `df.rename(...)`, etc. These mutate the ephemeral schema.
- **Column access** — `df["customer_id"]`, and this is where the check happens: is that column in the schema at this point of the program?

A `Tracker` holds the ephemeral schema for each DataFrame variable as the walk progresses. When a column access doesn't match the schema, frame-check emits a diagnostic:

```plaintext
example.py:12:10: Column 'customer_id' does not exist on DataFrame 'df'.
   |
12 | result = df["customer_id"]
   |          ^^^^^^^^^^^^^^^^^
   |
   = available: Age, City, Name, Salary
```

The error message tells you not just *that* the column doesn't exist, but *what is* available — which makes typos immediately obvious. And since it's pure static analysis, there is zero runtime overhead: your code never executes.

Running this as a command-line tool is already useful, but the goal was never just another linter to add to CI. The goal was feedback *as you type*.

## Editor integration

Remember the LSP rabbit hole I mentioned at the beginning? This is where it pays off.

frame-check is split into a few components:

- **frame-check-core** — the actual checker: AST parsing, schema tracking, diagnostics.
- **frame-check-lsp** — a Language Server Protocol implementation that wraps the core.
- **frame-check-extensions** — editor-specific extensions (currently Zed).

The LSP is what turns frame-check from "a linter you run in CI" into "a red squiggle under `df['custmer_id']` the moment you type it". That instant feedback loop was the whole motivation: catching a `KeyError` in your editor is infinitely cheaper than catching it in production.

Getting the squiggle to show up turned out to be the easy part, though. The hard part is knowing what pandas actually does.

## Taming the pandas API

The hardest part of this project isn't the AST walking — it's the sheer size of the pandas API. There are a dozen ways to create a DataFrame, a dozen ways to assign a column, and countless methods that transform schemas (`groupby`, `merge`, `pivot`, ...).

To avoid drowning, we track every pandas behaviour as a feature with a stable ID. For example:

- `DCMS-1` — DataFrame creation from a dictionary of lists ✅
- `DCMS-6` — `pd.read_csv` (including `usecols`) ✅
- `CAM-1` — direct assignment `df["c"] = ...` ✅
- `CAM-9` — `df.insert(...)` ❌ (not yet!)

This registry drives the support tables in the [docs](https://frame-check.github.io/frame-check/) and the README, and gives contributors a well-scoped menu of things to pick up: "implement CAM-9" is a much friendlier first issue than "make pandas work". And friendly, well-scoped tasks matter, because frame-check was never meant to be a solo project.

## Back to the sprint

frame-check started as a sprint idea at PyCon Hong Kong 2025, and that origin shaped it more than anything else. The feature-ID system exists because sprints need small, self-contained tasks. The monorepo layout exists so someone can hack on the core without touching the LSP.

And it worked: since the first commit, around ten people have contributed — adding support for `read_excel`, `read_json`, `read_parquet`, `df.rename`, and more. Not bad for a project that started as an answer to "do you have ideas for a sprint?". So where does it go from here?

## What's next

frame-check is still young and unpolished — the README says so in bold letters. There's a long tail of pandas features to support, control flow to reason about (what happens to the schema inside an `if`?), and more editors to integrate.

If any of this sounds interesting, the project lives at [github.com/frame-check/frame-check](https://github.com/frame-check/frame-check). Pick a feature ID, and come catch some `KeyError`s before they happen.
