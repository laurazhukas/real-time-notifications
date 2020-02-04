class User:

    def __init__(self, first_name : str, last_name : str, distance_units = 'metric', home_address = None, work_address = None, time = None):
        self.first_name = first_name
        self.last_name = last_name
        self.units = distance_units # API default for units is 'metric' other option is 'imperial'
        self.events = []
        self.id = 0
        # other posible parameters:
        '''
        self.home = home_address
        self.work = work_address
        self.buffer_time = time # the time it takes a user to get ready in the morning
        '''        