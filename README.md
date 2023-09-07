# FHighlight - Dynamic Code Highlighting for Anki

An Anki add-on that mainly adds syntax highlighting for code via a custom filter which you put in your [card templates](https://docs.ankiweb.net/templates/intro.html).

This uses the [Pygments](https://pygments.org/) library like [glutanimate](https://github.com/glutanimate/)'s _[Syntax Highlighting for Code](https://ankiweb.net/shared/info/1463041493)_ add-on. The main difference is that this add-on highlights code dynamically when it's shown in the reviewing screen,
and doesn't modify the notes themselves. This has the disadvantage that syntax highlighting will not work without the add-on (i.e. it won't work on mobile platforms), but might make it easier to dynamically modify some highlighting parameters.

## How to use

Put the add-on's filter in your card template like this:

```
{{highlight lang=python:Front}}
```

The `lang` option specifies the programming language. See [Pygments documentation](https://pygments.org/docs/lexers/) for a list of all supported languages.
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
Enclose code snippets in the triple backticks like this:

<pre>
```python
print('hello world!')
```
</pre>

You can also omit the language here.

## Download

You can download the add-on from AnkiWeb: [1339779080](https://ankiweb.net/shared/info/1339779080)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes.

## Support & feature requests

Please post any questions, bug reports, or feature requests in the [support page](https://forums.ankiweb.net/c/add-ons/11) or the [issue tracker](https://github.com/abdnh/anki-fhighlight/issues).

If you want priority support for your feature/help request, I'm available for hire.
You can get in touch from the aforementioned pages, via [email](mailto:abdo@abdnh.net) or on [Fiverr](https://www.fiverr.com/abd_nh).

## Support me

Consider supporting me if you like my work:

<a href="https://github.com/sponsors/abdnh"><img height='36' src="https://i.imgur.com/dAgtzcC.png"></a>
<a href="https://www.patreon.com/abdnh"><img height='36' src="https://i.imgur.com/mZBGpZ1.png"></a>
<a href="https://www.buymeacoffee.com/abdnh" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy Me A Coffee" style="height: 36px" ></a>

I'm also available for freelance add-on development on Fiverr:

<a href="https://www.fiverr.com/abd_nh/develop-an-anki-addon"><img height='36' src="https://i.imgur.com/0meG4dk.png"></a>
