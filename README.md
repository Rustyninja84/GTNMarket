# Star Forge GTN Market Watch

A fan-made, static SWTOR Star Forge GTN material-price tracker for GitHub Pages.

## Publish on GitHub Pages
1. Create a new **public** GitHub repository, e.g. `star-forge-gtn-watch`.
2. Upload `index.html` to the repository root and commit.
3. In the repository go to **Settings → Pages**.
4. Under **Build and deployment**, choose **Deploy from a branch**, branch `main`, folder `/ (root)`, then Save.
5. Visit `https://YOUR-USERNAME.github.io/star-forge-gtn-watch/` after deployment finishes.

## How it works
- Record observed GTN *unit asking prices* for items, including the observation time.
- The dashboard shows the latest observation, median of recorded asking prices, a heuristic price-position signal, and a price-history chart.
- SELL: latest price >= 115% of median, after at least three observations.
- FARM: latest price <= 85% of median, after at least three observations.
- HOLD: everything else. These are **not** evidence of actual demand or sales.
- The calculator estimates credits per hour based on user-entered farming rate, price, fees and costs.
- Export/import JSON for backups and transferring between browsers.

## Important limitations
- This is **not** a live SWTOR GTN scraper or connected API. GitHub Pages alone cannot query the in-game GTN.
- Entries are saved only in your current browser's `localStorage`; they do not automatically sync across devices or other users.
- Prices are listing observations, not completed sales, and recommendations are only simple heuristics.
- No server-side price alerts, automatic scraping, or push notifications are included.
- Fan project, not affiliated with EA, BioWare, or Lucasfilm.
