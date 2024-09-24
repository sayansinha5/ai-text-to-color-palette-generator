from flask import Flask, render_template, request
import openai
import json
from dotenv import dotenv_values

config = dotenv_values(".env")
openai.api_key = config["OPENAI_API_KEY"]

app = Flask(
   __name__,
   template_folder='templates',
   static_url_path='',
   static_folder='static'
   )

def generateColorsByPrompt(prompt_text):
    prompt = f"""
    You are a color palette generating assistant that responds to text prompts for color palettes
    You should generate color palettes that fit the theme or mood according to the instructions of the prompt.
    The prompt is {prompt_text}
    The palettes should contain minimum 2 colors and maximum 8 colors.
    You must return only hexadecimal color codes like #FFFFFF, #ABD87D, etc
    Must contain anything. Do not return blank array.

    Must format the result in JSON array as given below:
    [color_hex, color_hex, ...]
    """

    response = openai.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )


    colors = json.loads(response.choices[0].message.content)
    return {"colors": colors}

@app.route("/generate-palette", methods=["POST"])
def generate_palette():
  query = request.form.get("query")
  colors = generateColorsByPrompt(query)
  return colors

@app.route("/")
def index():
  return render_template("index.html")

if __name__ == "__main__":
  app.run(debug=True)
