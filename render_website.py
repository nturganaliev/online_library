import argparse
import os
import json
import urllib.parse

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def url_encode(value):
    return urllib.parse.quote(value)


def on_reload():
    AMOUNT_PER_PAGE = 20
    AMOUNT_PER_ROW = 2
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    env.filters['url_encode'] = url_encode
    parser = argparse.ArgumentParser(
        description='Enter filepath to get books descriptions.'
    )
    parser.add_argument(
        '--filepath',
        help='--filepath should be entered to get books descriptions',
        nargs='?',
        default='book_descriptions.json',
        type=str
    )
    args = parser.parse_args()

    html_pages_folder = os.path.join(os.path.abspath('.'), 'pages')
    os.makedirs(html_pages_folder, exist_ok=True)
    template = env.get_template('template.html')

    with open(args.filepath, 'r', encoding='utf-8') as file:
        book_descriptions = json.load(file)

    book_descriptions_chunks = list(
        chunked(book_descriptions, AMOUNT_PER_PAGE)
    )
    total_pages = len(book_descriptions_chunks)

    for index, book_descriptions_per_page in \
        enumerate(book_descriptions_chunks, 1):
            book_descriptions_per_row_chunks = list(
                chunked(book_descriptions_per_page, AMOUNT_PER_ROW)
            )
            rendered_page = template.render(
                book_descriptions_per_row_chunks=book_descriptions_per_row_chunks,
                total_pages=total_pages,
                current_page=index
            )
            with open(f'pages/index{index}.html', 'w', encoding='utf-8') as file:
                file.write(rendered_page)


def main():
    on_reload()

    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ == '__main__':
    main()
