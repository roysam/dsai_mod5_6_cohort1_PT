#gemini

from flask import Flask, request, render_template
import google.generativeai as genai
from openai import OpenAI
import os
from markdown2 import Markdown

# sqlite
import sqlite3
import datetime

# Configure Gemini
genai.configure(api_key=os.environ["GEMINI_KEY"])

# Configure OpenAI
client = OpenAI(api_key=os.environ["OPENAI_KEY"])

# Configure Gemini model
# model = genai.GenerativeModel("gemini-2.0-flash")
model = genai.GenerativeModel("gemini-2.5-flash-preview-04-17")

# Flask
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    return(render_template("index.html"))

@app.route("/main", methods=["GET", "POST"])
def main():
    q = request.form.get("q")
    if q != None:
        t = datetime.datetime.now()
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute("insert into users(name,timestamp) values(?,?)",(q,t))
        conn.commit()
        c.close()
        conn.close()
        return(render_template("main.html"))
    return(render_template("main.html"))

# User Log
@app.route("/user_log",methods=["GET","POST"])
def user_log():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    c.close()
    conn.close()
    return render_template("user_log.html", users=users)

# Delete Log
@app.route("/delete_log",methods=["GET","POST"])
def delete_log():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("delete from users")
    conn.commit()
    c.close()
    conn.close()
    return render_template("delete_log.html")

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

    markdowner = Markdown()
    formatted_response = markdowner.convert(r)
   #return(render_template("openai_reply.html",r=r))
    return(render_template("openai_reply.html",r=formatted_response))

if __name__ == "__main__":
    app.run()
