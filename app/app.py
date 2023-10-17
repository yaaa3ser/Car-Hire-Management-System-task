from typing import List, Dict
from flask import Flask, request, jsonify, render_template
import mysql.connector
import json

app = Flask(__name__)

db = mysql.connector.connect(
    host="db",
    user="root",
    password="root",
    port='3306',
    database="car_rental"
)
cursor = db.cursor()

@app.route('/get_customers', methods=['GET'])
def get_customers():
    query = "SELECT * FROM Customers"
    cursor.execute(query)
    customers = cursor.fetchall()
    customer_list = []
    for customer in customers:
        customer_data = {
            "customer_id": customer[0],
            "name": customer[1],
            "email": customer[2],
            "phone_number": customer[3]
        }
        customer_list.append(customer_data)
    return render_template('all_customers.html', customers=customer_list)


@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        query = "INSERT INTO Customers (name, email, phone_number) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, phone_number))
        db.commit()
        return "Customer added successfully!"
    return render_template('add_customer.html')

@app.route('/get_customer/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    query = "SELECT * FROM Customers WHERE customer_id=%s"
    cursor.execute(query, (customer_id,))
    customer = cursor.fetchone()
    if customer:
        customer_data = {
            "customer_id": customer[0],
            "name": customer[1],
            "email": customer[2],
            "phone_number": customer[3]
        }
        return render_template('customer_details.html', customer=customer_data)
    else:
        return "Customer not found!"

@app.route('/update_customer/<int:customer_id>', methods=['GET', 'POST'])
def update_customer(customer_id):
    if request.method == 'POST':
        data = request.form
        name = data['name']
        email = data['email']
        phone_number = data['phone_number']
        query = "UPDATE Customers SET name=%s, email=%s, phone_number=%s WHERE customer_id=%s"
        cursor.execute(query, (name, email, phone_number, customer_id))
        db.commit()
        return "Customer updated successfully!"
    else:
        # Retrieve customer details and render the update form
        query = "SELECT * FROM Customers WHERE customer_id=%s"
        cursor.execute(query, (customer_id,))
        customer = cursor.fetchone()
        if customer:
            customer_data = {
                "customer_id": customer[0],
                "name": customer[1],
                "email": customer[2],
                "phone_number": customer[3]
            }
            return render_template('update_customer.html', customer=customer_data)
        else:
            return "Customer not found!"

@app.route('/delete_customer/<int:customer_id>', methods=['GET'])
def delete_customer(customer_id):
    query = "DELETE FROM Customers WHERE customer_id=%s"
    cursor.execute(query, (customer_id,))
    db.commit()
    return "Customer deleted successfully!"



if __name__ == '__main__':
    app.run(host='0.0.0.0')
    

