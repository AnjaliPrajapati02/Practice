from os import name
from flask import Flask, render_template, request, redirect, url_for,jsonify
import pymysql
from flask_mysqldb import MySQL

def sql_connector():
    conn = pymysql.connect(user='root', password='', db='crud_inflask', host='localhost')
    c = conn.cursor()
    return conn, c

app = Flask(__name__)

# MySQL configuration
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'crud_inflask'

# # Initialize MySQL
# mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method=="POST":
        id=request.form['id']
        author=request.form['author']
        price=request.form['price']

        # conn=mysql.connection.cursor()
        conn,c=sql_connector()
        c.execute("INSERT INTO book_data (id, author, price) VALUES (%s, %s, %s)", (id, author, price))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('secondpage.html', success=True)


@app.route('/home')
def index():
    # Fetch data from the database
    # cursor = mysql.connection.cursor()
    conn,c=sql_connector()
    c.execute("SELECT id, author, price FROM book_data")
    data = c.fetchall()
    conn.close()

    # Pass the data to the HTML template
    return render_template('index.html', book_data=data)



@app.route('/home', methods=['POST'])
def delete():
    conn, c = sql_connector()

    # Get the id from the form data
    row_to_delete = request.form.get('id')

    # Assuming the 'id' is an integer, you may need to convert it
    # row_to_delete = (row_to_delete)

    c.execute("DELETE FROM book_data WHERE id = %s", (row_to_delete,))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    return f"Row with id {row_to_delete} deleted successfully!"

@app.route('/edit', methods=['GET', 'POST']) # type: ignore
def update():
    if request.method == 'GET':
        row_id = request.args.get('id')
        conn, c = sql_connector()
        c.execute("SELECT * FROM book_data WHERE id = %s", (row_id,))
        row = c.fetchone()
        conn.close()
        return render_template('edit.html', row=row)

    elif request.method == 'POST':

        id = request.form.get('id')
        author = request.form.get('author')
        price = request.form.get('price')


        conn, c = sql_connector()
        c.execute("UPDATE book_data SET author = %s, price = %s WHERE id = %s", (author, price, id))
        conn.commit()
        conn.close()

        print(f"ID: {id}, Author: {author}, Price: {price}")


        return redirect(url_for('index'))
    
    






if __name__ == '__main__':
    app.run(debug=True)


