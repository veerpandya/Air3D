from flask import (
    request,
    redirect,
    render_template,
    url_for,
    Blueprint,
    session,
    flash
)
from bson.objectid import ObjectId
import requests
from air3d_app import app, db
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from air3d_app.models import User, Profile, Requests, Design
from air3d_app.main.forms import ProfileForm, RequestForm, DesignForm
from air3d_app import bcrypt


main = Blueprint('main', __name__)


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


# Product Offers
@main.route('/design-upload-form')
def design_upload_form():
    '''Display design upload form'''
    return render_template('design-upload-form.html')


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
        return redirect(url_for('main.homepage'))
    
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
        return redirect(url_for('main.homepage'))

    # if form was not valid, or was not submitted yet
    return render_template('create_profile.html', form=form)


@main.route('/profile/<full_name>')
def profile(full_name):
    """View public profile of an attorny."""
    # user = User.query.filter_by(username=username).one()
    profile = Profile.query.filter_by(username=username).first()
    return render_template('profile.html', profile=profile)