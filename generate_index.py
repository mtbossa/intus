import json

from jinja2 import Environment, FileSystemLoader


def generate(local_data):

    with open(local_data, 'r') as f:
        posts = json.loads(f.read())

    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)

    rendered = env.get_template('display.html').render(posts=posts)

    with open('index.html', 'w') as f:
        f.write(rendered)
