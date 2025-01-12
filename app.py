import os
from flask import Flask, render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Absolute path for the database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'todo.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    all_todo = Todo.query.all()
    # print(all_todo)
    return render_template("index.html", allTodo=all_todo)

# @app.route("/update/<int:sno>", methods=['GET', 'POST'])
# def update(sno):
#     todo = Todo.query.get_or_404(sno)

#     if request.method == 'POST':
#         todo.title = request.form['title']
#         todo.desc = request.form['desc']
#         db.session.commit()
#         return redirect('/')

#     return render_template('update.html', todo=todo)


@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno =sno).first()
    db.session.delete(todo)
    db.session.commit()
    return  redirect("/")

if __name__ == "__main__":
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created.")
        except Exception as e:
            print(f"Error creating database tables: {e}")

    # Check for the database file after the app context is closed
    
    if os.path.exists("todo.db"):
        print("todo.db file created successfully.")
    else:
        print("todo.db file not found.")

    app.run(debug=False, port=8000)
