import os
from glob import glob
from pathlib import Path
from typing import Any

import boto3
import tqdm

AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""
MODELS_BUCKET = ""
PREFIX = "./"


class StableDiffusionUploader:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )

    def upload_model_to_s3(self, *, output_path: str) -> None:
        print("Uploading model to the S3 bucket")
        print("Uploading model to the S3 bucket")
        output_path = f"{PREFIX}{output_path}/**/*"
        print("output_path", output_path)
        list_of_content = glob(output_path, recursive=True)
        list_of_files = [file for file in list_of_content if Path(file).is_file()]
        print("list_of_files", list_of_files)
        self.upload_files(list_of_files)
        print("Model uploaded to the S3 bucket")

    def upload_file(self, file: str):
        file_size = os.stat(file).st_size
        filename = file.removeprefix(PREFIX)
        print(f"Uploading {filename} to S3")
        with tqdm.tqdm(total=file_size, unit="B", unit_scale=True, desc=file) as pbar:
            self.s3.upload_file(
                Filename=file,
                Bucket=MODELS_BUCKET,
                Key=filename,
                Callback=lambda bytes_transferred: pbar.update(bytes_transferred),
            )

    def upload_files(self, files: list[Any]):
        for file in files:
            self.upload_file(file)
