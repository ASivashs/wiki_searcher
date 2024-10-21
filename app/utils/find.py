from utils.get_wikipedia_data import find_on_wiki_and, find_on_wiki_or


str_to_token = {
    '1': True,
    '0': False,
    'AND': lambda left, right: left and right,
    'OR': lambda left, right: left or right,
    'NOT': lambda right: not right,
    '(': '(',
    ')': ')'
}
empty_res = True


def create_token_lst(s, str_to_token=str_to_token):
    s = s.replace('(', ' ( ')
    s = s.replace(')', ' ) ')

    return [str_to_token[it] for it in s.split()]


def find(lst, what, start=0):
    return [i for i, it in enumerate(lst) if it == what and i >= start]


def parens(token_lst):
    left_lst = find(token_lst, '(')

    if not left_lst:
        return False, -1, -1

    left = left_lst[-1]

    if token_lst[left + 1] != 0 and token_lst[left + 1] != 1:
        right = find(token_lst, ')', left + 3)[0]
    else:
        right = find(token_lst, ')', left + 4)[0]

    return True, left, right


def bool_eval(token_lst):
    if len(token_lst) == 2:
        return token_lst[0](token_lst[1])
    else:
        return token_lst[1](token_lst[0], token_lst[2])


def formatted_bool_eval(token_lst, empty_res=empty_res):
    if not token_lst:
        return empty_res

    if len(token_lst) == 1:
        return token_lst[0]

    has_parens, l_paren, r_paren = parens(token_lst)

    if not has_parens:
        return bool_eval(token_lst)

    token_lst[l_paren:r_paren + 1] = [bool_eval(token_lst[l_paren+1:r_paren])]

    return formatted_bool_eval(token_lst, bool_eval)


def nested_bool_eval(s):
    return formatted_bool_eval(create_token_lst(s))


###################################
def find_words(query):
    query = query.split(")")
    result = []
    for query_element in query:
        if "AND" in query_element:
            query_words = query_element.split("AND")
            query_words = [_.strip() for _ in query_words]
            query_words = [_.strip('(') for _ in query_words]
            search_result = find_on_wiki_and(query_words)
            if search_result:
                result.append(search_result)
        if "OR" in query_element:
            query_words = query_element.split("OR")
            query_words = [_.strip() for _ in query_words]
            query_words = [_.strip('(') for _ in query_words]
            search_result = find_on_wiki_or(' '.join(query_words).split())
            if search_result:
                result.append(search_result)
    return result


def find_word_in_content(text: str, page):
    result = 0
    if word in page:
        result = 1
        words_list.append(word)
    return str(result)


def find_word_in_title(text: str, page):
    result = 0
    if word in page:
        result = 1
        words_list.append(word)
    return str(result)
