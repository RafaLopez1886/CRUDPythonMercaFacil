from flask import Flask, render_template, request, flash, redirect, url_for
import pymysql

app = Flask(__name__)

#Conexión MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3307
app.config['MYSQL_USER'] = 'conexionIUD'
app.config['MYSQL_PASSWORD'] = 'Rafa.lopez.96'
app.config['MYSQL_DB'] = 'inventario_merca_facil'

#CONFIGURACIONES

app.secret_key='mysecretkey'

def get_db_connection():
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        port=app.config['MYSQL_PORT'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def index():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = 'SELECT * FROM clientes'
        cursor.execute(sql)
        data = [tuple(row.values()) for row in cursor.fetchall()]
        print(data)
    return render_template('index.html', clientes = data)
    cursor.close()
    connection.close()


@app.route('/add_cliente', methods=['POST'])
def add_cliente():
    if request.method == 'POST':
        Cli_Cedula = request.form['cli_Cedula']
        Cli_Nombre = request.form['cli_Nombre']
        Cli_Direccion = request.form['cli_Direccion']
        Cli_Telefono = request.form['cli_Telefono']

        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                sql = 'INSERT INTO clientes (Cli_Cedula, cli_Nombre, cli_Direccion, cli_Telefono) VALUES (%s, %s, %s, %s)'
                cursor.execute(sql, (Cli_Cedula, Cli_Nombre, Cli_Direccion, Cli_Telefono))
                connection.commit()

        except:
            connection.rollback()
        finally:
            flash('Cliente agregado satisfactoriamente!')
            return redirect(url_for('index'))
            connection.close()

    return 'Recibido!'


@app.route('/edit_cliente/<cli_Cedula>')
def get_cliente(cli_Cedula):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = ('SELECT * FROM clientes WHERE Cli_Cedula = %s')
        cursor.execute(sql,(cli_Cedula))
        data = [tuple(row.values()) for row in cursor.fetchall()]
        print(data[0])
        connection.commit()
        return render_template('edit-cliente.html', cliente = data[0])

@app.route('/update_cliente/<cli_Cedula>', methods = ['POST'])
def update_cliente(cli_Cedula):
    if request.method == 'POST':
        Cli_Cedula = request.form['cli_Cedula']
        Cli_Nombre = request.form['cli_Nombre']
        Cli_Direccion = request.form['cli_Direccion']
        Cli_Telefono = request.form['cli_Telefono']

        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = ("""
            UPDATE clientes
            SET Cli_Cedula = %s,
                Cli_Nombre = %s,
                Cli_Direccion = %s,
                Cli_Telefono = %s
            WHERE Cli_Cedula = %s
            """)
            cursor.execute(sql, (Cli_Cedula, Cli_Nombre, Cli_Direccion, Cli_Telefono, cli_Cedula))
            connection.commit()

            flash('Cliente actualizado satisfactoriamente!')
        return redirect(url_for('index'))
        connection.close()


@app.route('/delete_cliente/<string:cli_Cedula>')
def delete_cliente(cli_Cedula):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql =('DELETE FROM clientes WHERE Cli_Cedula = {0}'.format(cli_Cedula))
            cursor.execute(sql)
            connection.commit()
    except:
        connection.rollback()

    finally:
        flash('Cliente eliminado satisfactoriamente!')
        return redirect(url_for('index'))
        connection.close()



if __name__ == '__main__':
    app.run(port = 3000, debug = True)
