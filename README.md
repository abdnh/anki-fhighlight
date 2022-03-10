# Anki FHighlight

An [Anki](https://apps.ankiweb.net/) add-on that adds syntax highlighting for code via a custom filter which you put in your [card templates](https://docs.ankiweb.net/templates/intro.html).

This uses the [Pygments](https://pygments.org/) library like [glutanimate](https://github.com/glutanimate/)'s *[Syntax Highlighting for Code](https://ankiweb.net/shared/info/1463041493)* add-on. The main difference is that this add-on highlights code dynamically when it's shown in the reviewing screen,
and doesn't modify the notes themselves. This has the disadvantage that syntax highlighting will not work without the add-on
(i.e. it won't work on mobile platforms). I wrote this just because I want to keep my collection a bit smaller.

## How to use

Put the add-on's filter in your card template like this:
```
{{highlight lang=python:Front}}
```

The `lang` option specifies the programming language you want to highlight its code.
See [Pygments documentation](https://pygments.org/docs/lexers/) for a list of all supported languages.
You can alternatively omit the option to make the add-on try to guess the language from the field text using Pygments' [guess_lexer](https://pygments.org/docs/api/#pygments.lexers.guess_lexer) function.

You can also dynamically specify the language for each note by prefixing the value of the lang option with `#`:
```
{{highlight lang=#lang_field:Front}}
```
Here the value of the option (`lang_field`) is interpreted as a field name where the language identifier is stored in your notes.


You can also use the following filter to list all supported languages:
```
{{highlight-list-lexers:}}
```

There is also a more flexible option for highlighting code snippets in fields without having to modify your templates.
Enclose code snippets in the the special marker `#highlight` like so:
```
#highlight:python
print('hello world!')
#highlight
```

## Building

The Pygments library is not included in this repo. You can [download it manually](https://github.com/pygments/pygments/releases/) and copy it to the src/vendor/pygments directory. Alternatively, running the included Makefile will download Pygments, package the source files, and produce an .ankiaddon file.

