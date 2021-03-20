from flask import Flask, make_response, jsonify,request
from db_utils import update_db, get_entire_table, get_latest_row,fetch_today,update_day_data
from threading import Thread

webapp = Flask(__name__)
webapp.debug=False


@webapp.route('/history', methods=["GET"])
def history():
    table = get_entire_table()
    print(table)
    json_table = jsonify(table)
    resp = make_response(json_table, 200)
    return resp

@webapp.route('/today',methods=["GET"])
def today():
    today=fetch_today()
    json_day=jsonify(today)
    resp=make_response(json_day,200)
    return resp
@webapp.route('/update',methods=["GET"])
def update():
    update=update_day_data(request.args.get('move',default="running"))
    return update
    
@webapp.route("/latest_mean_std", methods=["GET"])
def latest_data():
    row = get_latest_row()
    json_row = jsonify(row)
    resp = make_response(json_row, 200)
    return resp


if __name__ == "__main__":
    #t = Thread(target=update_db)
    #t.start()
    webapp.run('127.0.0.1', port=2333) #