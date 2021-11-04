from main import run
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
  run()
  return 'Hello World!'