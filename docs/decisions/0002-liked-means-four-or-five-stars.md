# 0002: "Liked" means 4 or 5 stars, and any rated book counts as read

**Status:** accepted, 0.1.0

## Context

Ratings go from 1 to 5. A recommender needs to know what the reader liked, and must not recommend books they have already read.

## Decision

Build the similarity and taste profile from 4 and 5 star ratings only (69% of all ratings). Treat every rated book, at any star level, as read, and never recommend it.

## Tradeoff

- Ignoring 1 to 3 star ratings throws away some signal about what readers dislike.
- It keeps the methods simple and the test clear: the hidden book is one the reader liked.
