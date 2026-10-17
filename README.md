# istand

A portable desk for those that want to stand and work, everywhere.

This repo holds the click-through concept deck for **iStand** and **iStand Pro**.

- `src/template.html`: slide source (18 slides)
- `build.py`: builds `dist/index.html` and `dist/vercel.json`
- `dist/`: the static site Vercel serves (images, vendored three.js r128)

## Edit and ship

```sh
OG_BASE=https://istand-deck.vercel.app python3 build.py
git commit -am "Update deck" && git push
```

Live at **https://istand-deck.vercel.app** (Vercel project `istand`).

For now, Vercel's GitHub app isn't installed on this account, so pushes don't deploy on their own. Deploys go through the Vercel connector instead: a small page on Vercel loads `dist/` from a pinned commit through jsDelivr. Once the app is installed, link the repo (root directory `dist`, no build step) and every push to `main` deploys.

Keys: arrow keys, click, or swipe to move between slides · `F` for fullscreen · `#13` deep-links to the 3D viewer.
