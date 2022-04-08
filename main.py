import csv
import json
import zipfile
from argparse import ArgumentParser
from os import mkdir, path, rename, walk
from secrets import token_hex
from shutil import copyfile, rmtree
from urllib.parse import quote_plus

SOURCE_PATH = "gitmoji/gitmojis.csv"
COLLECTION_NAME = "_gitmoji"


def build_json_files(source: str, destionation: str):
    fieldnames = ["name", "keyword", "content"]

    with open(f"{source}.csv", newline='', encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=fieldnames)
        for row in reader:
            uid = token_hex(15)
            output = json.dumps(
                {
                    "alfredsnippet": {
                        "snippet": row["content"],
                        "uid": uid,
                        "keyword": row["keyword"],
                        "name": row["name"],
                    },
                },
                sort_keys=False,
                indent=4,
                separators=(',', ': '),
            )
            output_file = destionation + "/" + quote_plus(row["name"] + " [" + uid + "].json")
            with open(output_file, "w") as f:
                f.write(output)


def zip_files(destination: str):
    with zipfile.ZipFile(destination + ".zip", "w") as zf:
        for root, _, files in walk(destination):
            for f in files:
                zf.write(
                    path.join(root, f),
                    f,
                    compress_type=zipfile.ZIP_DEFLATED,
                )


def change_zip_extension(destionation: str):
    renamee = destionation + ".zip"
    pre, _ = path.splitext(renamee)
    rename(renamee, pre + ".alfredsnippets")


def main(source: str, destination: str):
    mkdir(destionation)
    copyfile("./info.plist", "./" + destionation + "/info.plist")
    build_json_files(source, destionation)
    zip_files(destionation)
    change_zip_extension(destionation)
    rmtree(destionation)


if __name__ == "__main__":
    parser = ArgumentParser(description="CSV to Alfred Snippets")
    parser.add_argument("-s", "--source", help="Relative path of csv file", required=True)
    parser.add_argument("-d", "--destination", help="Relative path of output file", required=True)
    args = parser.parse_args()
    source, destionation = args.source, args.destination
    main(source, destionation)
