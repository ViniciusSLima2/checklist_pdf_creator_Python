from flask import Flask, render_template, jsonify, request, redirect
import psycopg2
import pdf_creator
app = Flask(__name__)


def get_serial(modelo):
    try:
        data = [x[1] for x in get_model()]
        if modelo in data:
            connection = psycopg2.connect(
                host="localhost",
                database="postgres",
                user="postgres",
                password="root")
            cursor = connection.cursor()
            postgreSQL_select_Query = "SELECT serial_cel, id FROM seriais WHERE id_modelo = (SELECT m.id FROM modelo as m WHERE m.nome_modelo = '{0}');".format(modelo)

            cursor.execute(postgreSQL_select_Query)
            mobile_records = cursor.fetchall()
            return mobile_records
        else:
            raise TypeError("Invalid Model")
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
    finally:
        if connection is not None:
            connection.close()
            print("Database connection closed.")

def get_model():
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="root")

        cursor = connection.cursor()
        postgreSQL_select_Query = "SELECT * FROM modelo"

        cursor.execute(postgreSQL_select_Query)
        mobile_records = cursor.fetchall()
        return mobile_records
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
    finally:
        if connection is not None:
            connection.close()
            print("Database connection closed.")

@app.route('/')
def main():
    mobile_records = get_model()
    outputArray = []
    for record in mobile_records:
        outputObj = {
            'id': record[0],
            'nome_modelo': record[1]
        }
        outputArray.append(outputObj)
    return render_template("index.html", modelos=outputArray)

@app.route('/serials_iphone', methods=['POST', 'GET'])
def GetIphoneModel():
    category_id = request.form['category_id']
    iphoneModel = get_serial(category_id)
    outputArray = []
    for row in iphoneModel:
        outputObj = {
            'id' : row[1],
            'serial' : row[0]
        }
        outputArray.append(outputObj)
    return jsonify(outputArray)


@app.route('/formSubmit', methods=['POST', 'GET'])
def formSubmit():
    model = request.form.get("modelosIphone")
    employee_name = request.form.get("fullname_employee")
    client_name = request.form.get("fullname_client")
    serial = request.form.get("id_iPhone")
    color = request.form.get("color")
    problem = request.form.get("problem")
    pdf_creator.create_pdf(model, serial, client_name, employee_name, color, problem)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
