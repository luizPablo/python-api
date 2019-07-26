from flask import Flask, jsonify, request, json
from flaskext.mysql import MySQL

app = Flask(__name__)  
mysql = MySQL()

# MySQL: Parametros do BD
app.config['MYSQL_DATABASE_USER'] = 'root'  
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin'  
app.config['MYSQL_DATABASE_DB'] = 'proximo_db'  
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)

#Listar dados de uma tabela
@app.route('/list/<tabela>')
def get(tabela):
    con = mysql.connect()
    cur = con.cursor()

    cur.execute('''select * from proximo_db.{}'''.format(tabela))
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.close()
    con.close()
    
    return jsonify({tabela : r})

#Mostrar registro de uma tabela, partindo de uma coluna de idenficacao
@app.route('/get/<tabela>/<id_tab>')
def getTable(tabela, id_tab):
    con = mysql.connect()
    cur = con.cursor()

    cur.execute('''select * from proximo_db.{} where id = {}'''.format(tabela, id_tab))
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    
    cur.close()
    con.close()
    
    return jsonify({tabela : r})

#Filtrar e mostrar um registro, considerando a tabela e por qual coluna filtrar
@app.route('/filter/<tabela>/<coluna>/<valor>')
def getTableFilter(tabela, coluna, valor):
    con = mysql.connect()
    cur = con.cursor()

    cur.execute('''select * from proximo_db.{} where {} = "{}"'''.format(tabela, coluna,valor))
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    
    cur.close()
    con.close()
    
    return jsonify({tabela : r})

#Inserir registros em uma tabela
@app.route('/insert/<tabela>', methods=['GET', 'POST', 'PUT'])
def insert(tabela):
    json_ob = request.json
    
    values = ""
    columns = ""
    
    for item in json_ob:
    	values = values + "'{}',".format(json_ob.get("{}".format(item)))
    	columns = columns + "{},".format(item)
   	
   	con = mysql.connect()
    cur = con.cursor()
    
    cur.execute('''insert into proximo_db.{} ({}) values ({})'''.format(tabela, columns[:-1], values[:-1]))
    con.commit()
    
    cur.close()
    con.close()
    
    return jsonify({tabela : json_ob})

#Atualizar um registro de alguma tabela, partindo de uma coluna de identificacao
@app.route('/edit/<tabela>/<id_tab>', methods=['GET', 'POST', 'PUT'])
def edit(tabela, id_tab):
    json_ob = request.json
    
    edit = ""
    
    for item in json_ob:
    	edit = edit + "{} = '{}',".format(item, json_ob.get("{}".format(item)))
   	
   	con = mysql.connect()
    cur = con.cursor()
    
    cur.execute('''update proximo_db.{} set {} where id = {}'''.format(tabela, edit[:-1], id_tab))
    con.commit()
    
    cur.close()
    con.close()
    
    return jsonify({tabela : json_ob})

#Autenticacao via api
@app.route('/auth', methods=['GET'])
def auth():
    con = mysql.connect()
    cur = con.cursor()

    user = request.args.get('user')
    passw = request.args.get('pass')
    
    cur.execute('''select * from proximo_db.Usuario where user = "{}" and senha = "{}"'''.format(user, passw))
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    
    cur.close()
    con.close()
    
    return jsonify({'auth' : r})

if __name__ == '__main__':  
    app.run()