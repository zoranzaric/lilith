#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# multilang.py provides simple multilanguage support in lilith. It basically
# needs a primary language (can be defined in lilith.conf, defaults to
# systems locale) and every translation is rendered into /$year/$lang/$title/
# and offers a new environment variables in entry.html: translations, a list
# of items with lang, title and url attribute.
# Translations of one entry are bundled by an unique identifier and need the
# `lang` key to get sorted correctly. `lang` without an `identifier` key will
# not trigger multilang output.

import os, re
from jinja2 import Template
import logging

import lilith, tools
from tools import defaultfunc

log = logging.getLogger('lilith.extensions.multilang')


def cb_prepare(request):
    """copied from _prepare in lilith.py. Extended to correct url to
    /$lang/ and sets a default lang value (systems locale)"""
    
    config = request._config
    data = request._data
    for i, entry in enumerate(data['entry_list']):
        if entry.get('identifier', False) and \
        entry.get('lang', config['lang'])[0:2] != config['lang'][0:2]:
            lang = entry['lang'][0:2] + '/'
        else:
            lang = ''
        url = config.get('www_root', '') + '/' \
              + str(entry.date.year) + '/' + lang + entry['safe_title'] + '/'
        data['entry_list'][i]['url'] = url
        data['entry_list'][i]['lang_dir'] = lang
        if not entry.get('lang', None):
            data['entry_list'][i]['lang'] = config['lang'][0:2]
    
    return request

@defaultfunc
def cb_item(request):
    """Creates single full-length entry.  Looks like
    http://domain.tld/year/$lang/title/(index.html).
    
    required:
    entry.html -- layout of Post's entry
    main.html -- layout of the website
    """
    config = request._config
    data = request._data
    data['type'] = 'item'
    
    layout = config.get('layout_dir', 'layouts')
    tt_entry = Template(open(os.path.join(layout, 'entry.html')).read())
    tt_main = Template(open(os.path.join(layout, 'main.html')).read())

    # last preparations
    request = tools.run_callback(
            'prepare',
            request)
    
    dict = request._config
        
    for entry in data['entry_list']:

        translations = filter(lambda e: e != entry and \
                e.get('identifier', '') == entry.get('identifier', False),
                data['entry_list'])
        log.debug("%s's translations: %s" % (entry.title, repr(translations)))
        entry['translations'] = translations
                        
        entrydict = dict.copy()
        entrydict.update(entry)
        dict.update({'entry_list': tt_entry.render(entrydict) })
        html = tt_main.render( dict )
        
        directory = os.path.join(config.get('output_dir', 'out'),
                      str(entry.date.year),
                      entry['lang_dir'],
                      entry.safe_title)
        path = os.path.join(directory, 'index.html')
        tools.mk_file(html, entry, path)
    
    return request
    
@defaultfunc
def cb_page(request):
    """mostly identical to lilith._cb_page except of not displaying
    content which has translations and is not in default language."""
    
    config = request._config
    data = request._data
    data['type'] = 'page'
    ipp = config.get('items_per_page', 6)
    
    # last preparations
    request = tools.run_callback(
                'prepare',
                request)
    
    layout = config.get('layout_dir', 'layouts')
    tt_entry = Template(open(os.path.join(layout, 'entry.html')).read())
    tt_main = Template(open(os.path.join(layout, 'main.html')).read())
    
    dict = request._config
    entry_list = []
    for entry in data['entry_list']:
        if entry.get('identifier', False) and entry['lang'] != config['lang'][:2]:
            continue
        
        translations = filter(lambda e: e != entry and \
                e.get('identifier', '') == entry.get('identifier', False),
                data['entry_list'])
        entry['translations'] = translations    
        
        entrydict = dict.copy()
        entrydict.update(entry)
        entry_list.append(tt_entry.render(entrydict))
                
    for i, mem in enumerate([entry_list[x*ipp:(x+1)*ipp] for x in range(len(entry_list)/ipp+1)]):
        
        dict.update( {'entry_list': '\n'.join(mem), 'page': i+1,
                      'num_entries': len(entry_list)} )
        html = tt_main.render( dict )
        directory = os.path.join(config.get('output_dir', 'out'),
                         '' if i == 0 else 'page/%s' % (i+1))
        path = os.path.join(directory, 'index.html')
        tools.mk_file(html, {'title': 'page/%s' % (i+1)}, path)
        
    return request
