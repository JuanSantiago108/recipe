from flask import session,request,render_template,redirect,flash
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe
from flask_bcrypt import Bcrypt


@app.route("/display/recipe")
def display_recipe():
    if session:
        return render_template("recipe.html")
    return redirect("/")


@app.route("/dashboard")
def get_recipes():
    if session:
        recipes = Recipe.get_all()
        return render_template("dashboard.html", recipes = recipes)
    return redirect('/')


@app.route("/recipe/new", methods=['POST'])
def create_recipe():
    if  not Recipe.validate_recipes(request.form):
        return redirect('/display/recipe')
    else:
        data = {
            'name': request.form['name'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'created_at': request.form['created_at'],
            'under_thirty': request.form['under_thirty'],
            'user_id': session['user_id']
        }
        Recipe.create(data)
        return redirect ("/dashboard")


@app.route("/recipe/<int:id>")
def get_recipe (id):
    if session:
        data = {
            'id':id
        }
        recipe = Recipe.get_one(data)
        return render_template("displayRecipe.html", recipe = recipe)
    return redirect('/')


@app.route("/recipe/delete/<int:id>")
def recipe_delete(id):
    if session:
        data = {
            'id':id
        }
        Recipe.delete_one(data)
        return redirect ("/dashboard")
    return redirect('/')


@app.route("/recipe/edit/<int:id>")
def display_recipe_edit(id):
    if session:
        data = {
            'id':id
        }
        recipe = Recipe.get_one(data)
        return render_template("displayEditRecipe.html",recipe = recipe)
    return redirect("/")

@app.route("/recipe/edit/<int:id>", methods=['POST'])
def update_recipe(id):
    if  not Recipe.validate_recipes(request.form):
        return redirect("/recipe/edit/<int:id>")
    else:
        data ={
            "id":id,
            "name": request.form['name'],
            "description": request.form['description'],
            "instructions": request.form['instructions'],
            "under_thirty": request.form['under_thirty'],
            "user_id": session['user_id'],
            "created_at": request.form['created_at']
        }
        Recipe.update_one(data)
        return redirect("/dashboard")