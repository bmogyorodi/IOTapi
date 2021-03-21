
# ---------------------------------------------------------------------------
# Pelion Device Management SDK
# (C) COPYRIGHT 2017 Arm Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# --------------------------------------------------------------------------
"""Example showing basic usage of device resource subscriptions."""
from mbed_cloud import ConnectAPI
from mbed_cloud.exceptions import CloudAsyncError as CloudError
from db_utils import update_db, get_entire_table, get_latest_row,fetch_today,update_day_data
import pickle
import threading
import time
from flask import Flask, make_response, jsonify,request
from statistics import mode 
webapp = Flask(__name__)
webapp.debug=False
MOTION_RESOURCE = "/3200/0/4401"
SavedMotion=[]
lasttime=0
filename = 'finalized_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))

@webapp.route('/')
def last_move():
    global SavedMotion
    if  len(SavedMotion)==0:
        return "Motion Tracking hasn't begun!"
    class_label=str(int(loaded_model.predict([SavedMotion[-1]])[0]))
    if class_label=="11":
        return "Running"
    if class_label=="4":
        return "Walking"
    if class_label=="9":
        return "Cycling"
    if class_label=="10":
        return "Jogging"
    return class_label

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

@webapp.route('/debug',methods=["GET"])
def debugData():
    global SavedMotion
    resp=make_response(str(len(SavedMotion)),200)
    return resp

def _current_val(value):
    # Print the current value
    print("Current value: %r" % (value))
                

def _subscription_handler(device_id, path, value):
    global SavedMotion
    global lasttime
    try:
        decoded=value.decode("utf-8").split('?')[0]
        lasttime=time.time()
        data_array=decoded.split(',')
        data_array=[float(i)/104.5 for i in data_array[0:3]]+[float(i)/2000 for i in data_array[3:]]
        if len(data_array)!=0:
            SavedMotion.append(data_array)
            print(data_array)
    except UnicodeDecodeError:
        print("Unicode error, decoding failed")
    

def Subscribe(api,mainDevice):
    try:
        api.delete_subscriptions()
        api.add_resource_subscription_async(mainDevice.id, MOTION_RESOURCE, _subscription_handler)
    except:
        print("Connection error, retry later")
def StartAPI():
    webapp.run('0.0.0.0', port=2333) #ssl_context='adhoc'
def MinuteToDB():
    global SavedMotion
    time.sleep(60)
    if len(SavedMotion)<60:
        print("Check connection!")
    else:
        class_label=str(int(mode(loaded_model.predict(SavedMotion))))
        if class_label=="11":
            update_day_data("running") 
        if class_label=="4":
            update_day_data("walking") 
        if class_label=="9":
            update_day_data("cycling") 
        if class_label=="10":
            update_day_data("jogging")
        print("1 minute of"+class_label+"saved to DB!")
    SavedMotion=[]
    MinuteToDB()

def _main():
    global lasttime
    api = ConnectAPI()
    api.start_notifications()
    # calling start_notifications is required for getting/setting resource synchronously
    devices = api.list_connected_devices().data
    if not devices:
        raise Exception("No connected devices registered. Aborting")
    mainDevice=devices[-1]
    isActive=True
    lasttime=time.time()
    Subscribe(api,mainDevice)
    t = threading.Thread(target=StartAPI)
    t.start()
    t2=threading.Thread(target=MinuteToDB)
    t2.start()
    while True:   
        if time.time()-lasttime>3:    
            print("Attempt reconnect!")
            Subscribe(api,mainDevice)


if __name__ == "__main__":
    _main()
    
