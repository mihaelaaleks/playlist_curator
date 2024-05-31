from flask_wtf import FlaskForm
import wtforms as wtf
from wtforms.validators import DataRequired
from plotly_flask.models import genre_logic

class CuratorForm(FlaskForm):
    acousticness = wtf.IntegerRangeField('acousticness', [DataRequired()])
    danceability = wtf.IntegerRangeField('danceability', [DataRequired()])
    energy = wtf.IntegerRangeField('energy', [DataRequired()])
    instrumentalness = wtf.IntegerRangeField('instrumentalness', [DataRequired()])
    liveness = wtf.IntegerRangeField('liveness', [DataRequired()])
    popularity = wtf.IntegerRangeField('popularity', [DataRequired()])
    
    artist_select = wtf.StringField(label='artists', validators= [DataRequired()])
    track_select = wtf.StringField(label ='tracks', validators= [DataRequired()])
    
    # wtforms does not support dynamic choices
    # the query isn't consistently called when the form is loaded
    genre_select = wtf.SelectMultipleField(label='genre',choices = genre_logic.genre_json_to_list(),
                                           coerce= str,
                                           validators=[DataRequired()])
    submit = wtf.SubmitField('Submit')