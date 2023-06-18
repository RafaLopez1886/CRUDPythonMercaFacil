from flask import Flask, render_template, request, flash, redirect, url_for
from tablas import db, Cliente
from sqlalchemy import text
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


# Configuración de la conexión a la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://conexionIUD:Rafa.lopez.96@localhost:3307/inventario_merca_facil'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la instancia de SQLAlchemy
db.init_app(app)

secret_key = os.getenv('SECRET_KEY')
app.secret_key = secret_key

@app.route('/')
def index():
    clientes = Cliente.query.all()
    return render_template('index.html', clientes=clientes)

@app.route('/add_cliente', methods=['POST'])
def add_cliente():
    if request.method == 'POST':
        Cli_Cedula = request.form['Cli_Cedula']
        Cli_Nombre = request.form['Cli_Nombre']
        Cli_Direccion = request.form['Cli_Direccion']
        Cli_Telefono = request.form['Cli_Telefono']

        cliente = Cliente(Cli_Cedula, Cli_Nombre, Cli_Direccion, Cli_Telefono)
        db.session.add(cliente)
        db.session.commit()

        flash('Cliente agregado satisfactoriamente!')
        return redirect(url_for('index'))

    return 'Recibido!'

@app.route('/edit_cliente/<Cli_Cedula>')
def get_cliente(Cli_Cedula):
    cliente = Cliente.query.get(Cli_Cedula)
    return render_template('edit-cliente.html', cliente=cliente)

@app.route('/update_cliente/<Cli_Cedula>', methods=['POST'])
def update_cliente(Cli_Cedula):
    if request.method == 'POST':
        cliente = Cliente.query.get(Cli_Cedula)

        cliente.Cli_Cedula = request.form['Cli_Cedula']
        cliente.Cli_Nombre = request.form['Cli_Nombre']
        cliente.Cli_Direccion = request.form['Cli_Direccion']
        cliente.Cli_Telefono = request.form['Cli_Telefono']

        db.session.commit()
        flash('Cliente actualizado satisfactoriamente!')
        return redirect(url_for('index'))

@app.route('/delete_cliente/<Cli_Cedula>')
def delete_cliente(Cli_Cedula):
    cliente = Cliente.query.get(Cli_Cedula)

    db.session.execute(text(f"DELETE FROM ventas WHERE Vent_Cliente='{Cli_Cedula}'"))
    db.session.delete(cliente)
    db.session.commit()

    flash('Cliente eliminado satisfactoriamente!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=3000, debug=True)
