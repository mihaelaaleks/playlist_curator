import wtforms as wtf
from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField
from wtforms.validators import DataRequired

from plotly_flask.models import genre_logic


class CuratorForm(FlaskForm):
    # wtforms does not support dynamic choices
    # the query isn't consistently called when the form is loaded
    genre_select = SelectMultipleField(
        choices=genre_logic.genre_json_to_list(),
        coerce=str,
        validators=[DataRequired()],
    )
    submit = SubmitField("Submit")


class CuratorTypeForm(FlaskForm):
    from_scratch = SubmitField("From Scratch")
    from_playlist = SubmitField("From Own Playlist")
