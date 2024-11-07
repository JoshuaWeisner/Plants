import argparse
from ultralytics import YOLO
from pathlib import Path


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="transform the dataset bounding box format so it can be used by yolo"
    )
    parser.add_argument(
        "--weights",
        type=str,
        default="./runs/detect/train/weights/best.pt",
        help="location of model weights file",
    )
    parser.add_argument(
        "--image",
        type=str,
        required=True,
        help="image to run the detection on",
    )
    parser.add_argument(
        "--out",
        type=str,
        required=False,
        help="location to save the result",
    )
    parser.add_argument(
        "--confidence",
        type=float,
        default=0.7,
        help="required confidence for object detections",
    )
    parser.add_argument(
        "--split",
        action="store_true",
        help="splits the image into one file per object (if --out)",
    )
    return parser.parse_args()


def run(weights: str, image: str, out: str | None, confidence: float, split: bool):
    model = YOLO(weights)
    result = model.predict(image, conf=confidence)[0]

    if out:
        if split:
            result.save_crop(out, file_name=Path("img"))
        else:
            result.save(out)
    else:
        result.show()


def main():
    args = parse_arguments()
    run(args.weights, args.image, args.out, args.confidence, args.split)


if __name__ == "__main__":
    main()
