from flask import jsonify, request, render_template, Blueprint, \
    redirect, request, url_for

from utils.logger import logger


wiki_searcher = Blueprint("wiki_searcher", __name__)


@wiki_searcher.route("/")
def index():
    logger.info(f"Template 'index.j2' rendered.")
    if request.args.get("search"):
        redirect(url_for("wiki_searcher.search_results"))
    return render_template("index.j2")


@wiki_searcher.route("/search-result")
def search_results():
    pass


@wiki_searcher.route("/search-result/<page>")
def wiki_page(page):
    pass


@wiki_searcher.route("/metrics")
def metrics():
    pass
