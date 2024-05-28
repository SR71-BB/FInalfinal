from flask import Flask, make_response, jsonify
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



if __name__ == "__main__":
    app.run(debug = True)