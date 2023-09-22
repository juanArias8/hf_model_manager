import logging

from downloader import StableDiffusionDownloader
from uploader import StableDiffusionUploader

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    pipeline = "StableDiffusionXLImg2ImgPipeline"
    model_id = "stabilityai/stable-diffusion-xl-refiner-1.0"
    variant = 32
    prompt = "Astronaut in a jungle, cold color palette, muted colors, detailed, 8k"

    downloader = StableDiffusionDownloader(
        pipeline=pipeline,
        model_id=model_id,
        variant=variant
    )
    downloader.download_model()
    uploader = StableDiffusionUploader()
    uploader.upload_model_to_s3(output_path=model_id)
    # image = downloader.generate_image(prompt=prompt)
