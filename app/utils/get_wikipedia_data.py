import wikipedia
from utils.logger import logger


def search_pages(word: str, lang: str="en") -> list | None:
    wikipedia.set_lang(lang)
    wiki_pages = wikipedia.search(word)
    if len(wiki_pages) == 0:
        logger.error(f"Pages with word \"{word}\" not found.")
        return None
    logger.info(f"The following pages were found: {wiki_pages}.")
    return wiki_pages


def jsonify_wikipedia_page_content(wiki_page_name: str) -> dict | None:
    wiki_page = wikipedia.page(wiki_page_name)
    if not wiki_page:
        logger.error(f"Page with name \"{wiki_page_name}\" not found.")
        return None
    response = {
        "title": wiki_page.title,
        "url": wiki_page.url,
        "content": wiki_page.content,
        "summary": wiki_page.summary,
        "images": wiki_page.images,
    }
    logger.info(f"The following page was found: \"{response['title']}\".")
    return response
