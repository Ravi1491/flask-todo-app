import string
from flask import Flask, render_template, url_for,request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.app_context().push()

class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  content = db.Column(db.String(200), nullable=False)
  completed = db.Column(db.Integer, default=0)
  date_created = db.Column(db.DateTime, default=datetime.utcnow)
  
  def __repr__(self):
    return f"{self.id, self.content}"

@app.route('/')
def index():
  allTodo = Todo.query.all()
  return render_template('index.html', allTodo=allTodo)

@app.route('/add', methods=['POST'])
def addTodo():
  if request.method=='POST':
    title = request.form['title']
    content = request.form['content']
    
    todo = Todo(title=title, content=content)
    db.session.add(todo)
    db.session.commit()

  return redirect("/")

@app.route('/delete/<int:id>')
def deleteTodo(id):
  todo = Todo.query.filter_by(id=id).first()
  db.session.delete(todo)
  db.session.commit()
  return redirect("/")

@app.route('/completed/<int:id>')
def completeTodo(id):
  todo = Todo.query.filter_by(id=id).first()
  todo.completed = 1
  db.session.commit()
  
  return redirect("/")

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
  todo = Todo.query.filter_by(id=id).first()
  if request.method == 'POST':
    title = request.form['title']
    content = request.form['content']
    
    if len(title) > 0:
      todo.title = title
    if len(content) > 0:
      todo.content = content
    
    db.session.commit()
    
    return redirect('/')
    
  return render_template('update.html', todo=todo)

if __name__ == '__main__':
  db.create_all()
  app.run(debug=True)