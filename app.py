#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
This is the main file of the application
"""
import os
import re
import traceback
from flask import Flask, render_template, request, redirect, url_for, session
from src.trie import Trie
from src.errors import SearchMiss


app = Flask(__name__)
app.secret_key = re.sub(r"[^a-z\d]", "", os.path.realpath(__file__))

@app.route("/", methods=["GET"])
def init():
    """ Intialize values needed in session """

    session["removed"] = []
    session["removed-word"] = ""
    session["prefix"] = []
    session["suffix"] = []
    session["correct-spelling"] = []
    session["check-if-exsist"] = ""
    session["file"] = "frequency.txt"
    return redirect(url_for('main'))

@app.route("/index")
def main():
    """ Main route """
    if "removed" not in session:
        return redirect(url_for('init'))
    return render_template("index.html")


@app.route("/check-if-exists", methods=["GET"])
def check_if_exists():
    """
    This route is for checking if the word exists
    """
    res = session["check-if-exsist"]
    if res != "":
        session["check-if-exsist"] = ""

    return render_template("check_if_exists.html", title="Check if exists", res=res)

@app.route("/check-if-exists-post", methods=["POST"])
def check_if_exists_post():
    """
    Extracting the given word
    """
    trie = Trie.create_from_file(session["file"])
    removed_words = session["removed"]
    for word in removed_words:
        trie.remove(word)
    word = request.form.get("word")

    try:
        trie.check_if_exists(word)
        session["check-if-exsist"] = "yes"
    except SearchMiss:
        session["check-if-exsist"] = "no"

    return redirect(url_for('check_if_exists'))

@app.route("/prefix", methods=["GET"])
def prefix():
    """
    This route is for having all words with the same prefix displayed
    """
    res = session["prefix"]
    if res != []:
        session["prefix"] = []

    return render_template("prefix.html", title="Prefix", res=res)

@app.route("/prefix-post", methods=["POST"])
def prefix_post():
    """
    Extracting the giving prefix
    """
    trie = Trie.create_from_file(session["file"])
    removed_words = session["removed"]
    for word in removed_words:
        trie.remove(word)
    pre = request.form.get("word")

    res = trie.prefix_search(pre)
    if not res:
        res.append("There is no word with that prefix")

    session["prefix"] = res

    return redirect(url_for('prefix'))

@app.route("/suffix", methods=["GET"])
def suffix():
    """
    This route is for having all words with the same suffix displayed
    """
    res = session["suffix"]
    if res != []:
        session["suffix"] = []

    return render_template("suffix.html", title="Suffix", res=res)

@app.route("/suffix-post", methods=["POST"])
def suffix_post():
    """
    Extracting the giving suffix
    """
    trie = Trie.create_from_file(session["file"])
    removed_words = session["removed"]
    for word in removed_words:
        trie.remove(word)
    suf = request.form.get("word")

    res = trie.suffix_search(suf)
    if res == []:
        res.append("There is no word with that suffix")

    session["suffix"] = res

    return redirect(url_for('suffix'))

@app.route("/correct-spelling", methods=["GET"])
def correct_spelling():
    """
    This route is for having all words with the correct-spelling displayed
    """
    res = session["correct-spelling"]
    if res != []:
        session["correct-spelling"] = []

    return render_template("correct_spelling.html", title="Correct-spelling", res=res)

@app.route("/correct-spelling-post", methods=["POST"])
def correct_spelling_post():
    """
    Extracting the giving correct-spelling
    """
    trie = Trie.create_from_file(session["file"])
    removed_words = session["removed"]
    for word in removed_words:
        trie.remove(word)
    sugg = request.form.get("word")

    res = trie.correct_spelling(sugg)
    if res == []:
        res.append("There is no word with that correct-spelling")

    session["correct-spelling"] = res

    return redirect(url_for('correct_spelling'))

@app.route("/all-words", methods=["GET"])
def all_words():
    """
    This route is for having all words with the same prefix displayed
    """
    trie = Trie.create_from_file(session["file"])
    removed_words = session["removed"]
    for word in removed_words:
        trie.remove(word)

    res = trie.all_words()
    res.sort()
    count = trie.word_count()

    return render_template("all_words.html", title="All words", res=res, count=count)

@app.route("/remove", methods=["GET"])
def remove():
    """
    This route is for removing words
    """
    words = session["removed"]
    res = session["removed-word"]
    if res != "":
        session["removed-word"] = ""

    return render_template("remove_word.html", title="Remove", res=res, words=words)

@app.route("/remove-post", methods=["POST"])
def remove_post():
    """
    Removing the given word
    """
    trie = Trie.create_from_file(session["file"])
    removed_words = session["removed"]
    for word in removed_words:
        trie.remove(word)
    word_to_remove = request.form.get("word")

    try:
        trie.remove(word_to_remove)
        session["removed"].append(word_to_remove)
        session["removed-word"] = word_to_remove
    except SearchMiss:
        session["removed-word"] = "That word doesn't exist"

    return redirect(url_for('remove'))

@app.route("/change-file", methods=["GET"])
def change_file():
    """
    This route is for changing the word file
    """
    res = session["file"]

    return render_template("change_file.html", title="Remove", res=res)

@app.route("/change-file-post", methods=["POST"])
def change_file_post():
    """
    Extracting the giving file names
    """
    pre = request.form.get("file")
    session["file"] = pre
    session["removed"] = []

    return redirect(url_for('change_file'))

@app.route("/about")
def show_about():
    """
    This route is for the about page
    """
    return render_template("about.html", title="Om")

@app.route("/reset")
def reset():
    """
    Route for reset session
    """
    _ = [session.pop(key) for key in list(session.keys())]

    return redirect(url_for('init'))

@app.errorhandler(404)
def page_not_found(e):
    """
    Handler for page not found 404
    """
    #pylint: disable=unused-argument
    return "Flask 404 here, but not the page you requested."


@app.errorhandler(500)
def internal_server_error(e):
    """
    Handler for internal server error 500
    """
    #pylint: disable=unused-argument
    return "<p>Flask 500<pre>" + traceback.format_exc()

if __name__ == "__main__":
    app.run(debug=True)
