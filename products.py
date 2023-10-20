from flask import Flask, g, render_template, request
import sqlite3

app = Flask(__name__)

# Configura la conexión a tu base de datos SQLite
DATABASE = 'database.db'

# Crea una función para obtener la conexión a la base de datos
def get_db():
    # Obtiene la conexión de la variable global 'g' o crea una nueva si no existe
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Define una función para cerrar la conexión a la base de datos
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def get_products_from_db():
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    db.close()
    return products

@app.route('/products/list')
def list_products():
    # Obtén la información del navegador
    user_agent_info = {
        'User Agent': request.user_agent.string,
        'App Version': request.user_agent.version,
        'Platform': request.user_agent.platform
    }

    products = get_products_from_db()
    return render_template('products/list.html', user_agent_info=user_agent_info, products=products)

if __name__ == '__main__':
    app.run()
