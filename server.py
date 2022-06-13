from flask import Flask, g, render_template, request, redirect, url_for, jsonify
import json
import psycopg2
import db


app = Flask(__name__)
# import after making app -- this is important the way I have db.py setup

@app.before_first_request
def init():
    db.setup()


@app.route('/')
def frontPage():
    return render_template('firstPage.html')

@app.route('/survey')
def survey():
    return render_template('survey.html')

@app.route('/thanks',methods=['POST'])
def thanks():
    name1= request.form.get('name')
    type= request.form.get('type')
    region1=request.form.get('optionsRadios')
    kanto=request.form.get('kanto11')
    
    with db.get_db_cursor(True) as cur:
        cur.execute("INSERT INTO pokemon (name1, type1, region, ta) VALUES (%s,%s,%s,%s);",(name1,type,region1,kanto))
        
        return render_template('thank.html')
    
    #return render_template('thank.html', name1=name1, type=type, region1=region1, kanto=kanto)

@app.route('/decline')
def decline():
    return render_template('thanksAny.html')

@app.route('/api/results',methods=['GET'])
def results():
    
    with db.get_db_cursor(True) as cur:
        cur.execute("SELECT * FROM pokemon;")
        rolls = cur.fetchall()
        if(request.args.get("reverse",default="False",type=str)=="true"):
            rolls.reverse()
        return jsonify(rolls)

@app.route('/admin/summary',methods=['GET'])
def summary():
    
    with db.get_db_cursor(True) as cur:
        cur.execute("SELECT * FROM pokemon;")
        rolls = cur.fetchall()
        names=[]
        polls=[]
        for i in range(0,len(rolls)):
            names.append(rolls[i][1])
            polls.append(rolls[i][4])
        return render_template("admin.html", rolls=names,polls=polls )
'''
@app.route('/roll',methods=['GET'])
def viewRolls():
    
    with db.get_db_cursor(False) as cur:
        cur.execute("SELECT roll_id, roll_memo, roll_config, roll_result FROM roll;")
        rolls = cur.fetchall()
        return render_template("all_rolls.html", rolls=rolls)

@app.route('/roll', methods=['POST'])
def doRoll():
    roll_config = request.form.get('roll_config', 'd6')
    memo = request.form.get('roll_memo', 'nobody')
    result = dice.roll(roll_config, raw=True)
    roll_result_long = dice.utilities.verbose_print(result)
    roll_result = int(result.result)

    with db.get_db_cursor(True) as cur:
        cur.execute("insert into roll (roll_memo, roll_config, roll_result_long, roll_result) values (%s,%s,%s,%s) returning roll_id;", (memo, roll_config, roll_result_long, roll_result))
        id = cur.fetchone()
        id = id[0]
        return redirect(url_for("viewRollDetails", roll_id = id))

@app.route('/roll/<roll_id>')
def viewRollDetails(roll_id):
    with db.get_db_cursor() as cur:
        # NO -- since I use a dictCursor over in db.py you can use the rows as dictionaries OR tuples.
        cur.execute("SELECT roll_id, roll_memo, roll_config, roll_result, roll_result_long FROM roll where roll_id = %s;", (roll_id,))
        roll = cur.fetchone()
        return render_template("one_rolls.html", roll=roll)
'''
if __name__ == '__main__':
    app.run()