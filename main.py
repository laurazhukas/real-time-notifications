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

    if api_time != None:
        typical_travel_time = event.travel_time
        eighth_time = typical_travel_time/8
        # the buffer time decreases as call time is updated to account for time passed
        overall_time_buffer = typical_travel_time + eighth_time*num_of_updates + event.buffer
        real_time = update_time(event.time, overall_time_buffer)

    else:
        # for inital api call, calculate number of seconds before departure when api must be called
        typical_travel_time = event.travel_time # travel time without delay
        # start calling api (take into account user get ready time, travel and add half travel)
        overall_time_buffer = typical_travel_time/2 + typical_travel_time + event.buffer
        print(f"Overall time buffer in api call {overall_time_buffer}")
        real_time = update_time(event.time, overall_time_buffer) # make api call time into datetime object

    return real_time

def main ():
    stop_api_update = False
    # "sign in" as user
    user = get_user("ID_VALUE")
    
    # pprint.pprint(user['events'][0]['name'])
    pprint.pprint(user['events'][0])
    # new_obj = Struct.Struct(**user['events'][0])
    new_obj = Struct.Struct(**user['events'][0])
    # print(type(new_obj.destination_address))
    alarm = False

    # today_events = current_user.get_events()
    # next_event = today_events.sort() # the next event for the user that requires a notification
    # next_event = current_user.events[0]
    next_event = new_obj

    usual_travel_time = TrafficAPI.get_travel_time(next_event, False) # call api to determine the average travel time (not delay)
    next_event.travel_time = usual_travel_time # here you store that value into the actual event - figure out later (might delte)
    print(usual_travel_time)
    
    # api_call_time is actual time at which the api needs to be called 
    api_call_time = calculate_api_call(next_event)
    number_of_api_updates = 4
    print(f"api_call_time: {api_call_time}")
    usual_travel_delay = usual_travel_time + next_event.buffer

    alarm_time = update_time(next_event.time, usual_travel_delay)  # calculate the regular alarm time (no delay)

    print(f"Alarm time : {alarm_time}")

    while alarm == False:
        current_time = datetime.datetime.now()

        if (current_time >= api_call_time) and not stop_api_update:
            travel_time_delay = TrafficAPI.get_travel_time(next_event, True) # gets the travel time with live traffic (seconds)
            departure_time_delay = travel_time_delay + next_event.buffer
            print("in current_ time")
            
            if departure_time_delay > next_event.travel_time:
                alarm_time = update_time(next_event.time, departure_time_delay + next_event.buffer) # update alarm time
                print("in update delay")

            # update the api call time so it is not continuatlly called
            api_call_time = calculate_api_call(next_event, api_call_time, number_of_api_updates)
            number_of_api_updates -= 1
            if(number_of_api_updates == 1): 
                stop_api_update = True
        
        if current_time >= alarm_time:
            print("Sound the Alarm")
            alarm = True
            #del today_events[0] # remove event from user's events on that day
            # need to call something that would rest everything (api call, next event, usual travel time)
        

if __name__ == "__main__":
    main()