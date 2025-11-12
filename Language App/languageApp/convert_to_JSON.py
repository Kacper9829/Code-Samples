import json

def convert_txt_to_json(input_file, output_file):
    word_list = []

    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            if '\t' in line:
                word, definition = line.strip().split('\t', 1)
                word_list.append({"word": word.strip(), "definition": definition.strip()})

    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(word_list, json_file, indent=4, ensure_ascii=False)


convert_txt_to_json("languageApp\word_list.txt", "languageApp\word_list.json")