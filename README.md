# RGB+A Robot Perception

Project page for **RGB+A Robot Perception: Using Acoustic-Video Perception for Robot Manipulation with Occluded Contact Dynamics**.

Published at <https://rgba-robot.github.io/>.

## Structure

```
.
├── index.html               # main project page
└── static/
    ├── css/style.css        # all styles
    ├── js/                  # (reserved for future scripts)
    ├── videos/              # drop mp4s here (see filenames referenced in index.html)
    └── images/              # posters, diagrams, spectrograms
```

## Adding videos

The page references these files under `static/videos/`. Drop MP4s in with matching names and they will appear automatically:

| Section | File |
| --- | --- |
| Teaser | `teaser.mp4` |
| Motivation | `occluded_pushing.mp4`, `occluded_threading.mp4`, `occluded_generic.mp4` |
| Setup | `setup.mp4` |
| Tasks | `task_threading.mp4`, `task_grinding.mp4`, `task_peeling.mp4`, `task_boxopen.mp4`, `task_cleaning.mp4` |
| Baselines | `baseline_vision.mp4`, `ours_rgba.mp4` |
| Attention | `attn_threading.mp4`, `attn_peeling.mp4`, `attn_cleaning.mp4` |
| Failures | `fail_cleaning.mp4`, `fail_boxcut.mp4` |

Images referenced under `static/images/`:

- `teaser_poster.jpg` — teaser video poster frame
- `spectrogram_prior.png` — prior-work spectrogram illustration
- `beamforming.svg` — beamforming diagram
- `method_history.svg`, `method_attention.svg` — method architecture diagrams

## Local preview

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

## Deploy (GitHub Pages)

Pushing to `main` on the `rgba-robot/rgba-robot.github.io` repo publishes automatically.
