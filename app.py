from flask import Flask, request, render_template, redirect, flash, session
from models import db,connect_db,User
from forms import RegisterForm, LoginForm, CSRFProtectForm
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "never-tell!"

bcrypt = Bcrypt()
connect_db(app)
db.create_all()

@app.get("/")
def redirect_to_register():
    """ redirect to register page """

    return redirect("/register")

@app.route("/register", methods=["GET","POST"])
def register():
    """ show a form and when submitted will create a user """

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = RegisterForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(
            username,
            password,
            email,
            first_name,
            last_name
            )

        #serialized=new_user.serialize()

        db.session.add(new_user)
        db.session.commit()
        session["username"] = new_user.username

        flash(f"Successfully added user {new_user.first_name} {new_user.last_name}")

        return redirect(f"/users/{new_user.username}")

    else:

        return render_template("register.html",form=form,title="Sign Up")

@app.route("/login", methods=["GET","POST"])
def login():
    """ Show a login form and login user when submitted """

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username
            flash("Successfully logged in")
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["Bad username/password"]
            return redirect("/login")

    return render_template("login-page.html", form=form, title= "Login Page")

@app.get("/users/<username>")
def show_user_page(username):
    """Hidden profile page for logged-in users only."""

    if "username" not in session:
        flash("You must be logged in to view!")
        return redirect("/")

    else:
        user =  User.query.filter_by(username=username).one()
        form = CSRFProtectForm()

        return render_template("user-page.html", form=form, user=user, title="You made it!")

@app.post("/logout")
def logout_user():
    """Log out user."""
    form = CSRFProtectForm()

    print("LOGOUT**********")

    if form.validate_on_submit():
        session.pop("username")

        print("INSIDE LOGOUT**********")

    return redirect("/login")

