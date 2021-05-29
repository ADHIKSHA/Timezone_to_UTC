from run import app
from flask import request
from flask import Response
from http import HTTPStatus
import datetime
import json
import pytz

@app.route("/",methods= ['GET'])
def convert():
	try:
		Timezone = request.args.get("tz", default= "", type = str)
		hour = request.args.get("hr" , default= "", type= str)
		minute = request.args.get("min", default= "", type= str)
	except Exception as e:
		message ="The data provided is not in the proper format. Please check and try again!"+str(e)
		response = app.response_class(
			response=json.dumps({"message" : message}),
			status=400,
			mimetype='application/json')
		return response

	try:
		if Timezone == "" and hour == "" and minute == "":
			from datetime import timezone
			dt = datetime.datetime.now(timezone.utc)
			utc_time = dt.replace(tzinfo=timezone.utc)
			strUTC =utc_time.strftime("%d.%m.%y %H:%M:%S")
			message= "Time = {:d}:{:02d} UTC".format(utc_time.hour, utc_time.minute)
			response = app.response_class(
    			response=json.dumps({"message" : message}),
    			status=200,
    			mimetype='application/json')
			return response

		else:
			timestr= "2017-05-30T"+str(hour)+":"+str(minute)+":00Z"
			Ntime = datetime.datetime.strptime (timestr, "%Y-%m-%dT%H:%M:%SZ")
			tmz = pytz.timezone(Timezone)
			Ntime= tmz.localize(Ntime)
			UTCtime = Ntime.astimezone(pytz.utc)
			strUTC = UTCtime.strftime("%d.%m.%y %H:%M:%S")
			message= "Time = {:d}:{:02d} UTC".format(UTCtime.hour, UTCtime.minute)
			response = app.response_class(
				response=json.dumps({"message" : message}),
				status=200,
				mimetype='application/json')
			return response

	except Exception as e:
		message ="An error occured. Please check the data provided and try again!\n The error is: "+str(e)
		response = app.response_class(
			response=json.dumps({"message" : message}),
			status=400,
			mimetype='application/json')
		return response
