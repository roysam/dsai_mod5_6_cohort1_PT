#gemini

from flask import Flask, request, render_template
import google.generativeai as genai
from openai import OpenAI
import os

# Configure Gemini
genai.configure(api_key=os.environ["gemini_key"])

# Configure OpenAI
client = OpenAI(api_key=os.environ["openai_key"])

# Configure Gemini model
# model = genai.GenerativeModel("gemini-2.0-flash")
model = genai.GenerativeModel("gemini-2.5-flash-preview-04-17")

# Flask
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return(render_template("index.html"))

# Gemini
@app.route("/gemini",methods=["GET","POST"])
def gemini():
    return(render_template("gemini.html"))

@app.route("/gemini_reply",methods=["GET","POST"])
def gemini_reply():
    q = request.form.get("q")
    print(q)
    r = model.generate_content(q)
    r = r.text
    return(render_template("gemini_reply.html",r=r))

# OpenAI
@app.route("/openai",methods=["GET","POST"])
def openai():
    return(render_template("openai.html"))

@app.route("/openai_reply",methods=["GET","POST"])
def openai_reply():
    q = request.form.get("q")
    response = client.chat.completions.create(
      model="gpt-4o",
      messages=[{"role": "user", "content": q}]
    )
    r = response.choices[0].message.content
    return(render_template("openai_reply.html",r=r))

if __name__ == "__main__":
    app.run()
