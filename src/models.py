import datetime
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
    entradas = db.relationship('Entrada', backref='diario')

    def __init__(self, nombre, autor):
        self.nombre = nombre
        self.autor = autor

    @classmethod
    def new_diary(cls, nombre, autor):
        new_diary = cls(nombre, autor)
        db.session.add(new_diary)
        try:
            db.session.commit()
            return new_diary
        except Exception as error:
            print(error)
            return None

    def update(self, nombre, autor):
        self.nombre = nombre
        self.autor = autor
        try:
            db.session.commit()
            return self
        except Exception as error:
            print(error)
            return False

    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
            return True
        except Exception as error:
            print(error)
            return False

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "autor": self.autor,
            "entradas": [ entrada.serialize() for entrada in self.entradas ]
        }

class Entrada(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(128), nullable=False)
    contenido = db.Column(db.String(1024))
    fecha = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    diario_id = db.Column(db.Integer, db.ForeignKey('diario.id'))

    def __init__(self, titulo, contenido, diario):
        self.titulo = titulo
        self.contenido = contenido
        self.diario = diario

    @classmethod
    def new_entry(cls, titulo, contenido, diario):
        entrada = cls(titulo, contenido, diario)
        db.session.add(entrada)
        try:
            db.session.commit()
            return entrada
        except Exception as error:
            print(error)
            return None

    def serialize(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "fecha": self.fecha,
            "contenido": self.contenido,
            "diario": self.diario_id
        }