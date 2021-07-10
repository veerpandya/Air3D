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


# Product Requests
@main.route('/product-requests')
def product_requests():
    '''Display product requests'''
    return render_template('product-requests.html')


# Order Form
@main.route('/order-form')
def order_form():
    '''Display order form'''
    return render_template('order-form.html')


# Product Offers
@main.route('/design-upload-form')
def design_upload_form():
    '''Display design upload form'''
    return render_template('design-upload-form.html')
