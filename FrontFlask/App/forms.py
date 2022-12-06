import requests
from flask_wtf import FlaskForm
from wtforms.fields import (BooleanField, PasswordField, StringField,
							SubmitField, SelectField)
from wtforms import EmailField
from wtforms.validators import DataRequired, Email, Length
from App.models import Book


class LoginForm(FlaskForm):
	title = StringField("Titulo")
	album = StringField("Álbum")
	channel = StringField("Canal")
	submit = SubmitField("Prosseguir")


class RegisterForm(FlaskForm):

	link = StringField("Copie o link do vídeo", validators=[DataRequired("Digita a porra do campo caralho")])
	submit = SubmitField("Seguir")


class DownloadForm(FlaskForm):
	download = SubmitField("Download")


class BookForm(FlaskForm):
	name = StringField("Nome do livro", validators=[
		DataRequired("o campo é obrigatório")
	])
	submit = SubmitField("Salvar")


class UserBookForm(FlaskForm):
	book = SelectField("Livro", coerce=int)
	submit = SubmitField("Salvar")

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.book.choices = [
			(book.id, book.name) for book in Book.query.all()
		]