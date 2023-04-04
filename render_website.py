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
    template = env.get_template('template.html')
    with open('books/book_descriptions.json', 'r') as file:
        book_descriptions_json = file.read()
    book_descriptions = json.loads(book_descriptions_json)
    book_description_chunks = list(chunked(book_descriptions, 2))

    rendered_page = template.render(
        book_description_chunks=book_description_chunks
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def main():
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ == '__main__':
    main()
