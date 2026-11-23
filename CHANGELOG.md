# Changelog

All notable changes to this project. Versions follow [docs/versioning.md](docs/versioning.md).

## [0.2.0] - 2026-11-23

### Changed
- New design. The page opens on one reader's bookshelf: their last liked books as spines on a dark wooden shelf, the hidden next book in gold, and each method's top 10 underneath with a hit marked in gold. The page opens on a sampled reader where at least one method found the book, and says so.
- The headline results are a row of short findings under the shelf instead of three tiles.
- Own look for this app: white page, walnut shelf, book-cloth colours, Work Sans with Crimson Pro for book titles.

### Added
- Decision record: open with one reader's shelf.

Data and results are unchanged.

## [0.1.0] - 2026-11-20

First release.

### Added
- Offline test on goodbooks-10k: each of 10,000 readers' most recent liked book hidden, 10 recommendations per method.
- Bestseller list, "readers also liked" and a taste profile model, run on the last 1, 3 and 10 liked books and on the whole history.
- Series analysis and a "next in series" rule.
- Results page with headline numbers, a history chart, a method table with series and variety, and a reader-by-reader view.
- Scripts that reproduce every number from a clean folder.
- Case study, product brief and three decision records.
