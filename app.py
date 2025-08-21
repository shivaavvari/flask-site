from flask import Flask ,request, render_template , redirect
from flask_sqlalchemy import SQLAlchemy
import os 

projet_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(projet_dir,"mydatabase.db"))



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
db= SQLAlchemy(app)

class Book(db.Model):
    book = db.Column(db.String(100),unique=True,
                     nullable =True, primary_key=True)
    author = db.Column(db.String(100),
                     nullable =False)

@app.route('/updatebooks')
def updatebooks():
    books = Book.query.all()
    return render_template('updatebooks.html',books=books)

@app.route('/update',methods=['POST'])
def update():
    newname = request.form['newbook']
    oldname= request.form['oldbook']
    newauthor = request.form['newauthor']
    book = Book.query.filter_by(book=oldname).first()
    book.book = newname
    book.author = newauthor

    db.session.commit()

    return redirect('/books')


@app.route('/submitbook',methods=['POST'])
def submitbook():
    name = request.form['book']
    author = request.form['author']

    book = Book(book=name,author=author)
    db.session.add(book)
    db.session.commit()
    
    return redirect('/books')

@app.route('/addbook')
def addbook():
        
    return render_template('add_book.html')
@app.route('/delete',methods=['POST'])
def delete():
    book = request.form['oldb']
    book_1 = Book.query.filter_by(book=book).first()     
    db.session.delete(book_1)
    db.session.commit()
    return redirect('/books')
@app.route('/')
def index():
    #return 'this is the request made by th client %s' % request.headers
    return render_template('index.html')   


@app.route('/profile/<username>')
def profile(username):
    
    return render_template('profile.html',username=username, isActive =False)

@app.route('/books')
def books():
    books = Book.query.all()
    return render_template('books.html',books=books)

if __name__ =='__main__':
    with app.app_context():
        db.create_all()
        app.run(host="0.0.0.0",port=8000,debug=True)