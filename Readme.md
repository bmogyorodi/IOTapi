Fitness tracker api connected to pelion manager device:
Create .env to declare MBED_CLOUD_SDK_API_KEY with your pelion manager accounts api key to use
Reset MOTION resource in Pelion for 

ML notebook containing algorithm to create model based on movement data
Logistic regression appears to be the most effective

Create mysql tb: moveTracker with table moveset: (day:DATE,running:INT,jogging:INT,cycling:INT,walking:INT)
Create user READER with permission to Insert, Select and Update database to use api (no need for any other permissions)

python libraries needed:
numpy
scikit learn
pandas
mbed_cloud_sdk
pymysql
flask

