import argparse
import os
import json

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def on_reload():
    load_dotenv('.env')
    book_amount_per_page = int(os.getenv('BOOK_AMOUNT_PER_PAGE'))
    book_amount_per_row = int(os.getenv('BOOK_AMOUNT_PER_ROW'))
    filepath = os.getenv('FILEPATH')
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    parser = argparse.ArgumentParser(
        description='Enter filepath to get books descriptions.'
    )
    parser.add_argument(
        '--filepath',
        help='--filepath should be entered to get books descriptions',
        nargs='?',
        type=str
    )
    args = parser.parse_args()

    if args.filepath:
        filepath = args.filepath

    html_pages_folder = os.path.join(os.path.abspath('.'), 'pages')
    os.makedirs(html_pages_folder, exist_ok=True)
    template = env.get_template('template.html')

    with open(filepath, 'r', encoding='utf-8') as file:
        books = json.load(file)
    books_chunks = list(chunked(books, book_amount_per_page))
    total_pages = len(books_chunks)

    for index, books_per_page in enumerate(books_chunks, 1):
        books_per_row_chunks = list(
            chunked(books_per_page, book_amount_per_row)
        )
        rendered_page = template.render(
            books_per_row_chunks=books_per_row_chunks,
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
