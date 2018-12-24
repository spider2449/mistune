from mistune.scanner import escape_url
from mistune.inlines import ESCAPE

#: url link like: ``https://lepture.com/````````
URL_LINK_PATTERN = r'''(https?:\/\/[^\s<]+[^<.,:;"')\]\s])'''


def parse_url_link(self, m, state):
    return 'link', escape_url(m.group(0))


def url(md):
    md.inline.register_rule('url_link', URL_LINK_PATTERN, parse_url_link)
    md.inline.default_rules.append('url_link')


#: strike through syntax looks like: ``~~word~~``
STRIKETHROUGH_PATTERN = (
    r'~~(?=[^\s~])('
    r'(?:\\~|[^~])*'
    r'(?:' + ESCAPE + r'|[^\s~]))~~'
)


def parse_strikethrough(self, m, state):
    text = m.group(1)
    return 'strikethrough', self.render(text, state)


def render_html_strikethrough(text):
    return '<del>' + text + '</del>'


def strikethrough(md):
    md.inline.register_rule(
        'strikethrough', STRIKETHROUGH_PATTERN, parse_strikethrough)

    index = md.inline.default_rules.index('codespan')
    if index != -1:
        md.inline.default_rules.insert(index + 1, 'strikethrough')
    else:
        md.inline.default_rules.append('strikethrough')

    if md.renderer.NAME == 'html':
        md.renderer.register('strikethrough', render_html_strikethrough)
