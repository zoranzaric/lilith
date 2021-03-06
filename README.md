lilith
======

lilith is yet another lightweight static blogging software. It is designed to be
easily extendable and offers a various number of built-in plugins.

lilith is licensed under the Common Development and Distribution License (CDDL).

Features
--------

- blog articles, pages and rss/atom feeds
- theming support (using [jinja2](http://jinjna.pocoo.org/))
- [reStructuredText][1] and [Markdown][2] as markup languages
- (currently only german) hyphenation using `&shy;`
- MathML generation using [AsciiMathML][3]

[1]: http://docutils.sourceforge.net/rst.html
[2]: http://daringfireball.net/projects/markdown/
[3]: http://www1.chapman.edu/~jipsen/mathml/asciimath.html

Quickstart
----------

Dependencies `python` (at least 2.5), `pyyaml`, `shpaml`, and `jinja2`. And
of course `docutils` (`pygments` for syntax highlighting) or `markdown` for
markup, but not required in plain HTML.

    pip install pyyaml shpaml jinja2

Get lilith and edit `lilith.conf` and `layouts/`. Run lilith with:

    python lilith.py
    
which renders everything to `output_dir` (defaults to */out*). lilith has
a basic commandline interface, specify `-c FILE` to use another config file
and `-l DIR` to use an alternate layouts-folder (overwrites settings in
lilith.conf).


Using lilith
------------

lilith uses a flat file db to store its blog entries. It does not depend on a
specific filesystem structure, neither the user's structure has any effect on
the rendered output. Just specify a `entries_dir` in `lilith.conf`, lilith will
traverse this folder and processes all files in it.

An entry consists of two parts. A [YAML](http://en.wikipedia.org/wiki/YAML)-header
and then the real content. Inside the YAML-header you must specify at least
a `title: My Title`. I recommend to use a `date: 21.12.2012, 16:47` key otherwise
lilith is using the last modified timestamp.

If you don't know, what markup-language you prefer or if yo are using different
markup languages, use e.g. `parser: rst` for reStructuredText.

### Sample entry.txt

    ---
    title: A meaningful title
    parser: Markdown # optional
    date: 19.06.2011, 12:45 # recommended
    ---

    Your content goes here...

### lilith.conf – YAML syntax!

    # required in templating
    author:     your name
    website:    http://mywebsite.org/
    email:      me@example.org
    blog_title: your website's title
    www_root:   http://path.to/blog/

    # optional keys:
    ext_dir:        a list of dirs containing extensions for lilith, defaults to "ext/"
    ext_ignore:     a list of extensions to ignore, e.g. [mathml, ]
    entries_dir:    dir holding your entries, defaults to "content/"
    output_dir:     output directory, defaults to "out/"
    items_per_page: used for pagination, defaults to 6
        
    parser:         a default entry parser # NOTE: currently not used
    strptime:       your human-readable time parsing format, defauts to "%d.%m.%Y, %H:%M"
    lang:           (de-DE, ...) # used in HTML-layout (and for hyphenation, later)
    
You can specify every other key-value pair you want use in plugins or as
Template variable. Adding an existing key-value pair in the YAML-header
of an entry will locally overwrite the config's value.

### the output

    out/
    ├── 2011/
    │   └── a-meaningful-title/
    │       └── index.html
    ├── articles/
    │   └── index.html
    ├── atom/
    │   └── index.xml
    ├── rss/
    │   └── index.xml
    └── index.html

You may need to set index.xml as index-page in your webserver's configuration
to get rss and atom feeds in http://domain.org/atom/ or /rss/ .

Extensions
----------

### builtin

- **syndication**: produces valid atom and rss feeds
- **summarize**: summarizes posts to 200 words in pagination
- **hyphenate**: hyphenation using `&shy;` (currently german-only)
- **mathml**: asciimathml to MathML converter
- **articles**: simple article overview

These extensions are maintained by me and their compatibily is ensured.
