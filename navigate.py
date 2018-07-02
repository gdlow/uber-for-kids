import requests
import json
import time
import datetime
import polyline

pickup_loc='3.158125,101.751688'
dest_loc='3.1616321,101.7537138'
driver_loc='3.1329117,101.6761341'

maps_APIKey = 'xxxxxxxxxxxx'
cred = {'key':maps_APIKey}

URL = 'https://maps.googleapis.com/maps/api/directions/json'

def get_url(url,payload=None):
    payload.update(cred)
    response = requests.get(url, params=payload)
    content = response.content.decode('utf8')
    return content

def get_json_from_url(url,payload=None):
    content = get_url(url,payload)
    js = json.loads(content)
    return js


def getQuickestPath(origin=driver_loc,pickup=pickup_loc,dest=dest_loc,passengerList=['3.156282,101.745894','3.1581304,101.7494993','3.151714,101.745328'],dropOffTime=1518996606):
    pathInfo={}
    poly_coord=[]
    passengerList.append(pickup_loc)
    passengers=''
    origin=driver_loc
    destination=dest_loc
    mode='driving'
    for passenger in passengerList:
        passengers+='|'
        passengers+=passenger
    payload = {'origin':origin, 'destination':destination,'arrival_time':dropOffTime, 'mode':mode, 'waypoints':'optimize:true'+passengers}
    js = get_json_from_url(URL,payload)

    poly_points=polyline.decode(js['routes'][0]['overview_polyline']['points'])
    for poly_point in poly_points:
        poly_coord.append({'latitude':poly_point[0],'longitude':poly_point[1]})
    timeToDestination=dropOffTime-time.time()
    arrival_est=str(datetime.timedelta(seconds=(timeToDestination)))
    wait_time=predictDriverArrival(pickup_loc,js['routes'][0],timeToDestination)
    pathInfo = {'polylines':poly_coord,'arrival_est':arrival_est, 'wait_time':wait_time}

    return pathInfo

def predictDriverArrival(pickup,route,timeToDestination):
    coord = pickup.split(',')
    duration=0
    total_travel_time=0
    min=999
    lat = float(coord[0])
    lon = float(coord[1])
    rel_wait_time = 0
    legs=route['legs']
    for i in range(len(legs)):
        total_travel_time+=legs[i]['duration']['value']
        if ((legs[i]['start_location']['lat']+legs[i]['start_location']['lng']-lat-lon)<min):
            min=(legs[i]['start_location']['lat']+legs[i]['start_location']['lng']-lat-lon)
            rel_wait_time = total_travel_time

    abs_wait_time = timeToDestination - (total_travel_time - rel_wait_time)
    return str(datetime.timedelta(seconds=(abs_wait_time)))
