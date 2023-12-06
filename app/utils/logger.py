import logging


def logger_config():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("wiki_searcher.log")
        ]
    )

    logger = logging.getLogger(__name__)
    return logger


logger = logger_config()
