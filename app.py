import os
from flask import Flask,render_template, request, redirect, url_for, flash, session
from flask import current_app as app
from models import *
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy import and_, or_
from datetime import datetime, timedelta


#import matplotlib
#matplotlib.use('Agg')
# from flask import send_file
# import matplotlib.pyplot as plt
# import io
#from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super'
app.config['UPLOAD_FOLDER'] = 'uploads'

db.init_app(app)
ma.init_app(app)
bcrypt.init_app(app)

login_manager = LoginManager(app)
#login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/unauthorized")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form['name']
        mail = request.form['mail']
        password = request.form['password']
        role = request.form['role']

        if User.query.filter_by(mail=mail).first():
            flash ("Student already exists")
            return redirect(url_for("register"))
        
        if User.query.filter_by(role='admin').first() and role == 'admin':
            flash ("Instructor already exists")
            return redirect(url_for("register"))

        new_register = User(name = name, mail = mail, password = password,role=role)
        db.session.add(new_register)
        db.session.commit()
        flash ("registered successfully")
        return redirect(url_for("login"))
    
    return render_template("register.html")


@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        mail = request.form["mail"]
        password = request.form["password"]
        
        this_user = User.query.filter_by(mail=mail).first()
        if this_user and bcrypt.check_password_hash(this_user.password, password) and this_user.role == 'admin':
            login_user(this_user)
            flash("Instructor logged in successfully")
            return redirect(url_for("courses"))
        
        elif this_user and bcrypt.check_password_hash(this_user.password, password) and this_user.role == 'user':
            login_user(this_user)
            flash("Student logged in successfully")
            return redirect(url_for("courses"))
        
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully")
    return redirect(url_for("index"))

@app.route("/addcourse", methods=["GET", "POST"])
@login_required
def addcourse():
    if current_user.role != 'admin':
        return "Unauthorized access."

    if request.method == "POST":
        name = request.form['name']
        description = request.form['description']


        new_category = Course(name = name, description = description)
        db.session.add(new_category)
        db.session.commit()

        return redirect(url_for("courses"))
    return render_template("addcourse.html")

@app.route("/courses")
@login_required
def courses():
    courses = Course.query.all()
    return render_template("courses.html", courses = courses)

@app.route("/editcourse/<int:course_id>", methods=["GET", "POST"])
@login_required
def editcourse(course_id):
    course = Course.query.get_or_404(course_id)
    if request.method == "POST":
        # Update category details based on form submission
        course.name = request.form['name']
        course.description = request.form['description']
        db.session.commit()
        return redirect(url_for("courses"))
    return render_template("editcourse.html", course=course)

@app.route("/deletecourse/<int:course_id>")
@login_required
def deletecourse(course_id):
    if current_user.role != 'admin':
        return "Unauthorized access."

    course = Course.query.get(course_id)
    if not course:
        return "Course not found."
    
    assignments_to_delete = Assignment.query.filter_by(course_id=course_id).all()
    for assignment in assignments_to_delete:
        db.session.delete(assignment)

    db.session.delete(course)
    db.session.commit()

    return redirect(url_for("courses"))

@app.route("/addassignment/<int:course_id>", methods=["GET", "POST"])
@login_required
def addassignment(course_id):
    if current_user.role != 'admin':
        return "Unauthorized access."
    
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        #category_id = request.form['category']
        #category = request.form['category']

        new_Assignment = Assignment(title = title, author = author, course_id = course_id)
        db.session.add(new_Assignment)
        db.session.commit()

        return redirect(url_for("assignments", course_id = course_id))
    return render_template("addassignment.html", course_id = course_id)

@app.route("/assignments/<int:course_id>")
@login_required
def assignments(course_id):
    assignments = Assignment.query.filter_by(course_id=course_id).all()
    return render_template("assignments.html", assignments = assignments, course_id = course_id)

# @app.route("/books")
# @login_required
# def allbooks():
#     books = Book.query.all()
#     return render_template("books.html", books = books)


@app.route("/editassignment/<int:assignment_id>", methods=["GET", "POST"])
@login_required
def editassignment(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    if request.method == "POST":
        # Update book details based on form submission
        Assignment.title = request.form['title']
        Assignment.author = request.form['author']
        db.session.commit()
        return redirect(url_for("assignments", course_id=assignment.course_id))
    return render_template("editassignment.html", assignment=assignment)

@app.route("/deleteassignment/<int:assignment_id>")
@login_required
def deleteassignment(assignment_id):
    if current_user.role != 'admin':
        return "Unauthorized access."

    assignment = Assignment.query.filter_by(id=assignment_id).first()
    if not assignment:
        return "Assignment not found."
    db.session.delete(assignment)
    db.session.commit()

    return redirect(url_for("assignments", course_id=assignment.course_id))

@app.route("/search")
@login_required
def search():
    query = request.args.get('query')
    assignments = Assignment.query.filter(and_(Assignment.title.contains(query), Assignment.author.contains(query))).all()
    return render_template("search.html", query=query, assignments = assignments)

@app.route("/borrow/<int:assignment_id>")
@login_required
def borrow(assignment_id):
    assignment = Assignment.query.filter_by(id=assignment_id).first()
    if not assignment:
        return ("assignment not found.")
    
    already_borrowed = Borrow.query.filter_by(user_id=current_user.id, assignment_id=assignment_id).first()
    if already_borrowed:
        flash ("already submitted.")
        return redirect(url_for("assignments", course_id=assignment.course_id,))
    
    books_borrowed = Borrow.query.filter_by(user_id=current_user.id).count()
    if books_borrowed >= 2:
        flash ("already submitted")
        return redirect(url_for("assignments", course_id=assignment.course_id,))
        
    return_date = datetime.now() + timedelta(days=7)

    new_borrow = Borrow(user_id=current_user.id, assignment_id=assignment_id, borrow_date=datetime.now(), return_date=return_date)
    db.session.add(new_borrow)
    db.session.commit()
    flash ("Submited successfully.")
    return redirect(url_for("assignments", course_id=assignment.course_id,))

@app.route("/issuedbooks/<int:book_id>")
@login_required
def issuedbooks(assignment_id):
    assignment = Assignment.query.filter_by(id=assignment_id).first()
    if not assignment:
        flash ("No Assignments.")
        return redirect(url_for("dashboard"))
    
    issued_assignments = Issue.query.filter_by(user_id=current_user.id,assignment_id=assignment_id).all()
    if issued_assignments:
        flash (" already Done.")
        return redirect(url_for("dashboard"))
    
    borrow = Borrow.query.filter_by(assignment_id=assignment_id).first()
    if not borrow:
        flash ("assignment not borrowed.")
        return redirect(url_for("dashboard"))
    
    user = User.query.get(borrow.user_id)
    
    return_date = datetime.now() + timedelta(days=7)

    new_issue = Issue(user_id=user.id, assignment_id=assignment_id, issue_date=datetime.now(), return_date=return_date)
    db.session.add(new_issue)
    #db.session.commit()
    delete_borrow = Borrow.query.filter_by( assignment_id=assignment_id).first()
    db.session.delete(delete_borrow)
    db.session.commit()
    flash ("Assignment successfull.")
    return redirect(url_for("dashboard",assignment_id=assignment_id))

@app.route("/return/<int:book_id>")
@login_required
def return_book(assignment_id):
    assignment = Assignment.query.filter_by(id=assignment_id).first()
    if not assignment:
        return ("assignment not found.")
    
    # borrow = Borrow.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    # if not borrow:
    #     flash ("Book not borrowed.")
    #     return redirect(url_for("books", category_id=book.category_id,))
    issue = Issue.query.filter_by( assignment_id=assignment_id).first()
    if not issue:
        flash ("Assignment not present.")
        return redirect(url_for("userprofile"))

    db.session.delete(issue)
    db.session.commit()
    flash ("Assignment Done successfully.")
    return redirect(url_for("books", course_id=assignment.course_id,))

# @app.route("/revoke/<int:book_id>")
# @login_required
# def revoke(book_id):
#     book = Book.query.filter_by(id=book_id).first()
#     if not book:
#         return ("Book not found.")
    
#     issue = Issue.query.filter_by( book_id=book_id).first()
#     if not issue:
#         flash ("Book not issued.")
#         return redirect(url_for("dashboard"))

#     db.session.delete(issue)
#     db.session.commit()
#     flash ("Book revoked successfully.")
#     return redirect(url_for("dashboard"))

@app.route("/dashboard")
@login_required
def dashboard():
    borrowings = Borrow.query.all()
    users = User.query.all()
    revokes = Issue.query.all()
    # books = Book.query.all()
    return render_template("dashboard.html", borrowings=borrowings, users=users, revokes=revokes)

@app.route("/userprofile")
@login_required
def userprofile():
    issued_books = Issue.query.join(Assignment).all()
    users = User.query.all()
    print(issued_books)
    return render_template("userprofile.html", users=users, issued_books=issued_books)

@app.route("/searchbooks", methods=["GET"])
# @login_required
def searchbooks():
    query = request.args.get('query')
    if not query:
        return render_template("search.html", query=query, assignments=[])
    assignments = Assignment.query.filter(
        or_(
            Assignment.title.ilike(f'%{query}%'),  
            Assignment.author.ilike(f'%{query}%') 
        )
    ).all()
    
    return render_template("search.html", query=query, assignments = assignments)

# @app.route("/plot")
# def generate_plot():
#     # Sample data for the bar chart
#     months = ['January', 'February', 'March', 'April', 'May']
#     values = [10, 15, 7, 10, 12]

#     # Generate the bar chart
#     plt.bar(months, values)
#     plt.xlabel('Month')
#     plt.ylabel('Number of Books Borrowed')
#     plt.title('Books Borrowed per Month')

#     # Save the plot to a bytes buffer
#     buffer = io.BytesIO()
#     plt.savefig(buffer, format='png')
#     buffer.seek(0)
    
#     # Clear the plot to avoid memory leaks
#     plt.clf()

#     # Serve the plot as an image
#     return send_file(buffer, mimetype='image/png')



with app.app_context():
    db.create_all()
app.app_context().push()

if __name__ == '__main__':
    app.run(port='8000', debug=True)
