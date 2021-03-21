from flask import Flask, make_response, jsonify,request
from db_utils import update_db, get_entire_table, get_latest_row,fetch_today,update_day_data,get_month,get_day,get_year

webapp = Flask(__name__)
webapp.debug=False
def fetch_today():
    obj={"name":"Bence","age":20}
    return obj
@webapp.route('/today',methods=["GET"])
def today():
    today=fetch_today()
    json_day=jsonify(today)
    resp=make_response(json_day,200)
    return resp

@webapp.route('/month',methods=["GET"])
def monthData():
    data=get_month(int(request.args.get('year',default="2021")),int(request.args.get('month',default="3")))
    data=ConvertSumData(data)
    json_data=jsonify(data)
    resp=make_response(json_data,200)
    return resp
@webapp.route('/year',methods=["GET"])
def yeardata():
    data=get_year(int(request.args.get('year',default=2021)))
    data=ConvertSumData(data)
    json_data=jsonify(data)
    resp=make_response(json_data,200)
    return resp

def ConvertSumData(data):
    if data[0][0]==None:
        return [0,0,0,0]
    return [int(data[0][0]),int(data[0][1]),int(data[0][2]),int(data[0][3])]
if __name__ == "__main__":
    webapp.run('0.0.0.0', port=2333)  #ssl_context=('ssl/cert.pem', 'ssl/key.pem')

