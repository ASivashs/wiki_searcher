from flask import Flask, redirect, url_for


def create_app():
    app = Flask(__name__)
    
    # extensions
    from utils.logger import logger_config
    
    # blueprints
    from views import wiki_searcher
    app.register_blueprint(wiki_searcher)
    
    return app


app = create_app()
