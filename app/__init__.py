from flask import Flask, session
from datetime import timedelta
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY', '8!5*e!jybvgjc+e1#=y)l5%1ac$=%70v$$d59r*pg%qub^*8b8')
app.debug = os.getenv('DEBUG', 'False') == 'True'
app.host = os.getenv('HOST', '127.0.0.1')

app.permanent_session_lifetime = timedelta(hours=24)

@app.before_request
def create_session_id():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        session.permanent = True

from app import controllers
from app.views import routes