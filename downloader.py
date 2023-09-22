import importlib

import torch

PREFIX = "./"


class StableDiffusionDownloader:
    def __init__(self, *, pipeline: str, model_id: str, variant: int = 32, device: str = "cuda"):
        self.model_id = model_id
        self.dtype = torch.float32 if variant == 32 else torch.float16
        self.diffusers_import = importlib.import_module("diffusers")
        self.pipeline = getattr(self.diffusers_import, pipeline)
        self.pipe = self.pipeline.from_pretrained(
            model_id,
            torch_dtype=self.dtype,
            variant="fp16",
        )
        self.pipe.to(device)

    def download_model(self):
        print(f"Downloading model {self.model_id}")
        model_path = f"{PREFIX}{self.model_id}"
        self.pipe.save_pretrained(save_directory=model_path)
        print(f"Model {model_path} downloaded")

    def generate_image(self, *, prompt: str):
        images = self.pipe(prompt=prompt).images
        if len(images) == 0:
            raise Exception("No images were generated")
        return images
