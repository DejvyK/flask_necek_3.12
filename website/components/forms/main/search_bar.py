from flask import Markup, url_for
from website.blueprints.main.forms import Search_Bar


def component():
    form = Search_Bar()
    return Markup(f"""
    <form id="search_form">
        <div class="form-group">
            {form.query.label}
            {form.query}
        </div>
        <div class="form-group">
            {form.submit_search_bar}
        </div>
    </form>
    """)