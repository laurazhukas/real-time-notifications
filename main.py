import User
import Event
import requests
import json
import datetime

GOOGLE_API_KEY = ""
stop_api_update = False

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def generate_user_id():
    return -1

def create_new_user():
    return 1

def update_time(event_time, seconds_delay):
    # adds certain 
    return event_time - datetime.timedelta(seconds = seconds_delay)

def create_datetime_object(year:int, month:int, day:int, hour:int, minute:int):
    return datetime.datetime(year, month, day, hour, minute)

def get_travel_time(event, get_traffic_time):
    if(get_traffic_time):
        parameters = {
            "origins": event.origin_address,
            "destinations": event.destination_address,
            "key": GOOGLE_API_KEY,
            "mode": "driving",
            "departure_time": "now",
            # "traffic_model": "best_guess"
        }
        print("in get traffic time")

    else:
        parameters = {
            "origins": event.origin_address,
            "destinations": event.destination_address,
            # "units" : "metric",
            "key": GOOGLE_API_KEY,
        }
    response = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?", params = parameters)
    jprint(response.json())
    if get_traffic_time:
        time = response.json()['rows'][0]['elements'][0]['duration_in_traffic']['value']
    else:
        time = response.json()['rows'][0]['elements'][0]['duration']['value'] # duration of travel, duration must be changed to duration in traffic
    return time # in seconds

def calculate_api_call(event, api_time = None):

    if api_time != None:
        #update the api call time
        # for now just make it stop after one iteration
        stop_api_update = True

    else:
        # for inital api call, calculate number of seconds before departure when api must be called
        typical_travel_time = event.travel_time # travel time without delay
        # start calling api (take into account user get ready time, travel and add half travel)
        overall_time_buffer = typical_travel_time/2 + typical_travel_time + event.buffer
        print(f"Overall time buffer in api call {overall_time_buffer}")
        real_time = update_time(event.time, overall_time_buffer) # make api call time into datetime object

    return real_time


def main ():
    print(datetime.datetime.now())
    alarm = False
    # login in as user or create a new user (implement later)
    # create events for a user
    # login means just grab events for that user today and the next day (or have a check in the while)
    current_user = User.User("Laura", "Test")
    date = create_datetime_object(2020, 2, 4, 14, 20)
    current_user.events.append(Event.Event("Wake Up", "Toronto, ON", "Burlington, ON", date ,10))
    #today_events = current_user.get_events()
    #next_event = today_events.sort() # the next event for the user that requires a notification
    next_event = current_user.events[0]
    usual_travel_time = get_travel_time(next_event, False) # call api to determine the average travel time (not delay)
    next_event.travel_time = usual_travel_time # here you store that value into the actual event - figure out later (might delte)
    print(usual_travel_time)
    # api_call_time is actual time at which the api needs to be called 
    api_call_time = calculate_api_call(next_event)
    usual_travel_delay = usual_travel_time + next_event.buffer

    alarm_time = next_event.time - datetime.timedelta(seconds = usual_travel_delay) # calculate the regular alarm time (no delay)

    print(f"Alarm time : {alarm_time}")

    while alarm == False:
        current_time = datetime.datetime.now()

        # this is when you check delay in travel time
        if current_time <= api_call_time:
            # gets the travel time with live traffic (returns seconds for entire travel)
            travel_time_delay = get_travel_time(next_event, True)
            departure_time_delay = travel_time_delay + next_event.buffer
            print("in current_ time")
            if(not stop_api_update):
                # reset api call time so its not called constatly
                # api_call_time = calculate_api_call(self, next_event, api_call_time)
                stop_api_update = True
        
            if departure_time_delay > next_event.travel_time:
                # update notification time
                alarm_time = update_time(next_event.time, departure_time_delay + next_event.buffer)
                print("in update delay")
        
        if current_time >= alarm_time:
            print("sound the alarm")
            alarm = True
            # add remove event from that user on that day
        

if __name__ == "__main__":
    main()