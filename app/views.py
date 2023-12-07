from flask import jsonify, request, render_template, Blueprint, \
    redirect, request, url_for

import json

from utils.logger import logger
from utils.find import find_words
from utils.summarizer import summarize
from utils.MetricCalculator import MetricCalculator
from utils.get_wikipedia_data import search_pages, \
    jsonify_wikipedia_page_content, find_on_wiki


wiki_searcher = Blueprint("wiki_searcher", __name__)


def recursive_extract(input_list):
    result = []
    for item in input_list:
        if isinstance(item, list):
            result.extend(recursive_extract(item))
        else:
            result.append(item)
    logger.info(f"List normalized.")
    return result


def remove_not_recognition(input_list):
    filtered_list = [d for d in input_list if "Words" in d.keys()]
    logger.info(f"Not recognition links removed.")
    return filtered_list


def remove_dublicate(input_list):
    titles = []
    result = []
    for d in input_list:
        if d["title"] not in titles:
            result.append(d)
            titles.append(d["title"])
            continue
    return result


@wiki_searcher.route("/", methods=["GET"])
def index():
    logger.info(f"Template 'index.j2' rendered.")
    return render_template("index.j2")


@wiki_searcher.route("/search-result", methods=["GET"])
def search_results():
    query = request.args.get("query")
    logger.info(f"GET request data: '{query}'")
    
    with open("total.json", 'w') as json_file:
        json.dump(recursive_extract(query), json_file) 
    
    ### Getting wiki pages
    search_result = remove_dublicate(
        remove_not_recognition(
            recursive_extract(
                find_words(query)
            )
        )
    )
    # search_result = recursive_extract(find_words(query))
    if not search_result:
        return render_template("not_found.j2")
    
    with open("normie.json", 'w') as json_file:
        json.dump(search_result, json_file)
    
    return render_template("search_result.j2", json_pages=search_result)


@wiki_searcher.route("/wiki-page/<page>", methods=["GET", "POST"])
def wiki_page(page):
    wiki_pages_json = None
    with open("normie.json", 'r') as file:
        wiki_pages_json = json.load(file)
    for wiki_page in wiki_pages_json:
        if wiki_page["title"] == page: 
            wiki_page["summary_ai"] = summarize(wiki_page["content"], per=0.05)
            return render_template("wiki_page.j2", page_info=wiki_page) 


@wiki_searcher.route("/metrics")
def metrics():
    with open("normie.json", 'r') as file:
        relevant = json.load(file)
    with open("total.json", 'r') as file:
        total = json.load(file)
    relevant_no_relevant = remove_not_recognition(relevant)
    
    metric_calculator = MetricCalculator(total, relevant_no_relevant, relevant)
    metrics = {
        "precision": metric_calculator.precision(),
        "recall": metric_calculator.recall(),
        "accuracy": metric_calculator.accuracy(),
        "error": metric_calculator.error(),
        "f_measure": metric_calculator.f_measure(),
        "average_metrics": metric_calculator.average_metrics(),
    }
    metric_calculator.trec_graph()
    
    image_file = url_for('static', filename="trec_graph.png")
    
    return render_template("metrics.j2", metrics=metrics, image_file=image_file)
