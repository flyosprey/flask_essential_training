import json
import os.path
from werkzeug.utils import secure_filename
from flask import render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint


bp = Blueprint("url_short", __name__)


@bp.route("/")
def home():
    return render_template("home.html", codes=session.keys())


@bp.route("/your-url", methods=["POST", "GET"])
def about():
    if request.method == "POST":
        if os.path.exists("../urls.json"):
            with open("../urls.json", "r") as urls_file:
                urls = json.load(urls_file)
        if request.form["code"] in urls.keys():
            flash("That short name has already been taken. Please, select another name")
            return redirect(url_for("url_short.home"))
        if "url" in request.form.keys():
            urls = {request.form["code"]: {"url": request.form["url"]}}
        else:
            file = request.files["file"]
            full_name = request.form["code"] + secure_filename(file.filename)
            file.save("/home/vlad/Desktop/Learning/flask_essential_training/url_short./static/user_files/" + full_name)
            urls = {request.form["code"]: {"file": full_name}}
        with open("../urls.json", "w") as urls_file:
            json.dump(urls, urls_file)
            session[request.form["code"]] = True
        return render_template("your_url.html", code=request.form["code"])
    else:
        return redirect(url_for("url_short.home"))


@bp.route("/<string:code>")
def redirect_to_url(code):
    if os.path.exists("../urls.json"):
        with open("../urls.json") as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if "url" in urls[code].keys():
                    return redirect(urls[code]["url"])
                else:
                    return redirect(url_for("url_short.static", file="user_files/" + urls[code]["file"]))
    return abort(404)


@bp.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"), 404


@bp.route("/api")
def session_api():
    return jsonify([session.keys()])
