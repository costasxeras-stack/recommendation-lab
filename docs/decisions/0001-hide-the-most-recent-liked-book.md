# 0001: Hide each reader's most recent liked book, not a random one

**Status:** accepted, 0.1.0

## Context

An offline test needs a book to hide and try to recommend. Hiding a random book lets the method use books the reader rated later, which is not what a live feature can do.

## Decision

Hide the most recent book rated 4 or 5 stars, and everything rated after it, using the order the dataset gives (it states that ratings are in time order). Methods see only what came before.

## Tradeoff

- This mirrors "what will they want next", which is the real product question.
- It depends on the dataset's time order, which I could not check. If the order reflects how ratings were typed in rather than read, recent books may look more predictive than they are. The case study states this as the main caveat.
