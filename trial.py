from flask import Flask, make_response, jsonify,request

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

if __name__ == "__main__":
    webapp.run('0.0.0.0', port=2333)  #ssl_context=('ssl/cert.pem', 'ssl/key.pem')

