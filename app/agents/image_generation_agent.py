from openai import OpenAI
import os
from typing import Dict


class ImageGenerationAgent:

    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

    async def generate(self, payload: Dict):
        """
        payload expects:
        {
            "prompt": str,
            "size": "1024x1024"
        }
        """

        prompt = payload["prompt"]
        size = payload.get("size", "1024x1024")

        try:
            response = self.client.images.generate(
                model="gpt-image-1",
                prompt=prompt,
                size=size
            )

            image_url = response.data[0].url

            return {
                "image_url": image_url,
                "prompt_used": prompt,
                "model": "gpt-image-1",
                "size": size
            }

        except Exception as e:
            return {
                "error": "Image generation failed",
                "details": str(e)
            }

