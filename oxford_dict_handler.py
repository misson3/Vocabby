# Oct.24, 2021
# oxford_dict_api.py

import myKeys as mk
import requests
import json


app_id = mk.oxford_dict_app_id
app_key = mk.oxford_dict_app_key
language = 'en-gb'  # en-us


def parse3elements(resp_json):
    # in case word not found
    if "results" not in resp_json:
        lexCategory = ''
        definition = 'Not Found'
        example = ''
        return lexCategory, definition, example

    common_depth = resp_json["results"][0]["lexicalEntries"][0]
    # print('#####', common_depth["entries"][0]["senses"])

    if 'definitions' in common_depth["entries"][0]["senses"][0]:
        definition = common_depth["entries"][0]["senses"][0]["definitions"][0]
    else:
        definition = "Not Found"
        print("[debug] No 'definitions' key found.")

    example_intermediate = common_depth["entries"][0]["senses"][0]
    if "examples" in example_intermediate:
        example = example_intermediate["examples"][0]['text']
    else:
        example = "N.A."
    lexCategory = common_depth["lexicalCategory"]["text"]

    return lexCategory, definition, example


def lookUpDict(word):
    url = 'https://od-api.oxforddictionaries.com/api/v2/entries/' + language
    url += '/' + word.lower()
    resp = requests.get(url, headers={'app_id': app_id, 'app_key': app_key})
    resp_json = resp.json()

    category, definition, example = parse3elements(resp_json)

    return category, definition, example


def makeMessageLines(words):
    lines = []
    results = []
    for i, word in enumerate(words):
        category, definition, example = lookUpDict(word)
        if definition == 'Not Found':
            msg = '[' + word + '] NOT FOUND... :thinking_face:' + '\n'
        else:
            msg = '[' + word + ']' + '\n'
            msg += 'lexCategory: ' + category + '\n'
            msg += 'definition: ' + definition + '\n'
            msg += 'example: ' + example + '\n'
        lines.append(msg)
        results.append((word, category, definition, example))

    return lines, results


if __name__ == '__main__':
    import sys
    word = sys.argv[1]
    category, definition, example = lookUpDict(word)
    print("lexCategory: " + category)
    print(" definition: " + definition)
    print('    example: ' + example)
