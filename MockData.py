import datetime
import Event
import User
from DataBase import create_new_user, add_event_to_user, get_user_id

def create_mock_data():
    first_name = "User"
    last_name = "Test"
    create_new_user(User.User(first_name, last_name))
    date = datetime.datetime(2020, 2, 5, 2, 30)
    destination_address = "7070 Henri Julien Ave, Montreal, Quebec H2S 3S3"
    origin_address = "490 Rue de la Gauchetière O, Montréal, QC H2Z 0B3"
    event = Event.Event("Run Errand", destination_address , origin_address, date , 0)
    id_num = get_user_id(first_name, last_name)
    add_event_to_user(id_num, event)

if __name__ == "__main__":
    create_mock_data()