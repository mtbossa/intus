"""
Responsible for generating
the index.html page.
"""

import json

from jinja2 import Environment, FileSystemLoader


def index() -> None:
    """
    Generate index.html page
    using Jinja2 template.
    """
    with open('../data/local_data.json', 'r') as f:
        posts = json.loads(f.read())

    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)

    rendered = env.get_template('display.html').render(posts=posts)

    with open('../resources/index.html', 'w') as f:
        f.write(rendered)
