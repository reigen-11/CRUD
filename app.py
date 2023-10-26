from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import yaml

app = Flask(__name__)
app.secret_key = 'GOT'


db = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)
db_config = {
    'host': db['mysql_host'],
    'user': db['mysql_user'],
    'password': db['mysql_password'],
    'database': db['mysql_db']
}


@app.route('/')
def index():

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    connection.close()
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO items (name) VALUES (%s)', (name,))
        connection.commit()
        connection.close()
    
    return redirect(url_for('index'))

@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit(item_id):
    if request.method == 'POST':
        name = request.form['name']

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute('UPDATE items SET name = %s WHERE id = %s', (name, item_id))
        connection.commit()
        connection.close()
    
        return redirect(url_for('index'))

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM items WHERE id = %s', (item_id,))
    item = cursor.fetchone()
    connection.close()

    return render_template('edit.html', item=item)

@app.route('/delete/<int:item_id>')
def delete(item_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute('DELETE FROM items WHERE id = %s', (item_id,))
    connection.commit()
    connection.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
