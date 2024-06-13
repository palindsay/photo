import os
import argparse
from PIL import Image
import torch
from torch import autocast
from diffusers import StableDiffusionRefinePipeline, RealESRGANPipeline

def process_images(input_dir):
    # Load the AI models
    real_esrgan_model = RealESRGANPipeline.from_pretrained("nateraw/real-esrgan-x4-plus", torch_dtype=torch.float16)
    denoise_model = StableDiffusionRefinePipeline.from_pretrained("isaiahcascardo/stable-diffusion-denoise", torch_dtype=torch.float16)

    # Process each image in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".png"):
            input_path = os.path.join(input_dir, filename)
            image = Image.open(input_path)

            # Apply super-resolution
            with autocast("cuda"):
                upscaled_image = real_esrgan_model(image)["sample"]

            # Apply denoising
            with autocast("cuda"):
                denoised_image = denoise_model(upscaled_image)["sample"]

            # Save the processed image
            output_path = os.path.join(input_dir, f"processed_{filename}")
            denoised_image.save(output_path)
            print(f"Processed image: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process images with AI")
    parser.add_argument("input_dir", help="Directory containing PNG images to process")
    args = parser.parse_args()

    process_images(args.input_dir)
