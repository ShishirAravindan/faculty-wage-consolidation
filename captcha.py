#!.finPayVenv/bin/python3

import base64
import requests
import logging
import argparse
from PIL import Image
import io
from argparse import Namespace
from typing import Any

def parse_arguments() -> Namespace:
    """
    Parse command line arguments for the DeCAPTCHA program.

    Returns:
        argparse.Namespace: An object containing the parsed arguments:\n
        - image_path: Path to the image file
        - target: Classification target
        - server_url: vLLM server URL
        - log_level: Logging level
        - prompt: Classification prompt for llava
    """
    parser = argparse.ArgumentParser(description="DeCAPTCHA")
    parser.add_argument("image_path", help="path to the image file")
    parser.add_argument("--target", help="classification target", required=True)
    parser.add_argument("--server_url", default="http://localhost:11434/api/generate", 
                        help="vLLM server URL")
    parser.add_argument("--log_level", default="INFO", help="logging level", 
                        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    parser.add_argument("--prompt", default="Respond with 1 if image has a {target}, else 0.", 
                        help="classification prompt for llava")
    return parser.parse_args()

def split_and_encode_image(image_path: str) -> list[str]:
    """
    Split the image into 9 equal parts and return base64 
    encoded strings for each part.
    """
    with Image.open(image_path) as img:
        width, height = img.size
        square_size = min(width, height) // 3
        
        # List to store base64 encoded image parts
        encoded_parts = []
        
        for i in range(3):
            for j in range(3):
                # Coordinates for cropping
                left = j * square_size
                top = i * square_size
                right = left + square_size
                bottom = top + square_size
                
                square = img.crop((left, top, right, bottom))
                
                buffer = io.BytesIO()
                square.save(buffer, format="PNG")
                base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
                
                encoded_parts.append(base64_image)
    return encoded_parts
    

def make_vLLM_API_call(prompt:str, image: str) -> Any[int, None]:
    """Make an API call to the vLLM server for image classification.

    Args:
        - `prompt` (str): The classification prompt to send to the server.
        - `image` (str): The base64-encoded image data.

    Returns:
        - str: The stripped response from the server if the call is successful.
        None: If the API call fails.

    Raises: `requests.exceptions.RequestException`: If there's an error in 
    making the HTTP request.

    Note: This function logs the API call status and any errors that occur.
    """
    DATA = {
        "model": "llava",
        "prompt": prompt,
        "stream": False,
        "images": [image]
    }
    URL = "http://localhost:11434/api/generate"
    response = requests.post(URL, json=DATA, timeout=200)
    logging.info("REQUEST SENT")
    if response.status_code == 200:
        return response.json()['response'].strip()
    else:
        logging.error(f"{response.status_code}, {response.text}")
    return

def process_images(prompt: str, images: list[str]):
    """
    Process a list of images using the vLLM API for classification.

    Args:
        - `prompt` (str): The classification prompt to be used for each image.
        - `images` (list): A list of base64-encoded image strings to be classified.

    Returns:
        list: A list of integer results (0 or 1) corresponding to each image's classification.

    Note:
        - The returned list may be shorter than the input list if some classifications fail.
    """
    results = []

    for image in images:
        classification = make_vLLM_API_call(prompt, image)

        if classification == '0' or classification == '1':
            results.append(int(classification))
            logging.info(f'Model\'s prediction: {classification}')
        else:
            logging.error(f'Model returned non-regular prediction: {classification}')
    return results


def main():
    args = parse_arguments()
    logging.basicConfig(level=getattr(logging, args.log_level.upper()), 
                        format="[%(levelname)s] %(message)s")
    
    # replace {target} with the target words
    args.prompt = args.prompt.replace("{target}", args.target)

    images = split_and_encode_image(args.image_path)
    logging.info("Images split and encoded")
    preds = process_images(args.prompt, images)

    logging.info('Classification complete')

    print(preds)
    return


if __name__ == "__main__":
    main()
    