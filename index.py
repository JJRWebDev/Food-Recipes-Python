__author__ = 'Evil'

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flaskext.mysql import MySQL

app = Flask(__name__)

# Conexión a base de datos
mysql = MySQL() 
app.config['MYSQL_DATABASE_USER'] = '' #user
app.config['MYSQL_DATABASE_PASSWORD'] = '' #password
app.config['MYSQL_DATABASE_DB'] = '' #database
app.config['MYSQL_DATABASE_HOST'] = '' #host
mysql.init_app(app) #connect mysql
conn = mysql.connect()



@app.route('/')

def home():
    conn = mysql.connect() #cursor to mysql 
    cur = conn.cursor() 
    cur.execute('SELECT * FROM `recipe`;') #query
    resultados = cur.fetchall() #results    
    return render_template('home.html', recetas = resultados)

@app.route('/recipes')

def recipes():
    return render_template('recipes.html')

@app.route('/viewrecipe/<string:id>')

def viewrecipe(id):
    conn = mysql.connect() #cursor to mysql 
    cur = conn.cursor() 
    cur.execute('SELECT `id_recipe` as `ID_RECETA`, `name` as `NOMBRE_RECETA`, `pic` as `IMAGEN_RECETA`, `Recipe_Notes` as `HINTS` FROM `recipe` WHERE `id_recipe` = {0}'.format(id)) #query
    resultados = cur.fetchall() #results
    cur.execute('SELECT `pasos`.`id_recipe` as `ID_RECETA`, `pasos`.`step` as `STEP` FROM `foodygoodie`.`pasos` INNER JOIN `foodygoodie`.`recipe` ON `pasos`.`id_recipe` = `recipe`.`id_recipe` WHERE `recipe`.`id_recipe` = {0}'.format(id)) #query
    pasos = cur.fetchall() #results
    cur.execute('SELECT `ingredient`.`id_ingredient` as `ID_INGREDIENTE`, `ingredient`.`name` as `NOMBRE_INGREDIENTE`, `ingredient`.`symbol` as `ICON_INGR`, `ingredient_category`.`categoria` as `CATEGORIA`, `recipe_ingredient`.`cantidad` as `CANTIDAD`, `recipe_ingredient`.`Peso` as `PESO` FROM `foodygoodie`.`ingredient`, `foodygoodie`.`ingredient_category`, `foodygoodie`.`recipe_ingredient` WHERE `ingredient`.`id_cat` = `ingredient_category`.`id_cat` AND `recipe_ingredient`.`id_ingredient` = `ingredient`.`id_ingredient` AND `recipe_ingredient`.`id_recipe` = {0}'.format(id)) #query
    ingredientes = cur.fetchall()
    return render_template('view.html', recetasel = resultados, pasos = pasos, ingredientesel = ingredientes)

@app.route('/new')

def new():
    conn = mysql.connect() #cursor to mysql 
    cur = conn.cursor() 
    cur.execute('SELECT `ingredient`.`id_ingredient` as `ID_INGREDIENTE`, `ingredient`.`name` as `NOMBRE_INGREDIENTE`, `ingredient`.`symbol` as `ICON_INGR`, `ingredient_category`.`categoria` as `CATEGORIA` FROM `foodygoodie`.`ingredient`, `foodygoodie`.`ingredient_category` WHERE `ingredient`.`id_cat` = `ingredient_category`.`id_cat`;') #query
    resultados = cur.fetchall() #results
    return render_template('new.html', ingredientes = resultados)

@app.route('/lab', methods=['POST'])

def lab():
    if request.method == 'POST':
        """
        {
            "Ingre1": "3_1_1", 
            "Ingre2": "15_1_1", 
            "Ingre3": "27_1_1", 
            "RECIPEDESC": "Esta es la famosa receta de l Ali Oli.", 
            "RECIPENAME": "Receta de Ali Oli", 
            "Step1": "Mezclar el aceite de oliva y el ajo", 
            "Step2": "Anadimos unas gotas de limon", 
            "Step3": "Anadimos el huevo y batimos"
        }
        """
        RECNAME = request.form['RECIPENAME']
        RECDESC = request.form['RECIPEDESC']
        conn = mysql.connect() #cursor to mysql 
        cur = conn.cursor()

        #Insertamos la receta:
        cur.execute('INSERT INTO `recipe` (`name`, `Recipe_Notes`) VALUES (%s, %s)', (RECNAME, RECDESC)) #query
        conn.commit()

        #Obtenemos el ID:
        cur.execute('SELECT MAX(id_recipe) FROM recipe') #query
        resultados = cur.fetchall() #results
        recipedata = resultados[0][0]

        #Almaceno los pasos y los ingredientes en tupla para insertarlos:
        parametros = request.form
        for parametro in parametros:
            if parametro[0:4] == 'Step':
                    cur.execute('INSERT INTO `pasos` (`id_recipe`, `step`) VALUES (%s, %s)', (recipedata, request.form[parametro])) #query
                    conn.commit()
            elif parametro[0:5] == 'Ingre':
                cadena = request.form[parametro]
                separador = "_"
                ing_split = cadena.split(separador)
                cur.execute('INSERT INTO `recipe_ingredient` (`id_recipe`, `cantidad`, `id_ingredient`, `Peso`) VALUES (%s, %s, %s, %s)', (recipedata, ing_split[1], ing_split[0], ing_split[2])) #query
                conn.commit()
        #if parametro != 'RECIPENAME' and parametro != 'RECIPEDESC':
        #Insertaremos los pasos y los ingredientes a continuación:
        #return jsonify(request.form.to_dict())
    return redirect(url_for('/new'))

@app.route('/about')

def about():
    return render_template('about.html')

#@app.route('/datos', methods=['POST']) # receive form data here method post
#def datos():

#    if request.method == 'POST':
        #usergiven = request.form['usergiven'] #data
        #pswgiven = request.form['pswgiven']
#        conn = mysql.connect() #cursor to mysql 
#        cursor = conn.cursor() 
#        cursor.execute('SELECT * FROM `ingredient`;') #query
        #return str(cursor.fetchall()) #results
#        resultados = cursor.fetchall() #results
#        return render_template('home.html', ingredients = resultados)   
    #return render_template('datos.html')

if __name__ == '__main__':
    app.run(debug=True)