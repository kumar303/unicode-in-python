#!/usr/bin/env python

# kumar: sniped from: http://matt-good.net/files/software-dev-with-trac/rst2s5
# Author: Chris Liechti
# Contact: cliechti@gmx.net
# Copyright: This module has been placed in the public domain.

"""
A minimal front end to the Docutils Publisher, producing HTML slides using
the S5 template system.
"""

try:
    import locale
    locale.setlocale(locale.LC_ALL, '')
except:
    pass

import pygments
from pygments.lexers import get_lexer_by_name
from pygments.formatters import get_formatter_by_name
from docutils.parsers import rst
from docutils import nodes

def code_formatter(language, content):
    lexer = get_lexer_by_name(language)
    formatter = get_formatter_by_name('html', noclasses=True)
    html = pygments.highlight(content, lexer, formatter)
    return nodes.raw('', html, format='html')

def code_role(name, rawtext, text, lineno, inliner, options={},
              content=[]):
    language = options.get('language')
    if not language:
        args  = text.split(':', 1)
        language = args[0]
        if len(args) == 2:
            text = args[1]
        else:
            text = ''
    reference = code_formatter(language, text)
    return [reference], []

def code_block(name, arguments, options, content, lineno,
               content_offset, block_text, state, state_machine):
    """
    Create a code-block directive for docutils.

    Usage: .. code-block:: language

    If the language can be syntax highlighted it will be.
    """
    language = arguments[0]
    text = '\n'.join(content)        
    reference = code_formatter(language, text)
    return [reference]

# These are documented
# at http://docutils.sourceforge.net/spec/howto/rst-directives.html.
code_block.arguments = (
    1, # Number of required arguments.
    0, # Number of optional arguments.
    0) # True if final argument may contain whitespace.

# A mapping from option name to conversion function.
code_role.options = code_block.options = {
    'language' :
    rst.directives.unchanged # Return the text argument, unchanged
}
code_block.content = 1 # True if content is allowed.
# Register the directive with docutils.
rst.directives.register_directive('code-block', code_block)
rst.roles.register_local_role('code-block', code_role)


from docutils.core import publish_cmdline, default_description

description = ('Generates S5 (X)HTML slideshow documents from standalone '
               'reStructuredText sources.  ' + default_description)

publish_cmdline(writer_name='s5', description=description)
