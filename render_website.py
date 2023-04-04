import os
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    path = os.path.abspath('.')
    directory = os.path.join(path, 'pages')
    os.makedirs(directory, exist_ok=True)
    template = env.get_template('template.html')
    with open('books/book_descriptions.json', 'r') as file:
        book_descriptions_json = file.read()
    book_descriptions = json.loads(book_descriptions_json)
    page_book_chunks = list(chunked(book_descriptions, 20))

    for index, page_book_chunk in enumerate(page_book_chunks):
        book_description_chunks = list(chunked(page_book_chunk, 2))
        rendered_page = template.render(
            book_description_chunks=book_description_chunks
        )
        with open(f'pages/index{index}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


def main():
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ == '__main__':
    main()
