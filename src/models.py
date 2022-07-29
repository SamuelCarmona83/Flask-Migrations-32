from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Diario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(48), nullable=False)
    autor = db.Column(db.String(48))

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "autor": self.autor
        }
