from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "person"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/personinfo", methods=["GET"])
def get_personinfo():
    cur = mysql.connection.cursor()
    query = """
    select * from personinfo
    """
    cur.execute(query)
    data = cur.fetchall()
    cur.close

    return make_response(jsonify(data), 200)


@app.route("/personinfo/<int:id>", methods=["GET"])
def get_person_id(id):
    cur = mysql.connection.cursor()
    query = """
    SELECT * FROM person.personinfo WHERE ID = {}; """.format(id)
    cur.execute(query)
    data = cur.fetchall()
    cur.close

    return make_response(jsonify(data), 200)


@app.route("/personinfo", methods=["POST"])
def add_person():
    cur = mysql.connection.cursor()
    info = request.get_json()
    name = info.get("name")
    age = info.get("age")

    if not name or not age:
        return make_response(jsonify({"message": "Missing required fields"}), 400)

    query = "INSERT INTO personinfo (name, age) VALUES (%s, %s)"
    cur.execute(query, (name, age))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()

    return make_response(jsonify({"message": "Person added successfully",
                                 "rows_affected": rows_affected}), 201)


@app.route("/personinfo/<int:id>", methods=["PUT"])
def update_person(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    name = info.get("name")
    age = info.get("age")

    if not name or not age:
        return make_response(jsonify({"message": "Missing required fields"}), 400)

    query = "UPDATE personinfo SET name = %s, age = %s WHERE id = %s"
    cur.execute(query, (name, age, id))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()

    if rows_affected > 0:
        return make_response(jsonify({"message": "Person updated successfully",
                                 "rows_affected": rows_affected}), 200)
    else:
        return make_response(jsonify({"message": "Person not found"}), 404)


@app.route("/personinfo/<int:id>", methods=["DELETE"])
def delete_person(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM personinfo WHERE id = %s", (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()

    return make_response(jsonify({"message": "Person deleted successfully",
                                 "rows_affected": rows_affected}), 200)



if __name__ == "__main__":
    app.run(debug = True)