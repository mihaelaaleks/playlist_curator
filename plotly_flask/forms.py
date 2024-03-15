from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerRangeField, FieldList, SelectMultipleField
from wtforms.validators import DataRequired

from plotly_flask.models import genre_logic

class CuratorForm(FlaskForm):
    acousticness = IntegerRangeField('acousticness', [DataRequired()])
    danceability = IntegerRangeField('danceability', [DataRequired()])
    energy = IntegerRangeField('energy', [DataRequired()])
    instrumentalness = IntegerRangeField('instrumentalness', [DataRequired()])
    liveness = IntegerRangeField('liveness', [DataRequired()])
    popularity = IntegerRangeField('popularity', [DataRequired()])
    
    genres_choices = genre_logic.genre_json_to_list()
    genre_select = SelectMultipleField(choices=genres_choices, default = ['jazz', 'alternative'])
    submit = SubmitField('Submit')
