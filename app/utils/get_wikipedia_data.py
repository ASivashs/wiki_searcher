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
    wiki_page = False
    try:
        wiki_page = wikipedia.page(wiki_page_name)
    except Exception as err:
        logger.error(err)
    if not wiki_page:
        logger.error(f"Page with name \"{wiki_page_name}\" not found.")
        return False
    response = {
        "title": wiki_page.title,
        "url": wiki_page.url,
        "content": wiki_page.content,
        "summary": wiki_page.summary,
        # "images": wiki_page.images,
    }
    logger.info(f"The following page was found: \"{response['title']}\".")
    return response


def highlight_content(content: str, word: str) -> str:
    if isinstance(content, str):
        content = content.split()
    for element in range(len(content)):
        if word == content[element]:
            logger.info(f"Highlighted word {content[element]}")
            content[element] = f"<b>{content[element]}</b>"
    content = " ".join(content)
    return content


def find_on_wiki(query: list) -> bool | list:
    json_pages = []
    for page in query.split():
        page_ids = search_pages(page)
        for page_id in page_ids:      
            wiki_json_page = jsonify_wikipedia_page_content(page_id)
            if wiki_json_page:
                json_pages.append(wiki_json_page)
    return json_pages


def find_on_wiki_or(query: list) -> bool | list:
    joined_query = ' '.join(query)
    
    result = []
    joined_result = find_on_wiki(joined_query)
    
    if joined_result:
        joined_result[0]["Words"] = query
        for separated in query:
            joined_result[0]["summary"] = highlight_content(
                joined_result[0]["summary"], 
                separated
            )
            joined_result[0]["content"] = highlight_content(
                joined_result[0]["content"], 
                separated
            )
        result.append(joined_result)

    for element in query:
        element_result = find_on_wiki(element)
        for pages in element_result:
            if pages:  
                pages["summary"] = highlight_content(
                    pages["summary"], 
                    separated
                )
                pages["content"] = highlight_content(
                    pages["content"], 
                    separated
                )
                pages["Words"] = query
                result.append(pages)
    
    return result


def recursive_extract(input_list):
    result = []
    for item in input_list:
        if isinstance(item, list):
            result.extend(recursive_extract(item))
        else:
            result.append(item)
    logger.info(f"List normalized.")
    return result


def find_on_wiki_joined(query: list, separated_words: list) -> bool | list:
    if len(query) == 0:
        return False
    json_pages = []
    query = recursive_extract(query)
    for page in query:
        if page:
            if " ".join(separated_words) == page["title"]:
                page["title"] = highlight_content(
                    page["title"], 
                    " ".join(separated_words)
                )
                json_pages.append(page)
                
            separate_result_content = [True]
            for separated in separated_words:
                for w in page["content"]:
                    if separated == w:
                        page["content"] = highlight_content(
                            page["content"], 
                            separated
                        )
                        separate_result_content.append(True)
                        break
                if not all(separate_result_content):
                    separate_result_content.append(False)
                    break
            if all(separate_result_content):
                for separated in separated_words:
                    page["summary"] = highlight_content(
                        page["summary"], 
                        separated
                    )
                    page["content"] = highlight_content(
                        page["content"], 
                        separated
                    )
                json_pages.append(page)
                
            separate_result = [True]
            for separated in separated_words:
                for w in page["summary"]:
                    if separated == w:
                        page["summary"] = highlight_content(
                            page["summary"], 
                            separated
                        )
                        separate_result.append(True)
                        break
                if not all(separate_result):
                    separate_result.append(False)
                    break
            if all(separate_result):
                for separated in separated_words:
                    page["summary"] = highlight_content(
                        page["summary"], 
                        separated
                    )
                    page["content"] = highlight_content(
                        page["content"], 
                        separated
                    )
                json_pages.append(page)
    
    return json_pages


def find_on_wiki_and(query: list) -> bool | list:
    joined_query = ' '.join(query)
    
    result = []
    joined_result = find_on_wiki(joined_query)
    
    if joined_result:
        joined_result[0]["Words"] = query
        result.append(joined_result)
    
    for element in query:
        element_result = find_on_wiki(element)
        for pages in element_result:
            if pages:
                pages["Words"] = query
                result.append(pages)
    result = find_on_wiki_joined(result, query)
    
    return result
    