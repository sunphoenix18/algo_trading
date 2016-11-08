import logging

from flask import Flask, render_template, request, flash
from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager, login_required, current_user
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface

import zerorpc
from forms import OperationForm

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)

app = Flask(__name__)
app.config.from_pyfile('config.py')

# flask_login configuration
login_manager = LoginManager()
login_manager.init_app(app)

# flask_mongoengine  configuration
db = MongoEngine(app)
app.session_interface = MongoEngineSessionInterface(db)

# flask_bcrypt configuration
flask_bcrypt = Bcrypt(app)

# flask_debugtoolbar configuration
toolbar = DebugToolbarExtension(app)


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    form = OperationForm(request.form)
    if request.method == 'POST':
        flash("Slicing orders on server")
        logging.debug(form.security.data)
        logging.debug(form.shares.data)
        logging.debug(form.operation.data)
        logging.debug(form.methods.data)

        user_id = str(current_user.get_id())
        stock = form.security.data
        action = int(form.operation.data)
        volume = int(form.shares.data)

        algo_trade_engine = zerorpc.Client('tcp://127.0.0.1:4242')
        algo_trade_engine.slicing_order(user_id, stock, action, volume)

    return render_template('home.html', email=current_user.email, form=form)



