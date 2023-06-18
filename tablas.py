from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cliente(db.Model):
    __tablename__ = 'clientes'
    Cli_Cedula = db.Column(db.String(15), primary_key=True)
    Cli_Nombre = db.Column(db.String(100))
    Cli_Direccion = db.Column(db.String(100))
    Cli_Telefono = db.Column(db.String(20))

    def __init__(self, Cli_Cedula, Cli_Nombre, Cli_Direccion, Cli_Telefono):
        self.Cli_Cedula = Cli_Cedula
        self.Cli_Nombre = Cli_Nombre
        self.Cli_Direccion = Cli_Direccion
        self.Cli_Telefono = Cli_Telefono

