import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Absolute path for the database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'todo.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model for the Todo table
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# Route for the home page
@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        
        print("Redirecting to prevent duplicate submissions.")
        return redirect("/")
    
    all_todo = Todo.query.all()
    return render_template("index.html", allTodo=all_todo)



# Route to delete a todo item
@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect("/")

# Main entry point for the application
if __name__ == "__main__":
    # Create database tables if they don't exist
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully.")
        except Exception as e:
            print(f"Error creating database tables: {e}")

    # Fetch the PORT environment variable for deployment
    port = int(os.environ.get("PORT", 8000))
    
    # Run the app on 0.0.0.0 to bind to all network interfaces
    app.run(debug=True, host="0.0.0.0", port=port)
