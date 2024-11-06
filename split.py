import argparse
import os
import random

from tqdm import tqdm
from shutil import copy2 as fcopy
from enum import Enum

SRC_IMAGES = "images"
OUT_IMAGES = "images"
SRC_BBOXES = "bboxesYolo"
OUT_BBOXES = "labels"


class OutDir(Enum):
    TRAIN = "train"
    VAL = "val"
    TEST = "test"


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="transform the dataset bounding box format so it can be used by yolo"
    )
    parser.add_argument(
        "--data-root",
        type=str,
        default="./data",
        help="directory of images and annotations",
    )
    parser.add_argument(
        "--ratio",
        type=str,
        default="70/30",
        help="proportions of train/val/test (if make-tests) for the dataset",
    )
    parser.add_argument(
        "--seed",
        type=str,
        default="0",
        help="seed for random choices, not seeded if 'none'",
    )
    parser.add_argument(
        "--make-tests",
        action="store_true",
        help="put some images in the testing dir",
    )
    return parser.parse_args()


def seed(seed_str: str):
    if seed_str.lower() != "none":
        random.seed(seed_str.encode())


def get_dist(ratio: str, make_tests: bool):
    try:
        raw = [float(n) for n in ratio.strip().split("/")]
    except:
        print(
            f"invalid ratio input '{ratio}', should be numbers separated by '/' such as '70/30'"
        )
        exit(1)
    count = 2
    if make_tests:
        count = 3
    if len(raw) < count:
        print(f"too few parts in ratio input, needs {count}")
        exit(1)
    raw = raw[:count]
    tot = sum(raw)
    return [n / tot for n in raw]


def copy_file(
    bbox_file: str, data_root: str, images_dir: str, bboxes_dir: str, out_dir: OutDir
):
    out_root = os.path.join(data_root, out_dir.value)
    out_bbox_dir = os.path.join(out_root, OUT_BBOXES)
    out_img_dir = os.path.join(out_root, OUT_IMAGES)

    img_file = bbox_file.replace(".txt", ".jpg")
    fcopy(os.path.join(bboxes_dir, bbox_file), out_bbox_dir)
    fcopy(os.path.join(images_dir, img_file), out_img_dir)


def split(data_root: str, dist: list[float], make_tests: bool):
    data_root = os.path.realpath(data_root)
    images = os.path.join(data_root, SRC_IMAGES)
    bboxes = os.path.join(data_root, SRC_BBOXES)

    for dest in OutDir:
        for out_type in [OUT_IMAGES, OUT_BBOXES]:
            os.makedirs(os.path.join(data_root, dest.value, out_type), exist_ok=True)

    # every bbox should have a corresponding image, verified by transform.py
    files = os.listdir(bboxes)
    count = len(files)
    remaining = count

    if make_tests:
        test_count = int(count * dist[2])
        remaining -= test_count
        tests = random.sample(files, test_count)
        for test in tqdm(tests, desc="copying testing data"):
            files.remove(test)
            copy_file(test, data_root, images, bboxes, OutDir.TEST)

    val_count = int(count * dist[1])
    remaining -= val_count
    vals = random.sample(files, val_count)
    for val in tqdm(vals, desc="copying validation data"):
        files.remove(val)
        copy_file(val, data_root, images, bboxes, OutDir.VAL)

    trains = random.sample(files, remaining)
    for train in tqdm(trains, desc="copying training data"):
        files.remove(train)
        copy_file(train, data_root, images, bboxes, OutDir.TRAIN)


def main():
    args = parse_arguments()
    seed(args.seed)
    dist = get_dist(args.ratio, args.make_tests)
    split(args.data_root, dist, args.make_tests)


if __name__ == "__main__":
    main()
