from flask import Flask, request, render_template, redirect, flash, session
from models import db,connect_db,User, Note
from forms import RegisterForm, LoginForm, CSRFProtectForm, AddNoteForm, UpdateNoteForm
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

    if "username" not in session and session["username"] != username:
        flash("You must be logged in to view!")
        return redirect("/")

    else:
        user = User.query.get_or_404(username)
        form = CSRFProtectForm()

        return render_template("user-page.html", form=form, user=user, title="You made it!")

@app.post("/logout")
def logout_user():
    """Log out user."""
    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop("username")

    return redirect("/login")

@app.post("/users/<username>/delete")
def delete_user(username):
    """Delete user """

    if "username" not in session:
        flash("You must be logged in to view!")
        return redirect("/")

    form = CSRFProtectForm()


    if form.validate_on_submit():
        user = User.query.filter_by(username=username).one()
        if user.notes:
            user_notes = user.notes
            db.session.delete(user_notes)
        db.session.delete(user)
        db.session.commit()
        session.pop("username")

        return redirect("/")

@app.route("/users/<username>/notes/add", methods=["GET","POST"])
def add_notes(username):
    """display add note page and add notes on submit """

    if "username" not in session:
        flash("You must be logged in to view!")
        return redirect("/")

    form = AddNoteForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=username).one() 

        title = form.title.data
        content = form.content.data

        new_note = Note(title=title,content=content,owner=user.username)
        db.session.add(new_note)
        db.session.commit()

        return redirect(f"/users/{user.username}")


    else:
        return render_template("add-note.html",form=form,title="Add Notes")


@app.route("/notes/<int:note_id>/update", methods=["GET", "POST"])
def edit_notes(note_id):
    """Display edit note form and make updates on submit """

    if "username" not in session:
        flash("You must be logged in to view!")
        return redirect("/")

    note = Note.query.get(note_id)
    form = UpdateNoteForm(obj=note)

    if form.validate_on_submit():

        note.title = form.title.data
        note.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{note.owner}")

    else:
        return render_template("edit-note.html", form=form,title="Edit Note")

@app.post("/notes/<int:note_id>/delete")
def delete_note(note_id):
    """Delete note """

    note = Note.query.get_or_404(note_id)
    if "username" not in session and session["username"] != note.owner:
        flash("You must be logged in to view!")
        return redirect("/")

    form = CSRFProtectForm()


    if form.validate_on_submit():
        
        username = note.owner
        
        db.session.delete(note)
        db.session.commit()

        return redirect(f"/users/{username}")


    


