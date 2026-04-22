"""
Data Collection Script — scrape images for 15 Malaysian food/product categories.
Run: python collect_data.py
"""

import os
import hashlib
from PIL import Image
from icrawler.builtin import BingImageCrawler

CATEGORIES = {
    "nasi_lemak": ["nasi lemak Malaysian food", "nasi lemak sambal"],
    "roti_canai": ["roti canai Malaysian", "roti canai flatbread"],
    "satay": ["Malaysian satay skewers", "satay chicken Malaysia"],
    "char_kuey_teow": ["char kuey teow Penang", "char kuey teow Malaysian"],
    "rendang": ["rendang beef Malaysian", "rendang daging"],
    "laksa": ["laksa Malaysian curry noodle", "laksa Penang"],
    "cendol": ["cendol dessert Malaysian", "cendol ais"],
    "milo": ["Milo drink Malaysia can", "Milo chocolate drink"],
    "maggi_mee": ["Maggi mee goreng Malaysian", "Maggi instant noodle Malaysia"],
    "boh_tea": ["Boh tea Malaysia", "Boh tea box package"],
    "kaya_toast": ["kaya toast Malaysian", "kaya toast breakfast"],
    "teh_tarik": ["teh tarik Malaysian", "teh tarik pulled tea"],
    "pisang_goreng": ["pisang goreng Malaysian", "pisang goreng fried banana"],
    "kuih_lapis": ["kuih lapis Malaysian", "kuih lapis layer cake"],
    "nasi_kandar": ["nasi kandar Penang", "nasi kandar Malaysian"],
}

OUTPUT_DIR = "data/raw"
MAX_PER_CATEGORY = 3000  # scrape extra, manually prune to >=100


def dedup_folder(folder):
    """Remove duplicate images by file hash."""
    seen = set()
    removed = 0
    for fname in os.listdir(folder):
        fpath = os.path.join(folder, fname)
        if not fname.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            continue
        try:
            with open(fpath, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
            if file_hash in seen:
                os.remove(fpath)
                removed += 1
            else:
                seen.add(file_hash)
        except Exception:
            os.remove(fpath)  # corrupted file
            removed += 1
    return removed


def remove_corrupted(folder):
    """Remove images that can't be opened by PIL."""
    removed = 0
    for fname in os.listdir(folder):
        fpath = os.path.join(folder, fname)
        if not fname.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            continue
        try:
            img = Image.open(fpath)
            img.verify()
        except Exception:
            os.remove(fpath)
            removed += 1
    return removed


def collect():
    for category, queries in CATEGORIES.items():
        cat_dir = os.path.join(OUTPUT_DIR, category)
        os.makedirs(cat_dir, exist_ok=True)

        existing = len([f for f in os.listdir(cat_dir)
                       if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        if existing >= MAX_PER_CATEGORY:
            print(f"[SKIP] {category}: {existing} images")
            continue

        print(f"\n[COLLECTING] {category} ({existing} existing)")
        for query in queries:
            crawler = BingImageCrawler(
                storage={"root_dir": cat_dir},
                feeder_threads=2, parser_threads=2, downloader_threads=4,
            )
            crawler.crawl(keyword=query, max_num=160, min_size=(200, 200),
                         file_idx_offset="auto")

        # Clean up: remove corrupted + duplicates
        n_corrupt = remove_corrupted(cat_dir)
        n_dupes = dedup_folder(cat_dir)
        final = len([f for f in os.listdir(cat_dir)
                    if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))])
        print(f"[DONE] {category}: {final} images (removed {n_corrupt} corrupted, {n_dupes} duplicates)")


def verify():
    print("\n" + "=" * 50)
    print("Dataset Summary")
    print("=" * 50)
    total = 0
    for cat in sorted(CATEGORIES):
        cat_dir = os.path.join(OUTPUT_DIR, cat)
        count = len([f for f in os.listdir(cat_dir)
                    if f.lower().endswith(('.jpg', '.jpeg', '.png'))]) if os.path.exists(cat_dir) else 0
        status = "OK" if count >= 100 else "NEED MORE"
        print(f"  {cat:<20s}: {count:>4d}  [{status}]")
        total += count
    print(f"\n  Total: {total} | Avg: {total/len(CATEGORIES):.0f}")


if __name__ == "__main__":
    collect()
    verify()