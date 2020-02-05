import User
import Event
import datetime
import TrafficAPI
import pprint
import Struct
from DataBase import get_user

def update_time(event_time, seconds_delay):
    return event_time - datetime.timedelta(seconds = seconds_delay)

def create_datetime_object(year:int, month:int, day:int, hour:int, minute:int):
    return datetime.datetime(year, month, day, hour, minute)

def calculate_api_call(event, api_time = None, num_of_updates = 0):
    '''
        Updates api_call_time when a value for api_time is passed in 
        Otherwise for inital api call, it calculates the number of seconds before departure when api must be called
    '''
    
    if api_time != None:
        typical_travel_time = event.travel_time
        eighth_time = typical_travel_time/8
        # the buffer time decreases as call time is updated to account for time passed
        overall_time_buffer = typical_travel_time + eighth_time*num_of_updates + event.buffer
        real_time = update_time(event.time, overall_time_buffer)

    else:
        typical_travel_time = event.travel_time # travel time without delay
        # calculate buffer with get ready time, travel and add half of travel time
        overall_time_buffer = typical_travel_time/2 + typical_travel_time + event.buffer
        print(f"Overall time buffer in api call {overall_time_buffer}")
        real_time = update_time(event.time, overall_time_buffer) # make api call time into datetime object

    return real_time

def main ():
    stop_api_update = False
    number_of_api_updates = 4
    alarm = False 
    user = get_user("ID_VALUE") # "sign in" as user
    pprint.pprint(user['events'][0])
    next_event = Struct.Struct(**user['events'][0]) # convert dict returned to Struct object 

    next_event.travel_time = TrafficAPI.get_travel_time(next_event, False) # call api to determine the average travel time (not delay)
    api_call_time = calculate_api_call(next_event) # get time at which the api needs to be called 
    print(f"api_call_time: {api_call_time}")
    usual_travel_delay = next_event.travel_time + next_event.buffer

    alarm_time = update_time(next_event.time, usual_travel_delay)  # calculate the regular alarm time (no delay)
    print(f"Alarm time : {alarm_time}")

    while alarm == False:
        current_time = datetime.datetime.now()

        if (current_time >= api_call_time) and not stop_api_update:
            travel_time_delay = TrafficAPI.get_travel_time(next_event, True) # gets the travel time with live traffic (seconds)
            departure_time_delay = travel_time_delay + next_event.buffer
            alarm_time = update_time(next_event.time, departure_time_delay + next_event.buffer) # update alarm time
            print(f"Alarm time updated to: {alarm_time}")

            # update the api call time so it is not continuatlly called
            api_call_time = calculate_api_call(next_event, api_call_time, number_of_api_updates)
            print(f"API call time updated to: {api_call_time}")
            number_of_api_updates -= 1
            if(number_of_api_updates == 1): 
                stop_api_update = True
        
        if current_time >= alarm_time:
            print("Sound the Alarm")
            alarm = True


if __name__ == "__main__":
    main()