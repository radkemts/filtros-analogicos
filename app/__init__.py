from flask import Flask, session
from datetime import timedelta
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY')
app.debug = os.getenv('DEBUG')
app.host = os.getenv('HOST')

app.permanent_session_lifetime = timedelta(hours=24)

@app.before_request
def create_session_id():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        session.permanent = True


from app.controllers import routes