from image_encoder import encode_image
import anthropic
from PIL import Image

api_k = "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"


def analyze_image(image_encoded, prompt):
    client = anthropic.Anthropic(api_key=api_k)
    media_type = "image/jpeg"

    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_encoded,
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ],
            }
        ],
    )
    return message.content[0].text
