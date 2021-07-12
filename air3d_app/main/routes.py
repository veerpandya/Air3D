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
from air3d_app import app, db
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from air3d_app.models import User, Profile, Requests, Design
from air3d_app.main.forms import ProfileForm, RequestForm, DesignForm
from air3d_app import bcrypt

main = Blueprint('main', __name__)

# Create Upload sets for offers and design requests
offers = UploadSet("offers", IMAGES)
design_requests = UploadSet("requests", IMAGES)
configure_uploads(app, (offers, design_requests))


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


# Product Requests
@main.route('/product-requests')
def product_requests():
    '''Display product requests'''
    return render_template('product-requests.html')


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
