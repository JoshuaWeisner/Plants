import argparse
import os
import shutil

import requests
import tarfile
from tqdm import tqdm


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="download and extract all dataset images and annotations"
    )
    parser.add_argument(
        "--data-root",
        type=str,
        default="./data",
        help="directory for downloaded images and annotations",
    )
    parser.add_argument(
        "--skip",
        type=int,
        default=0,
        help="skip first n downloads, in case of interruption",
    )
    return parser.parse_args()


def setup(data_root, skip):
    url_prefix = "https://vitro-testing.com/wp-content/uploads/2022/12/"

    os.makedirs(data_root, exist_ok=True)

    for file_name in tqdm(
        [
            "cropandweed_annotations",
            "cropandweed_images1of4",
            "cropandweed_images2of4",
            "cropandweed_images3of4",
            "cropandweed_images4of4",
        ][skip:],
        desc="downloading and extracting files",
    ):
        response = requests.get(f"{url_prefix}{file_name}.tar", stream=True)
        length = int(response.headers.get("content-length", 0))
        with tqdm.wrapattr(
            response.raw, "read", total=length, desc=file_name
        ) as fileobj:
            archive = tarfile.open(fileobj=fileobj, mode="r|")
            archive.extractall(data_root, filter="data")

    shutil.move(
        os.path.join(data_root, "bboxes"), os.path.join(data_root, "CropAndWeed")
    )
    shutil.move(
        os.path.join(data_root, "CropAndWeed"),
        os.path.join(data_root, "bboxes", "CropAndWeed"),
    )

    for image_name in os.listdir("./images"):
        shutil.copy(
            os.path.join("./images", image_name),
            os.path.join(data_root, "images", image_name),
        )


def main():
    args = parse_arguments()
    setup(args.data_root, args.skip)


if __name__ == "__main__":
    main()
