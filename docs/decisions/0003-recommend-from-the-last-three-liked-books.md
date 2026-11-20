# 0003: Start recommendations from the last 3 liked books

**Status:** proposed for a live test, based on the 0.1.0 results

## Context

"Readers also liked" from the whole history found the hidden book for 5.0% of readers. From the last 3 liked books it found it for 20.6%, with far more variety (7,731 different books against 2,448). The last book alone gave 20.0%, and the last 10 gave 16.3%.

## Decision

If this were a live feature, start "readers also liked" from the reader's last 3 liked books, and test it against the whole-history version.

## Tradeoff

- Three books is a little better than one and less exposed to a single unusual pick.
- Recent books can over-focus on a short phase, such as one series. A blend with long-term taste is the next thing to test.
- The offline result depends on the dataset's time order (decision 0001), so a live test is needed before relying on it.
