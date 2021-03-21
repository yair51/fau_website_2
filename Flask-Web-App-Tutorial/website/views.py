from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, Location
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@views.route('/index')
def home():
    # queries all of the locations
    locations = Location.query.all()
    # loops through all locations
    for location in locations:
        # takes the value from the url key 'weight' + location's id
        weight = request.args.get('weight' + str(location.id))
        # changes the location's weight if the weight param exists in the url
        if weight:
            location.weight = weight
    # changes the value of the weight in the database and on screen
    db.session.commit()
    #return render_template("index.html", user=current_user, locations=locations, weight=weight)
    return render_template("index.html", user=current_user, locations=locations)

@views.route('/about')
def about():
    return render_template("about.html", user=current_user)

@views.route('/locations', methods=['GET', 'POST'])
@views.route('/locations/<int:id>', methods=['GET', 'POST'])
def locations(id=0):
    editing = False
    location = Location.query.get(id)
    if id != 0:
        # sets editing to true if the post is being editing
        editing = True
    if request.method == 'POST':
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        zip = request.form.get('zipCode')
        # if editing changes, reset all fields of the location to the current values
        if id != 0:
            location.address = address
            location.city = city
            location.state = state
            location.zip = zip
            db.session.commit()
            flash('Location edited.', category='success')
        else:
            # checks if the location exists
            location = Location.query.filter_by(address=address).first()
            if location:
                flash('Address already exists.', category='error')
                return redirect(url_for('views.locations'))
            else:
                # create a location with the following information
                new_location = Location(address=address, city=city, state=state, zip=zip, weight=0)
                # adds the location to the database
                db.session.add(new_location)
                db.session.commit()
                flash('Location added.', category='success')
                # locations = Location.query.all()
                # for place in locations:
                #     print(place.address)
                # sends user back to home page after new location is created
        return redirect(url_for('views.home'))
    return render_template("locations.html", user=current_user, editing=editing, location=location)

    # @views.route('/edit', methods=['GET','POST'])
    # def edit():
    #     return render_template("locations.html", user=current_user)


@views.route('/delete-location', methods=['POST'])
def delete_location():
    print("delete-location")
    location = json.loads(request.data)
    locationId = location['locationId']
    location = Location.query.get(locationId)
    if location:
        #if note.user_id == current_user.id:
        db.session.delete(location)
        db.session.commit()
        count = 1
        locations = Location.query.all()
        for location in locations:
            location.id = count
            count += 1
        db.session.commit()

    return jsonify({})