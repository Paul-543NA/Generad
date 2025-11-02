import os
import time
from openai import OpenAI
import dotenv
from PIL import Image
from io import BytesIO
from google import genai
from google.genai import types
import fal_client
from prompts import get_persona_generation_prompt, get_video_generation_prompt


def initialize_clients(openai_key, gemini_key, fal_key):
    """Initialize API clients with user-provided keys"""
    # Set FAL_KEY environment variable for fal_client
    os.environ["FAL_KEY"] = fal_key
    openai_client = OpenAI(api_key=openai_key)
    gemini_client = genai.Client(api_key=gemini_key)
    return openai_client, gemini_client


def get_image_bytes(image_path):
    image = Image.open(image_path)
    image_bytes = BytesIO()
    image.save(image_bytes, format="JPEG")
    return image_bytes.getvalue()


def generate_video(script_lines, first_frame_path, gemini_client, output_dir="."):
    """
    Generate a video from a script and first frame image.

    Args:
        script_lines: The video script text
        first_frame_path: Path to the first frame image
        gemini_client: Initialized Gemini client
        output_dir: Directory to save the output video (default: current directory)

    Returns:
        Path to the generated full video
    """
    # Try to extract content based on timestamps if available
    split_script_lines = script_lines.split("\n")
    first_half_text = ""
    second_half_text = ""
    for line in split_script_lines:
        if "[0:00" in line or "[0:02" in line or "[0:04" in line:
            first_half_text += line + " "
        elif "[0:06" in line or "[0:08" in line or "[0:09" in line:
            second_half_text += line + " "

    # Fallback: if no timestamps found, split by character count
    if not first_half_text or not second_half_text:
        mid_point = len(script_lines) // 2
        first_half_text = script_lines[:mid_point]
        second_half_text = script_lines[mid_point:]

    first_half_prompt = f"First 8 seconds of UGC video: {first_half_text[:500]} DO NOT OVERLAY CAPTIONS ON THE VIDEO"
    second_half_prompt = f"Next 8 seconds continuing the UGC video: {second_half_text[:500]} DO NOT OVERLAY CAPTIONS ON THE VIDEO"

    # Creaate first image structure for Gemini Files API
    # Define the mime type
    if "jpg" in first_frame_path:
        mime_type = "image/jpeg"
    elif "png" in first_frame_path:
        mime_type = "image/png"
    else:
        mime_type = "image/jpeg"

    first_frame_dict = {
        "mimeType": mime_type,
        # Get the next one with PIL
        "image_bytes": get_image_bytes(first_frame_path),
    }

    operation = gemini_client.models.generate_videos(
        model="veo-3.1-fast-generate-preview",
        prompt=first_half_prompt,
        image=first_frame_dict,
        config=types.GenerateVideosConfig(
            aspect_ratio="9:16", resolution="720p", duration_seconds=8
        ),
    )
    print("Waiting for first half video generation to complete...")

    # Poll the operation status until the video is ready
    while not operation.done:
        print("  Still generating...")
        time.sleep(10)
        operation = gemini_client.operations.get(operation)

    # Download the generated video
    generated_video_first_half = operation.response.generated_videos[0]
    first_half_video_path = os.path.join(output_dir, "first_half.mp4")
    gemini_client.files.download(file=generated_video_first_half.video)
    generated_video_first_half.video.save(first_half_video_path)
    print(f"First half video saved to {first_half_video_path}")

    # Generating second half of video
    operation = gemini_client.models.generate_videos(
        model="veo-3.1-generate-preview",
        video=generated_video_first_half.video,
        prompt=second_half_prompt,
        config=types.GenerateVideosConfig(
            number_of_videos=1, resolution="720p", aspect_ratio="9:16"
        ),
    )

    print("Waiting for video extension to complete...")
    while not operation.done:
        print("  Still extending...")
        time.sleep(10)
        operation = gemini_client.operations.get(operation)

    # Download the extended video
    generated_video_full = operation.response.generated_videos[0]
    full_video_path = os.path.join(output_dir, "full_ugc_ad.mp4")
    gemini_client.files.download(file=generated_video_full.video)
    generated_video_full.video.save(full_video_path)
    print(f"Full UGC ad video saved to {full_video_path}")

    print("\n✅ Video generation pipeline completed successfully!")
    print(f"Final video: {full_video_path}")

    return full_video_path


def generate_persona_profile(product_name, product_description, openai_client):
    """
    Generate an AI persona profile for the product.

    Args:
        product_name: Name of the product
        product_description: Description of the product
        openai_client: Initialized OpenAI client

    Returns:
        The generated persona profile text
    """
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": get_persona_generation_prompt(
                    product_name, product_description
                ),
            }
        ],
    )
    return response.choices[0].message.content


def upload_product_image(product_image_pil, temp_path="temp_product.png"):
    """
    Upload product image to fal.ai and return the URL.

    Args:
        product_image_pil: PIL Image object of the product
        temp_path: Temporary file path to save the image

    Returns:
        URL of the uploaded product image
    """
    product_image_pil.save(temp_path)
    product_image_url = fal_client.upload_file(temp_path)
    return product_image_url


def generate_creator_image(persona_profile, fal_key):
    """
    Generate a creator image based on the persona profile.

    Args:
        persona_profile: The generated persona profile text
        fal_key: Fal.ai API key

    Returns:
        URL of the generated creator image
    """
    # Set FAL_KEY environment variable for fal_client
    os.environ["FAL_KEY"] = fal_key

    result_creator_image = fal_client.subscribe(
        "fal-ai/nano-banana",
        arguments={
            "prompt": f"""
                        Create a photorealistic 9:16 iPhone camera selfie of the creator described below.
                        Use natural lighting and realistic depth of field. Ensure the product is clearly visible and in the creator's hand.

                        Creator description:
                        {persona_profile}
                        """,
            "aspect_ratio": "9:16",
        },
        with_logs=True,
    )
    return result_creator_image["images"][0]["url"]


def generate_first_frame(creator_image_url, product_image_url, fal_key):
    """
    Generate the first frame showing creator holding the product.

    Args:
        creator_image_url: URL of the creator image
        product_image_url: URL of the product image
        fal_key: Fal.ai API key

    Returns:
        URL of the generated first frame image
    """
    # Set FAL_KEY environment variable for fal_client
    os.environ["FAL_KEY"] = fal_key

    result_first_frame = fal_client.subscribe(
        "fal-ai/nano-banana/edit",
        arguments={
            "prompt": """
                        Create a photorealistic 9:16 iPhone camera selfie of the creator in the first image holding the product from the second image.
                        Use natural lighting and realistic depth of field. Ensure the product is clearly visible and in the creator's hand.
                        """,
            "image_urls": [creator_image_url, product_image_url],
            "aspect_ratio": "9:16",
        },
        with_logs=True,
    )
    return result_first_frame["images"][0]["url"]


def generate_video_script(
    product_name, product_description, persona_profile, openai_client
):
    """
    Generate a video script based on the product and persona.

    Args:
        product_name: Name of the product
        product_description: Description of the product
        persona_profile: The generated persona profile text
        openai_client: Initialized OpenAI client

    Returns:
        The generated video script text
    """
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": get_video_generation_prompt(
                    product_name, product_description, persona_profile
                ),
            }
        ],
    )
    return response.choices[0].message.content
