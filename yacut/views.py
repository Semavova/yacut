from flask import flash, redirect, render_template, url_for

from . import app
from .forms import URLMapForm
from .models import URLMap
from .settings import REDIRECT_VIEW


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        return render_template(
            'index.html',
            form=form,
            short_url=url_for(
                REDIRECT_VIEW,
                short=URLMap.create_entry(
                    original=form.original_link.data,
                    short=form.custom_id.data
                ).short,
                _external=True
            )
        )
    except Exception as error:
        flash(error)
        return render_template('index.html', form=form)


@app.route('/<string:short>')
def redirect_view(short):
    return redirect(URLMap.get_original_link_or_404(short))
