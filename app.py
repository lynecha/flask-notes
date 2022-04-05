from flask import Flask, request, render_template, redirect, flash, session
from models import db,connect_db,User
from forms import RegisterForm, LoginForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "never-tell!"

connect_db(app)
db.create_all()


@app.get("/")
def redirect_to_register():
    """ redirect to register page """

    return redirect("/register")

@app.route("/register", methods=["GET","POST"])
def register():
    """ show a form and when submitted will create a user """ 

    form = RegisterForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User(username=username,
                    password=password,
                    email=email,
                    first_name=first_name,
                    last_name=last_name)

        #serialized=new_user.serialize()
        
        db.session.add(new_user)
        db.session.commit()

        flash(f"sucessfully added user {new_user.first_name} {new_user.last_name}")

        return redirect("/secret")
    
    else:

        return render_template("register.html",form=form,title = "Sign Up")

@app.route("/login", methods=["GET","POST"])
def login():
    """ Show a login form and login user when submitted """

    form = LoginForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).one_or_none()

        if user and user.password == password:
            # TODO:session stuff
            flash("Successfully logged in")
            return redirect("/secret")

        else:
            form.username.errors = ["bad username/password"]



    else:

        return render_template("login-page.html", form=form, title= "Login Page")

@app.get("/secret")
def show_secret():
    """ show secret page """

    return render_template("secret.html",title="You made it!")







