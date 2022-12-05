import json
from datetime import timedelta
import requests
from werkzeug.datastructures import MultiDict

from flask import flash, redirect, render_template, url_for, request
from flask_login import (
	login_required,
	login_user,
	logout_user,
	current_user
)
from werkzeug.security import check_password_hash, generate_password_hash

from App import db
from App.models import User, Book
from App.forms import LoginForm, RegisterForm, BookForm, UserBookForm, DownloadForm


class Routes:

	def __init__(self):
		self.video_code = None

	def register(self):
		form = RegisterForm()
		if request.method == 'POST':
			link = form.data['link']
			self.video_code = link
			return redirect("http://127.0.0.1:5000/login")

		return render_template("register.html", form=form)

	def login(self): # METADATA
		result = requests.post(f'http://127.0.0.1:8000/update/{self.video_code}').json()
		form = LoginForm(formdata=MultiDict({'title': result['title'], 'album': result['album'], 'channel': result['channel']}))

		if request.method == 'POST':
			form = LoginForm()
			metadata = {
				'channel': form.channel.data,
				'title': form.title.data,
				'album': form.album.data,
			}
			requests.put(f'http://127.0.0.1:8000/update/{self.video_code}/metadata',
						 headers={'Content-Type': 'application/json'},
						 data=json.dumps(metadata))
			requests.post(f'http://127.0.0.1:8000/downloadMP3/{self.video_code}')
			return redirect("http://127.0.0.1:5000/register")
		return render_template("login.html", form=form)

	def logout(self):
		logout_user()
		return redirect(url_for("index"))

	def book_add(self):
		form = BookForm()

		if form.validate_on_submit():
			book = Book()
			book.name = form.name.data

			db.session.add(book)
			db.session.commit()

			flash("Livro cadastrado com sucesso", "success")
			return redirect(url_for("book_add"))
		return render_template("book/add.html", form=form)

	def user_add_book(id):
		form = UserBookForm()

		if form.validate_on_submit():
			book = Book.query.get(form.book.data)
			current_user.books.append(book)

			db.session.add(current_user)
			db.session.commit()

			flash("Livro cadastrado com sucesso!", "success")
			return redirect(url_for("user_add_book", id=current_user.id))

		return render_template("book/user_add_book.html", form=form)