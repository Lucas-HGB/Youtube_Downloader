from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
login_manager = LoginManager()
bootstrap = Bootstrap()


def create_app():
	app = Flask(__name__)
	app.config["SECRET_KEY"] = 'secret'
	app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

	db.init_app(app)
	login_manager.init_app(app)
	bootstrap.init_app(app)

	from App import routes
	routes = routes.Routes()

	@app.route("/register", methods=["GET", "POST"])
	def register():
		return routes.register()

	@app.route("/login", methods=["GET", "POST"])
	def login():
		return routes.login()

	@app.route("/download", methods=["GET", "POST"])
	def download():
		return routes.download()

	@app.route("/logout")
	def logout():
		return routes.logout()

	@app.route("/book/add", methods=["GET", "POST"])
	def book_app():
		return routes.book_add()

	@app.route("/user/<int:id>/add-book",  methods=["GET", "POST"])
	def user_add_book():
		return routes.user_add_book()


	return app