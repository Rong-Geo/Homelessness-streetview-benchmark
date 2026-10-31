"""Check a local copy of the benchmark and print per-split statistics.

Usage (from the repository root):
    python scripts/check_dataset.py            # uses ./data
    python scripts/check_dataset.py path/to/data

Only the Python standard library is required.
"""

import json
import sys
from collections import Counter
from pathlib import Path

EXPECTED = {"train": (754, 1015), "test": (501, 369)}  # (images, boxes)


def check_split(root: Path, split: str) -> bool:
    """Print statistics for one split and return True if it matches the release."""
    ann_path = root / split / "_annotations.coco.json"
    with open(ann_path, encoding="utf-8") as f:
        coco = json.load(f)

    names = {c["id"]: c["name"] for c in coco["categories"]}
    per_class = Counter(names[a["category_id"]] for a in coco["annotations"])
    missing = [im["file_name"] for im in coco["images"]
               if not (root / split / im["file_name"]).is_file()]
    sequences = {im.get("sequence") for im in coco["images"]}

    n_img, n_box = len(coco["images"]), len(coco["annotations"])
    print(f"[{split}] {n_img} images, {n_box} boxes, {len(sequences)} sequences, "
          f"{len(missing)} missing image files")
    for name, count in sorted(per_class.items()):
        print(f"    {name:<24} {count}")

    ok = (n_img, n_box) == EXPECTED[split] and not missing
    if not ok:
        print(f"    WARNING: expected {EXPECTED[split][0]} images and "
              f"{EXPECTED[split][1]} boxes with no missing files")
    return ok


def main() -> None:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data")
    results = [check_split(root, s) for s in ("train", "test")]
    print("OK: dataset is complete." if all(results) else "Dataset is incomplete.")
    sys.exit(0 if all(results) else 1)


if __name__ == "__main__":
    main()
