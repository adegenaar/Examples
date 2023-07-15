from jinja2 import Environment
from jinja2.loaders import DictLoader


def basic_environment() -> None:
    env = Environment(
        line_statement_prefix="#", variable_start_string="${", variable_end_string="}"
    )
    print(
        env.from_string(
            """\
    <ul>
    # for item in range(10)
        <li class="${loop.cycle('odd', 'even')}">${item}</li>
    # endfor
    </ul>\
    """
        ).render()
    )


def basic_inheritance() -> None:
    env = Environment(
        loader=DictLoader(
            {
                "a": "[A[{% block body %}{% endblock %}]]",
                "b": "{% extends 'a' %}{% block body %}[B]{% endblock %}",
                "c": "{% extends 'b' %}{% block body %}###{{ super() }}###{% endblock %}",
            }
        )
    )
    print(env.get_template("c").render())


def basic_dictloader():
    env = Environment(
        loader=DictLoader(
            {
                "child.html": """\
{% extends default_layout or 'default.html' %}
{% include helpers = 'helpers.html' %}
{% macro get_the_answer() %}42{% endmacro %}
{% title = 'Hello World' %}
{% block body %}
    {{ get_the_answer() }}
    {{ helpers.conspirate() }}
{% endblock %}
""",
                "default.html": """\
<!doctype html>
<title>{{ title }}</title>
{% block body %}{% endblock %}
""",
                "helpers.html": """\
{% macro conspirate() %}23{% endmacro %}
""",
            }
        )
    )
    tmpl = env.get_template("child.html")
    print(tmpl.render())


def basic_filter_and_linestatements() -> None:
    env = Environment(
        line_statement_prefix="%", variable_start_string="${", variable_end_string="}"
    )
    tmpl = env.from_string(
        """\
% macro foo()
    ${caller(42)}
% endmacro
<ul>
% for item in seq
    <li>${item}</li>
% endfor
</ul>
% call(var) foo()
    [${var}]
% endcall
% filter escape
    <hello world>
    % for item in [1, 2, 3]
      -  ${item}
    % endfor
% endfilter
"""
    )
    print(tmpl.render(seq=range(10)))


def basic_loop_filter():
    tmpl = Environment().from_string(
        """\
<ul>
{%- for item in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] if item % 2 == 0 %}
    <li>{{ loop.index }} / {{ loop.length }}: {{ item }}</li>
{%- endfor %}
</ul>
if condition: {{ 1 if foo else 0 }}
"""
    )
    print(tmpl.render(foo=True))


def basic_translate():
    env = Environment(extensions=["jinja2.ext.i18n"])
    env.globals["gettext"] = {"Hello %(user)s!": "Hallo %(user)s!"}.__getitem__
    env.globals["ngettext"] = lambda s, p, n: {
        "%(count)s user": "%(count)d Benutzer",
        "%(count)s users": "%(count)d Benutzer",
    }[s if n == 1 else p]
    print(
        env.from_string(
            """\
{% trans %}Hello {{ user }}!{% endtrans %}
{% trans count=users|count -%}
{{ count }} user{% pluralize %}{{ count }} users
{% endtrans %}
"""
        ).render(user="someone", users=[1, 2, 3])
    )


if __name__ == "__main__":
    basic_dictloader()
    basic_environment()
    basic_filter_and_linestatements()
    basic_inheritance()
    basic_loop_filter()
    basic_translate()
