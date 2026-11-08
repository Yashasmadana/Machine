# The Machine

A daily 20-minute interview workout for Linux kernel, embedded Linux and networking roles.

Each session:

1. **Concept of the day** (6 min): one topic in depth, with a diagram, what to say, interviewer follow-ups and wrong answers to avoid.
2. **Flashcards** (7 min): spaced repetition across 160 cards. Weak cards come back sooner.
3. **Code puzzle** (5 min): predict the output, find the bug, or write the function. C outputs verified with gcc on x86_64.
4. **News** (2 min): latest kernel releases from kernel.org and headlines from LWN.net, refreshed twice a day.

Progress (streak, card schedule) is saved in your browser. Use **Progress → Copy backup** to move it to another device.

## Files

| File | What it does |
|---|---|
| `index.html` | The site |
| `data/concepts.json` | 36 concepts, rotated one per completed session |
| `data/cards.json` | 160 flashcards |
| `data/puzzles.json` | 36 code puzzles |
| `news.json` | Kernel releases + LWN headlines (rewritten automatically) |
| `scripts/update_news.py` | Fetches the news |
| `.github/workflows/update-news.yml` | Runs at 6:20 AM and 6:20 PM IST |

## Set up on GitHub Pages

1. Create a new **public** repository called `the-machine`.
2. Add all files from this folder, including the hidden `.github` folder.
3. **Settings → Pages**: Deploy from a branch, `main`, `/ (root)`.
4. **Settings → Actions → General → Workflow permissions**: Read and write.
5. **Actions → Update kernel news → Run workflow**.

Open it at `https://<your-username>.github.io/the-machine/`. Opening `index.html` by double-clicking won't load the data files; use the GitHub Pages address.

## Adding content

Append objects to the JSON files in `data/` using the same fields. New concepts and puzzles join the rotation automatically; new cards enter as "new" cards.

## Keyboard

In flashcards: **Space** shows the answer, **1–4** rate it (Again, Hard, Good, Easy). Double-click the timer to reset it.
