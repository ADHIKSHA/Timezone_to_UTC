#import all the necessary libraries
from run import app
from flask import request
from flask import Response
from http import HTTPStatus
import datetime
import json
import pytz

# define function that would be called when route "/" is accessed.
@app.route("/",methods= ['GET'])
def convert():
	# try and except block to get all the Request arguments.
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
		return response      # return error response
	# try and except block to convert given Time into UTC
	try:
		if Timezone == "" and hour == "" and minute == "":	#if no arguments are provided the local time is converted to UTC
			from datetime import timezone
			dt = datetime.datetime.now(timezone.utc)       # Get the current local time
			utc_time = dt.replace(tzinfo=timezone.utc)     # Convert current time to UTC
			message= "Time = {:d}:{:02d} UTC".format(utc_time.hour, utc_time.minute) # display hour and minute from UTC
			response = app.response_class(
    			response=json.dumps({"message" : message}),
    			status=200,
    			mimetype='application/json')
			return response           # return success response

		else:  # if arguments are provided
			timestr= "2017-05-30T"+str(hour)+":"+str(minute)+":00Z" # create a datetime string with provided hour and minute
			Ntime = datetime.datetime.strptime (timestr, "%Y-%m-%dT%H:%M:%SZ") # Convert given string to datetime object
			tmz = pytz.timezone(Timezone) # Get the timezone object in pytz
			Ntime= tmz.localize(Ntime) # localize the datetime object with the given timezone
			UTCtime = Ntime.astimezone(pytz.utc) # convert the datetime object to UTC
			message= "Time = {:d}:{:02d} UTC".format(UTCtime.hour, UTCtime.minute) # display hour and minute from UTC
			response = app.response_class(    
				response=json.dumps({"message" : message}),
				status=200,
				mimetype='application/json')
			return response               # return success response

	except Exception as e:
		message ="An error occured. Please check the data provided and try again!\n The error is: "+str(e)
		response = app.response_class(
			response=json.dumps({"message" : message}),
			status=400,
			mimetype='application/json')
		return response                   # return error response
