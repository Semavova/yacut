from flask import redirect, render_template

from . import app
from .forms import URLMapForm
from .models import URLMap
from .settings import INDEX_PAGE


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template(INDEX_PAGE, form=form)
    return render_template(
        INDEX_PAGE,
        form=form,
        short=URLMap.create_entry(
            original=form.original_link.data, short=form.custom_id.data
        )
    )


@app.route('/<string:short>')
def redirect_view(short):
    return redirect(URLMap.get_original_link(short))
