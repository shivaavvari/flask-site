import os
import tempfile
import pytest
from flask import template_rendered
from app import app, db, Book

# test_app.py

@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
   
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
  
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
       
        yield app.test_client()
        db.session.remove()
        db.drop_all()
    os.close(db_fd)
    os.unlink(db_path)

def capture_recorded(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    return recorded

def test_index_renders_index_html(client):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    response = client.get('/')
    template_rendered.disconnect(record, app)
    assert response.status_code == 200
    assert len(recorded) > 0  # Ensure a template was rendered

    assert recorded[-1][0].name == 'index.html'

def test_addbook_renders_add_book_html(client):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))
    
    
    template_rendered.connect(record, app)
    response = client.get('/addbook')
    template_rendered.disconnect(record, app)
    assert response.status_code == 200
    assert len(recorded) > 0  # Ensure a template was rendered

    assert recorded[-1][0].name == 'add_book.html'

def test_submitbook_adds_book_and_redirects(client):
    response = client.post('/submitbook', data={'book': 'TestBook', 'author': 'TestAuthor'})
    assert response.status_code == 302  # Redirect
    with app.app_context():
        book = Book.query.filter_by(book='TestBook').first()
        assert book is not None
        assert book.author == 'TestAuthor'

def test_books_lists_books(client):
    with app.app_context():
        db.session.add(Book(book='Book1', author='Author1'))
        db.session.commit()
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))
    
    
    template_rendered.connect(record, app)
    response = client.get('/books')
    template_rendered.disconnect(record, app)
    assert response.status_code == 200
    assert len(recorded) > 0  # Ensure a template was rendered
    assert recorded[-1][0].name == 'books.html'
    assert any(b.book == 'Book1' for b in recorded[-1][1]['books'])

def test_updatebooks_lists_books(client):
    with app.app_context():
        db.session.add(Book(book='Book2', author='Author2'))
        db.session.commit()
        db.session.add(Book(book='Book1', author='Author1'))
        db.session.commit()
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))
    
    
    template_rendered.connect(record, app)
    response = client.get('/updatebooks')
    template_rendered.disconnect(record, app)
    
    assert response.status_code == 200
    assert len(recorded) > 0  # Ensure a template was rendered
    assert recorded[-1][0].name == 'updatebooks.html'
    assert any(b.book == 'Book2' for b in recorded[-1][1]['books'])

def test_update_changes_book_and_redirects(client):
    with app.app_context():
        db.session.add(Book(book='OldBook', author='OldAuthor'))
        db.session.commit()
    response = client.post('/update', data={'oldbook': 'OldBook', 'newbook': 'NewBook', 'newauthor': 'NewAuthor'})
    assert response.status_code == 302
    with app.app_context():
        book = Book.query.filter_by(book='NewBook').first()
        assert book is not None
        assert book.author == 'NewAuthor'

def test_delete_removes_book_and_redirects(client):
    with app.app_context():
        db.session.add(Book(book='DeleteBook', author='AuthorDel'))
        db.session.commit()
    response = client.post('/delete', data={'oldb': 'DeleteBook'})
    assert response.status_code == 302
    with app.app_context():
        book = Book.query.filter_by(book='DeleteBook').first()
        assert book is None

def test_profile_renders_profile_html(client):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))
    
    
    template_rendered.connect(record, app)
    response = client.get('/profile/testuser')
    template_rendered.disconnect(record, app)
    
    assert response.status_code == 200
    assert len(recorded) > 0  # Ensure a template was rendered

    assert recorded[-1][0].name == 'profile.html'
    assert recorded[-1][1]['username'] == 'testuser'
    assert recorded[-1][1]['isActive'] is False