from flask import Flask,render_template,redirect, request
from application import app
from hashids import Hashids

hashids = Hashids(
    salt="as$$Gnz5H1H2bWvBbMnZ5A^XCcD&K$xz#@3205V@4#98yt4q23wqo!ADei",
    min_length=7,
    alphabet="1234567890zxcvbnmASDFGHJKLPOIUYqwterQWERMZX"
    )

@app.route('/')
def home():

    #if request.method == "post":
    #    original_url = request.form['original_url']

    return "hello world"

@app.route('/encode/<int:num>')
def encoding(num=1):
    id = hashids.encode(num)
    return id

@app.route('/<string:s>')
def view(s):
    n = hashids.decode(s)
    if n ==():
        return "<h1>Invailid url</h1>"
    list_n = list(n)

    return str(list_n[0])