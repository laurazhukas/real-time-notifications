import User
import Event
import datetime
import TrafficAPI

stop_api_update = False

def update_time(event_time, seconds_delay):
    # adds certain 
    return event_time - datetime.timedelta(seconds = seconds_delay)

def create_datetime_object(year:int, month:int, day:int, hour:int, minute:int):
    return datetime.datetime(year, month, day, hour, minute)

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
    alarm = False
    # login in as user or create a new user (implement later)
    # create events for a user
    # login means just grab events for that user today and the next day (or have a check in the while)
    current_user = User.User("Laura", "Test")
    date = create_datetime_object(2020, 2, 4, 14, 20)
    current_user.events.append(Event.Event("Wake Up", "Toronto, ON", "Burlington, ON", date ,10))
    # current_user.events.append(Event.Event("Wake Up", "Toronto, ON", "Burlington, ON", date ,10))
    # today_events = current_user.get_events()
    # next_event = today_events.sort() # the next event for the user that requires a notification
    next_event = current_user.events[0]
    usual_travel_time = TrafficAPI.get_travel_time(next_event, False) # call api to determine the average travel time (not delay)
    next_event.travel_time = usual_travel_time # here you store that value into the actual event - figure out later (might delte)
    print(usual_travel_time)
    # api_call_time is actual time at which the api needs to be called 
    api_call_time = calculate_api_call(next_event)
    usual_travel_delay = usual_travel_time + next_event.buffer

    alarm_time = update_time(next_event.time, usual_travel_delay)  # calculate the regular alarm time (no delay)

    print(f"Alarm time : {alarm_time}")

    while alarm == False:
        current_time = datetime.datetime.now()

        # this is when you check delay in travel time
        if current_time <= api_call_time:
            # gets the travel time with live traffic (returns seconds for entire travel)
            travel_time_delay = TrafficAPI.get_travel_time(next_event, True)
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
            #del today_events[0] # remove event from user's events on that day
            # need to call something that woud rest everything (api call, next event, usual travel time)
        

if __name__ == "__main__":
    main()