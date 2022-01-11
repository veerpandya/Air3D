from flask import (
    request,
    redirect,
    render_template,
    url_for,
    Blueprint,
    session,
    flash
)
from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, IMAGES, configure_uploads
from bson.objectid import ObjectId
import requests
import os
from dotenv import load_dotenv
from air3d_app import app, db, socketio
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from air3d_app.models import User, Profile, Requests, Design
from air3d_app.main.forms import ProfileForm, RequestForm, DesignForm
from air3d_app import bcrypt
import stripe

main = Blueprint('main', __name__)


# Create Upload sets for offers and design requests
offers = UploadSet("offers", IMAGES)
design_requests = UploadSet("requests", IMAGES)
configure_uploads(app, (offers, design_requests))

# Set Stripe Variables
load_dotenv()

stripe_keys = {
    "secret_key": os.getenv("STRIPE_SECRET_KEY"),
    "publishable_key": os.getenv("STRIPE_PUBLISHABLE_KEY"),
}

stripe.api_key = stripe_keys["secret_key"]


# Homepage
@main.route('/')
def home():
    '''Display homepage'''
    return render_template('home.html')


# Product Offers
@main.route('/product-offers')
def product_offers():
    '''Display product offers'''
    return render_template('product-offers.html')


@main.route('/order-form', methods=['GET', 'POST'])
def create_request():
    """Create a request for a product."""
    form = RequestForm()
    if form.validate_on_submit():
        new_request = Requests(
            username=form.username.data,
            email=form.email.data,
            description=form.description.data
        )
        db.session.add(new_request)
        db.session.commit()

        flash('New request submitted successfully.')
        return redirect(url_for('main.home'))

    # if form was not valid, or was not submitted yet
    return render_template('order-form.html', form=form)


@main.route('/product-requests')
@login_required
def product_requests():
    """View list of all submitted product requests."""
    all_requests = Requests.query.all()
    return render_template('product-requests.html',
                           all_requests=all_requests)


@main.route('/create_profile', methods=['GET', 'POST'])
@login_required
def create_profile():
    """Create a public profile."""
    form = ProfileForm()
    # if form was submitted and contained no errors
    if form.validate_on_submit():
        new_profile = Profile(
            username=form.username.data
        )
        db.session.add(new_profile)
        db.session.commit()

        flash('New profile was created successfully.')
        return redirect(url_for('main.home'))

    # if form was not valid, or was not submitted yet
    return render_template('create_profile.html', form=form)


# Check to make sure the upload type is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


# Order Form
@main.route('/order-form', methods=['GET', 'POST'])
def order_form():
    '''Display order form'''
    # Handle file upload
    if request.method == 'POST' and 'request' in request.files:
        design_requests.save(request.files['request'])
        flash("Request submitted")
        return render_template('order-form.html')
    return render_template('order-form.html')


@main.route('/profile/<full_name>')
def profile(full_name):
    """View public profile of an attorny."""
    # user = User.query.filter_by(username=username).one()
    profile = Profile.query.filter_by(username=current_user.username).first()
    return render_template('profile.html', profile=profile)


# Product Offers Upload Form
@main.route('/design-upload-form')
def design_upload_form():
    '''Display design upload form'''
    # Handle file upload
    if request.method == 'POST' and 'offer' in request.files:
        offers.save(request.files['offer'])
        flash("Offer submitted")
        return render_template('design-upload-form.html')
    return render_template('design-upload-form.html')


# Chat Page
@main.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    return render_template('chat.html')


def receive_message(methods=['GET', 'POST']):
    print("New Message")


@socketio.on('message')
def message(json):
    print(str(json))
    socketio.emit('response', json, callback=receive_message)
