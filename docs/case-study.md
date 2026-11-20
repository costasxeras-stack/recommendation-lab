# Case study: Recommendation Lab

## The question

Does a personalised "readers also liked" beat a bestseller list, and what makes it work: the method, or the choices around it?

## Data

goodbooks-10k: 5,976,479 ratings (1 to 5 stars) from 53,424 readers on 10,000 popular books. Every reader has between 19 and 200 ratings. The dataset states that ratings are listed in time order.

## Approach

1. **The test.** For 10,000 random readers, the most recent book they rated 4 or 5 stars was hidden, together with everything they rated after it. Each method then had 10 recommendations to find it. Books the reader had already rated were never recommended.
2. **The methods.**
   - Bestseller list: the most liked books overall.
   - Readers also liked: for each book the reader liked, books liked by the same people (cosine similarity), added up.
   - Taste profile model: 64 hidden patterns learned from all likes (truncated SVD), matched to the reader's likes.
3. **How much history.** Each personalised method ran on the reader's last 1, 3 or 10 liked books and on their whole history.
4. **Series.** Book titles carry the series and number, for example "(The Hunger Games, #1)". 42% of the books are in a series. I counted how often the hidden book continues the series of the book liked just before, and tested a "next in series" rule.
5. **Measures.** Share of readers whose hidden book was in the top 10. Number of different books recommended across all readers. Share of recommendations from the 100 most liked books.

## Findings

### 1. Which books you start from matters more than the method (confirmed)

| History used | Readers also liked | Taste profile model | Bestseller list |
|---|---|---|---|
| Last 1 book | 20.0% | 8.8% | 1.9% |
| Last 3 books | 20.6% | 9.1% | 1.9% |
| Last 10 books | 16.3% | 8.5% | 1.9% |
| Whole history | 5.0% | 5.9% | 1.9% |

With the whole history, both personalised methods are about 3 times better than the bestseller list, and close to each other. From the last 3 liked books, "readers also liked" finds the next book 4 times as often.

### 2. Series explain part of it, not all (confirmed)

922 of the 10,000 hidden books (9%) continue the series of the book liked just before. "Readers also liked" from the last 3 books finds 97% of those. For the other 9,078 readers it still finds 12.8%, against 3.9% from the whole history.

### 3. A "next in series" rule adds nothing on top (confirmed)

The rule applies to 2,458 readers (the last liked book is in a series with unread later books) and is right for 764 of them (31%). Putting it in front of "readers also liked" from the last 3 books changes the hit rate from 20.6% to 20.6%: the similarity method already learns series from what people read together. A rule like this is still useful where there is little rating data, for example for new books.

### 4. Recent books bring variety (confirmed)

| Method | Different books recommended | Top-100 bestsellers in the top 10 |
|---|---|---|
| Bestseller list | 58 | 100% |
| Readers also liked, whole history | 2,448 | 73% |
| Readers also liked, last 3 books | 7,731 | 24% |

Adding up similarities over a long history favours books that are similar to everything, which are the bestsellers. Starting from a few recent books keeps the recommendations specific.

### 5. Part of the recency effect may come from how the data was entered (hypothesis)

The dataset says ratings are in time order, but not whether that is reading order or the order people typed in their ratings. Readers who rate many books in one session may enter them by series, author or shelf, which would make the last few books unusually close to the hidden one. A test with real reading dates would settle this.

## What I learned as a PM

- Before changing the algorithm, check its inputs. Here the starting books mattered more than the model.
- A simple rule (next in series) is a good baseline and a good fallback, even when it adds nothing to a strong method.
- Watch variety, not just hits. A method can score well and still show everyone the same bestsellers.
- State the data's weak point plainly. The time order here is the dataset's claim, not something I could check.

## Limits

- One dataset of popular books, and readers with at least 19 ratings. There are no truly new readers.
- One hidden book per reader. A hit means the book was in the top 10, not that the reader would have clicked it.
- Simple methods on purpose. Stronger models may close part of the gap between whole history and recent books.

## What I would do next

1. Repeat on a dataset with real reading dates, to test the recency effect.
2. Blend recent and long-term taste and find the best mix.
3. Test new readers with 0 to 2 liked books, where only the bestseller list and the series rule can help.

## My role

I framed the question, chose the test, the methods and the measures, and wrote the findings. Claude (Anthropic) wrote the code with me and ran the checks.
