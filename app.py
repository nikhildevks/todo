from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy   
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMYTRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False )
    desc = db.Column(db.String(1000), nullable=False )
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"




@app.route('/',methods=['GET','POST'])
def home():
    if request.method == 'POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
    




    all_todo=Todo.query.all()
    return render_template('index.html',all_todo=all_todo)

@app.route('/update/<sno>',methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        update_item=Todo.query.filter_by(sno=sno).first()
        update_item.title=title
        update_item.desc=desc
        db.session.add(update_item)
        db.session.commit()
        return redirect("/")
    update_item=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todos=update_item)


#@app.route('/update/<todos.sno>')
#def update(sno):


@app.route('/delete/<sno>')
def delete(sno):
    delete_item=Todo.query.filter_by(sno=sno).first()
    db.session.delete(delete_item)
    db.session.commit()
    return redirect ("/")

if __name__=="__main__":
    app.run(debug=True,port=8000)