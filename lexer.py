import keyword
import re

keywords = keyword.kwlist
pattern = r'\b(' + '|'.join(keywords) + r')\b'

token_types = [
    ('keyword', pattern),
    ('var_name', r'[A-Za-z_]\w*'),
    ('const', r'-?\d+(\.\d*)?'),
    ('op', r'==|!=|>=|<=|\+=|-=|\*=|/=|[+\-*/=]'),
    ('punc', r'[\(\)\{\}\[\]:,]'),
    ('blank', r'[ \t]+|\n'),
    ('comment', r'#.*'),
    ('string', r'(\'[^\']*\'|\"[^\"]*\"|\'\'\'[^\']*\'\'\'|\"\"\"[^\"]*\"\"\")'),
    ('unknown', r'.')

]

token_re = '|'.join(f'(?P<{classtype}>{name})' for classtype, name in token_types)


def lex(code):
    tokens_list = []
    line_num = 1
    line_start = 0

    for match in re.finditer(token_re, code):
        token_type = match.lastgroup
        token_value = match.group(token_type)
        token_start = match.start()

        if token_type not in ['blank', 'comment']:
            col_num = token_start - line_start
            tokens_list.append((token_type, token_value, line_num, col_num))

        if '\n' in token_value:
            line_num += 1
            line_start = match.end()

    return tokens_list


code = open('testing.py', 'r').read()

tokens = lex(code)
for token in tokens:
    print(token)
