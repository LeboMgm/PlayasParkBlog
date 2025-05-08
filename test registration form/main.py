from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import smtplib
import requests

OWN_EMAIL = "mancaveeatdrink@gmail.com"
OWN_PASSWORD = "riptzznynmchnneu"


#Playas Park Blog Url
posts = requests.get("https://api.npoint.io/022c094f633c350fe1df").json()

respond = requests.get("https://sahiphopmag.co.za/")
web_page = respond.text
soup = BeautifulSoup(web_page,'html.parser')

app = Flask(__name__)

@app.route('/')
def get_all_posts():

    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post,)

@app.route("/other_posts")
def other_posts():
    blog_list = []
    link_list = []
    dates_list = []
    title = soup.find_all(name='a')
    for blog_data in range(len(title)):
        if blog_data < 10:
            blog_list.append(title[blog_data].getText())
            link_list.append(title[blog_data].get("href"))
            dates_list.append(title[blog_data].find_next(name="span", class_="date").getText())

    return render_template("other_posts.html", blogs=blog_list, links=link_list, dates=dates_list)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.sendmail(OWN_EMAIL, OWN_EMAIL, email_message)


if __name__ == "__main__":

#if you want your web server to run in repl.it, use the next line:
    app.run(host='0.0.0.0', port=8080)

#If you want your web server to run locally on your computer, use this:
    app.run(debug=True)
