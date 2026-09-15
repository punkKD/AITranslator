from functions.cohereCall import *
metadata_prompt= """
1. The context of the text in the image (a signboard, menu, name, etc.): {image_context}
2. The country or region where the image was taken: {image_location}
3. The purpose of the translation (tourist, business, academic research, etc.): {image_purpose}

Please highlight the text in the image that is most relevant to the information above.

Things to note:
Do not include anything else in this prompt in the output. 
Only output the text and summarise necessary translator's notes.
"""
content_format= [
            {"type": "text",
              "text": metadata_prompt
              },
            {"type": "image_url",
            "image_url": {
              "url": "{image_url}",
              "detail": "{image_detail}" # Here's where we're setting the detail.
          }
        },
      ]
def detect_image(image_url: str, image_detail:str="low", image_context:str="General", 
                 image_location:str="Unknown", image_purpose:str="General"):
    content_format[1]["image_url"]["url"] = image_url  # Update the image URL in the content format
    content_format[1]["image_url"]["detail"] = image_detail  # Update the image detail in the content format
    response = co.chat(
        model="command-a-vision-07-2025",
        messages=[{"role": "user", "content": content_format}]
    )
    image_description = response.message.content[0].text
    return image_description

