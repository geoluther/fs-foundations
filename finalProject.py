from flask import Flask, render_template, url_for, redirect, request, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

## create main restaurant page
@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
	restaurants = session.query(Restaurant).all()
	return render_template('main.html', restaurants=restaurants)
    # return "page to list restaurants complete!"


## create a new restaurant
@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        restName = Restaurant(
            name=request.form['name'])
        session.add(restName)
        session.commit()
        flash("New Restaurant Created")
        return redirect(url_for('showRestaurants'))
    else:
    	return render_template('newRestaurant.html')
    #return "page to CREATE a new restaurant done"


## show restaurant menu by rest. id
@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)


## edit a restaurant
@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		restaurant.name = request.form['name']
		session.add(restaurant)
		session.commit()
		flash("Restaurant Name Edited")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('editRestaurant.html', restaurant = restaurant)
    # return "EDIT page for restaurant %s done" % restaurant_id


## delete a restaurant
@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	deletedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		session.delete(deletedRestaurant)
		session.commit()
		flash("Restaurant Deleted")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('deleteRestaurant.html', restaurant = deletedRestaurant,)
    #return "page to DELETE a new restaurant done"


# Task 1: Create route for newMenuItem function here

@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(name=request.form['name'], description=request.form[
			'description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
		session.add(newItem)
		session.commit()
		flash("menu item added")
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	else:
		return render_template('newmenuitem.html', restaurant_id=restaurant_id)


# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['course']:
            editedItem.course = request.form['course']
        session.add(editedItem)
        session.commit()
        flash("menu item edited")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:

        return render_template('editmenuitem.html', restaurant_id = restaurant_id,
 			MenuID = menu_id, item = editedItem)

    # return "page to edit a menu item. Task 2 complete!"


# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	deletedItem = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		session.delete(deletedItem)
		session.commit()
		flash("menu item deleted")
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
	#USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
		return render_template('deletemenuitem.html', restaurant_id = restaurant_id,
			MenuID = menu_id, item = deletedItem)
	# return "page to delete a menu item. Task 3 complete!"

## ENDPOINTS

## all restaurants menu endpoint
@app.route('/restaurants/JSON')
def restaurantsJSON():
    #restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(Restaurant).all()
    return jsonify(Restaurants=[i.serialize for i in items])

## restaurant menu endpoint
@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    #restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

## menu item endpoint
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    #restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item = session.query(MenuItem).filter_by(
        id=menu_id).one()
    return jsonify(MenuItem=item.serialize)


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)


