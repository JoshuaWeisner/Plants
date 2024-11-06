import argparse
import os

from tqdm import tqdm

IMAGES_DIR = "images"
BBOXES_DIR = "bboxes/CropAndWeed"
BBOXES_OUT_DIR = "bboxesYolo"

IMG_WIDTH = 1088
IMG_HEIGHT = 1920


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
        "--use-labels",
        action="store_true",
        help="use labels for both crop (0) and weed (1)",
    )
    return parser.parse_args()


def transform_labels(csv_file: str, out_dir: str, use_label: bool):
    out_file = os.path.join(out_dir, os.path.basename(csv_file).replace(".csv", ".txt"))

    with open(out_file, "w") as out:
        with open(csv_file, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # discard stem positions
                # https://github.com/cropandweed/cropandweed-dataset?tab=readme-ov-file#annotation-format
                left, top, right, bottom, label, *_ = [int(n) for n in line.split(",")]
                width = right - left
                # positive y is lower in the image
                height = bottom - top
                x = (left + right) / 2
                y = (top + bottom) / 2
                width /= IMG_WIDTH
                x /= IMG_WIDTH
                height /= IMG_HEIGHT
                y /= IMG_HEIGHT
                if not use_label:
                    label = 0
                out.write(f"{label} {x:.6} {y:.6} {width:.6} {height:.6}\n")


def transform(data_root: str, use_labels: bool):
    data_root = os.path.realpath(data_root)
    images = os.path.join(data_root, IMAGES_DIR)
    bboxes = os.path.join(data_root, BBOXES_DIR)
    out = os.path.join(data_root, BBOXES_OUT_DIR)

    os.makedirs(out, exist_ok=True)

    # bbox_csv is without directory
    for bbox_csv in tqdm(os.listdir(bboxes), desc="processing bboxes"):
        matching_img = os.path.join(images, bbox_csv.replace(".csv", ".jpg"))
        if not os.path.exists(matching_img):
            print(f"warning: image {matching_img} not found in {images}")
            continue
        transform_labels(os.path.join(bboxes, bbox_csv), out, use_labels)


def main():
    args = parse_arguments()
    transform(args.data_root, args.use_labels)


if __name__ == "__main__":
    main()
