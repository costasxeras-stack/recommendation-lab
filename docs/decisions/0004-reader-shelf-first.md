# 0004: Open with one reader's shelf

**Status:** Accepted · 23 November 2026

## Context

Version 0.1.0 opened with three number tiles and put the reader examples at the bottom. It shared one visual template with the other portfolio apps, and the finding (start from the last few books) only showed up after reading a chart.

## Decision

Open with one reader's bookshelf. Their last liked books stand as spines, oldest on the left, and the hidden next book stands in gold at the end. Under the shelf, each method's top 10 is a row of title tags, and a hit turns gold. The page opens on the first sampled reader where at least one method found the book, and the line above the shelf says so, because a reader where every method misses does not show the difference between methods. "Show another reader" moves through all 40 sampled readers in order, hits and misses.

The app gets its own look: white page, dark walnut shelf, book-cloth colours, Work Sans, with Crimson Pro only for book titles.

## Consequences

- A visitor sees "last 3 books found it, whole history missed it" in one example before any number.
- Choosing the opening reader is a curation step. It is stated on the page so it is not mistaken for a typical result.
- On phones each method shows its first 5 picks, plus the hit if it is lower down.
