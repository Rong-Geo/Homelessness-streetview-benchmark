# Homelessness Street-View Benchmark (San Diego dashcam frames)

Object-detection benchmark of vehicle-mounted street-view video frames from downtown San Diego, California, annotated with bounding boxes and persistent track identifiers for visible indicators of unsheltered homelessness.

This is the dataset released with the paper:

> X. Du\*, R. Li\*, S. Paila, M.-H. Tsou, X. Liu. **Scalable Privacy-Preserving Urban Unsheltered Homelessness Surveying Using Street-View Video and Imagery.** Submitted to *Scientific Reports*. (\* equal contribution)

All video and images were recorded by the authors with forward-facing cameras in a passenger vehicle between November 2025 and January 2026. No images come from Google Street View, Mapillary, BDD100K, or any other third-party dataset. "Street-view video" in the paper title means these author-collected recordings.

## At a glance

| | |
| :-- | :-- |
| Images | 1,255 JPEG frames from 18 video sequences |
| Boxes | 1,384 bounding boxes, each with a `track_id` |
| Classes | 4 (encampments, shopping carts, two pedestrian classes) |
| Splits | `train` (754 images) / `test` (501 images), split by time within each sequence |
| Format | COCO detection JSON, one file per split |
| Resolution | 1920×1080 (1,136 images) and 3840×2160 (119 images) |
| Size | about 810 MB |

## Download

**Option 1: ZIP (no tools needed).** Click the green **Code** button at the top of this page, then **Download ZIP**. Unzip it; the data is in `data/`.

**Option 2: git clone.**

```bash
git clone https://github.com/Rong-Geo/homelessness-streetview-benchmark.git
cd homelessness-streetview-benchmark
```

**Option 3: download only one split** (for example, only `test`):

```bash
git clone --filter=blob:none --sparse https://github.com/Rong-Geo/homelessness-streetview-benchmark.git
cd homelessness-streetview-benchmark
git sparse-checkout set data/test
```

**Check the download** (Python 3, standard library only):

```bash
python scripts/check_dataset.py
```

Expected last line: `OK: dataset is complete.`

## Folder structure

```
homelessness-streetview-benchmark/
├── README.md
├── LICENSE
├── CITATION.cff
├── scripts/
│   └── check_dataset.py           # verifies image counts, box counts, missing files
└── data/
    ├── train/
    │   ├── _annotations.coco.json # COCO annotations for the 754 train images
    │   └── *.jpg
    └── test/
        ├── _annotations.coco.json # COCO annotations for the 501 test images
        └── *.jpg
```

## Classes

The annotation files use the release names in the first column. The paper uses the names in the second column.

| `category_id` | Name in JSON | Name in paper | train boxes | test boxes |
| ----: | :-- | :-- | ----: | ----: |
| 1 | `Homeless_People` | Pedestrian-II (unhoused person on the street) | 334 | 112 |
| 2 | `Homeless_Encampments` | Encampments | 355 | 117 |
| 3 | `Homeless_Homeless Cart` | Shopping cart | 180 | 82 |
| 4 | `pedestrian` | Pedestrian-I (other pedestrian) | 146 | 58 |

## Statistics

| Split | Images | Images with ≥1 box | Boxes |
| :-- | ----: | ----: | ----: |
| train | 754 | 427 | 1,015 |
| test | 501 | 189 | 369 |
| total | 1,255 | 616 | 1,384 |

Images without boxes are kept on purpose as negative (background) frames.

## Train/test split

Each of the 18 sequences is split **by time**: the first ~60% of its frames are in `train` and the remaining ~40% are in `test`. Within every sequence, all train frames come before all test frames.

Both splits therefore cover the same 18 scenes. The test set measures generalization to later moments of scenes seen in training, **not** to new locations or new videos. Frames were not split at random because neighboring frames are nearly identical, and a random split would place near-duplicates in both splits.

To reproduce the paper's results, use the splits exactly as provided.

## File naming

```
<sequence>__<original_filename>.jpg
e.g. 20251110_145602_seq000__20251110_145602_f0000.jpg
```

- `<sequence>`: source video plus segment index (e.g. `20251110_145602_seq000`)
- `fNNNN`: frame index within the source video

## Annotation format (COCO)

Each `_annotations.coco.json` follows the standard COCO detection format:

- `images[]`: `id`, `file_name`, `width`, `height`, plus `sequence` and `original_filename`
- `annotations[]`: `id`, `image_id`, `category_id`, `bbox` = `[x, y, width, height]` in absolute pixels (top-left origin), `area`, `iscrowd` (always 0), `segmentation` (empty), plus:
  - `track_id`: object identity, consistent across frames within a sequence (used by the paper's temporal-consistency regularizer)
  - `occluded`: occlusion flag (0 for every box in this release)
- `categories[]`: the 4 classes above

Image and annotation `id`s are unique only within one split's JSON file.

Standard COCO tools (pycocotools, Detectron2, MMDetection, RF-DETR, Ultralytics converters, etc.) read these files directly and ignore the extra fields.

## Quick start

```python
# pip install pycocotools
from pycocotools.coco import COCO

coco = COCO("data/train/_annotations.coco.json")
print(len(coco.getImgIds()), "images,", len(coco.getAnnIds()), "boxes")

# All boxes of one tracked object across frames
anns = coco.loadAnns(coco.getAnnIds())
track = [a for a in anns if a["track_id"] == anns[0]["track_id"]]
print(len(track), "boxes share track_id", anns[0]["track_id"])
```

## What is not included

The original full-length videos, exact GPS tracks, and potentially identifying metadata are not public because they may contain personally identifiable and sensitive location information. Subject to institutional approval and a data-use agreement, restricted materials may be made available to qualified researchers on reasonable request to the corresponding author (xiaobai.liu@sdsu.edu). Training code, model configurations, and evaluation scripts will be added before publication.

## Responsible use

The frames show people in public spaces, some of whom may be experiencing homelessness. Use this dataset only for research on aggregate, privacy-preserving measurement of urban conditions. Do not use it to identify, re-identify, track, or profile individuals, and do not combine it with other data for that purpose.

## License

The dataset is released under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/); see `LICENSE`. Please cite the paper when you use it.

## Citation

```bibtex
@article{du2026homelessness,
  title   = {Scalable Privacy-Preserving Urban Unsheltered Homelessness Surveying Using Street-View Video and Imagery},
  author  = {Du, Xinyu and Li, Rong and Paila, Sumanth and Tsou, Ming-Hsiang and Liu, Xiaobai},
  journal = {Scientific Reports},
  note    = {Under review},
  year    = {2026}
}
```

## Acknowledgement

This work was partially supported by the U.S. National Science Foundation under Grant No. 2417568.

## Contact

Xiaobai Liu, San Diego State University — xiaobai.liu@sdsu.edu
