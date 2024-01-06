"""Routes for parent Flask app."""
from flask import render_template
from flask import current_app as app

"""Landing page."""
@app.route('/')
def home():
    return render_template(
        'index.html',
        title='Plotly Dash Flask Tutorial',
        description='Embed Plotly Dash into your Flask applications.',
        template='home-template',
        body="This is a homepage served with Flask."
    )
    
@app.route('/curator')
def curator():
    return render_template(
        'curator.html',
        title='Plotly Dash Flask Tutorial',
        description='Embed Plotly Dash into your Flask applications.',
        template='home-template',
        body="This is a homepage served with Flask."
    )
    
@app.route('/test')
def test():
    return render_template (
        'index_v2.jinja2',
        title='Plotly Dash Flask Tutorial',
        description='Embed Plotly Dash into your Flask applications.',
        template='home-template',
        body="This is a homepage served with Flask."   
    )