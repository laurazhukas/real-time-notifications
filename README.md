# real-time-notifications

**Purpose**: There's nothing worse than having to leave that 10-20 min buffer when you travel. Life is unpredictable, but with Smart Alarm you're better prepared and have more time for the things that matter.

**What it does**: Notifications that update in real time, taking into account traffic delays. The user specifies events they have and then the alarm will calculate the amount of time it takes a user to get to a destination. If there is traffic on route the alarm will update and alert the user earlier.

# Running
In order to run the program you will need to add a `GOOGLE_API_KEY` into the `TrafficAPI.py` file, as well as the serverConfig in `DataBase.py`. After these have both been added you must specify the user id of the user you would like to sign into on line 41 of `main.py`. Finally, you can run the program using `python3 main.py`.

# Creating mock data
In `MockData.py` specify the user details as well as the events you would like to add to the user. Then run `python3 MockData.py`

# Background on calculations
Within `main.py` multiple calcualtions are performed to determine how the alarm should update. In `main()` we begin by obtaining the user object from the DB, then the destination address and origin address are used to determine the typical time it takes for a user to travel between the two destinations (uses Google DistanceMatrix API without live traffic updates). 

Then the time at which API must be called is determined in `calculate_api_call()`. In this function the overall buffer time is calculated by looking at how long the user specified it would take them to get ready, the usual travel time and half of the usual travel time is also added. The assumption behind adding half of the travel time is that is it very unlikely that the time it takes to get to your destination will double in value (with the exception of very short trips ex. 10 min drive). After the buffer time has been calculated the call time is returned based on the specified event start time and the buffer.

The default alarm time is set by taking into account the buffer time and the usual travel time. Afterwards the program begins to iterate over the current time. Once the current time has reached the time the `api_call_time`, the API is called and the delay with live traffic is calculated, after which the alarm is updated. In order to prevent continuous API calls the api call time is updated at most four times. Within `calculate_api_call()` when `api_time` is passed in it will recalculate the new `api_call_time`.

After the alarm time has been updated according to the live traffic delays, it waits to sound the alarm and alert the user that it is time to prepare for their event.
