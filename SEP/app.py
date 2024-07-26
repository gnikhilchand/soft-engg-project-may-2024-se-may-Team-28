from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

# @app.route('/courses')
# def courses():
#     return render_template('course.html')

# @app.route('/teachers')
# def teachers():
#     return render_template('teacher.html')

# @app.route('/blog')
# def blog():
#     return render_template('blog.html')

# @app.route('/single')
# def single():
#     return render_template('single.html')

# @app.route('/contact')
# def contact():
#     return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
