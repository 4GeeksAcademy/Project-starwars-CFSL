from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    #favoritos = db.relationship('Favoritos', back_populates='User')
    favoritos = db.relationship('Favoritos', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            
            # do not serialize the password, its a security breach
        }
    
    
class Planetas(db.Model):
    id_planeta = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False, unique= True)
    diametro = db.Column(db.Integer)
    poblacion = db.Column(db.Integer)
    clima = db.Column(db.String(250))

    favoritos = db.relationship('Favoritos', backref='planetas', lazy=True)

    def __repr__(self):
        return f'<Planetas {self.id_planeta}>'

    def serialize(self):
        return {
            "id": self.id_planeta,
            "nombre": self.nombre,
            "diametro": self.diametro,
            "poblacion": self.poblacion,
            "clima": self.clima,
        }

class Personajes(db.Model):
    id_personaje = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False, unique= True)
    genero = db.Column(db.String(250))
    altura = db.Column(db.Integer)
    peso = db.Column(db.Integer)

    favoritos = db.relationship('Favoritos', backref='personajes', lazy=True)

    def __repr__(self):
        return f'<Personajes {self.id_personaje}>'

    def serialize(self):
        return {
            "id": self.id_personaje,
            "nombre": self.nombre,
            "genero": self.genero,
            "altura": self.altura,
            "peso": self.peso,
        }

class Vehiculos(db.Model):
    id_vehiculo = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False, unique= True)
    modelo = db.Column(db.String(250))
    fabricante = db.Column(db.String(250))
    num_pasajeros = db.Column(db.Integer)
    costo = db.Column(db.Integer)

    favoritos = db.relationship('Favoritos', backref='vehiculos', lazy=True)

    def __repr__(self):
        return f'<Vehiculos {self.id_vehiculo}>'

    def serialize(self):
        return {
            "id": self.id_vehiculo,
            "nombre": self.nombre,
            "modelo": self.modelo,
            "fabricante": self.fabricante,
            "num_pasajeros": self.num_pasajeros,
            "costo": self.costo,

        }
    
class Favoritos(db.Model):
    id_favorito = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planetas.id_planeta'), nullable=True)
    character_id = db.Column(db.Integer, db.ForeignKey('personajes.id_personaje'), nullable=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehiculos.id_vehiculo'), nullable=True)


    def __repr__(self):
        return f'<Favoritos {self.id_favorito}>'

    def serialize(self):
        return {
            "id": self.id_favorito,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "character_id": self.character_id,
            "vehicle_id": self.vehicle_id,

        }