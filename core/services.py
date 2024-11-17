import requests

# function to check pnr status
def check_pnr_status(pnr_number):
    url = "https://irctc1.p.rapidapi.com/api/v3/getPNRStatus"

    querystring = {"pnrNumber":pnr_number}

    headers = {
        "x-rapidapi-key": "a461fde803msh91913946d3b364fp1cf3d6jsnb689b24fccff",
        "x-rapidapi-host": "irctc1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json()
        print("Response Data:", data)

        # Check if critical fields exist to determine PNR validity
        pnr_data = data.get("data", {})
        pnr_number_in_response = pnr_data.get("Pnr")
        train_no = pnr_data.get("TrainNo")
        passenger_status = pnr_data.get("PassengerStatus", [])

        if pnr_number_in_response and train_no and passenger_status:
            # PNR exists and contains passenger status information
            print(f"PNR {pnr_number} is valid.")
            #get_train_schedule(train_no)
            return train_no
        else:
            # Critical data is missing; assume PNR is invalid
            print(f"PNR {pnr_number} is invalid.")
            return None
    else:
        print("Failed to retrieve PNR status:", response.status_code, response.text)
        return None
    
def get_train_schedule(train_number):
    url = "https://irctc1.p.rapidapi.com/api/v1/getTrainSchedule"

    querystring = {"trainNo":train_number}

    headers = {
        "x-rapidapi-key": "a461fde803msh91913946d3b364fp1cf3d6jsnb689b24fccff",
        "x-rapidapi-host": "irctc1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json()
        train_data = data.get("data", {})
        train_stations = train_data.get("route", [])
        stations = []
        for station in train_stations:
            station_name = station.get("station_name")
            stations.append(station_name)
            
        print(stations)
        #print("Train Schedule Data:", train_stations)
        return True
    else:
        print("Failed to retrieve Train Schedule:", response.status_code, response.text)
        return False

    #print(response.json())

# function to verify if the route covers sender and recipient stations and if they fall between traveler's origin and destination
def verify_route(origin, destination, pnr_number, sender_origin, sender_destination):
    # check pnr and get train number
    train_no = check_pnr_status(pnr_number)

    if not train_no:
        return False, "Invalid PNR Number."
    
    # fetch train route
    train_route = get_train_schedule(train_no)

    if not train_route:
        return False, "Unable to return train schedule."
    
    try:
        # get indices of traveler, sender, and recipient stations
        traveler_origin_index = train_route.index(origin)
        traveler_destination_index = train_route.index(destination)
        sender_station_index = train_route.index(sender_origin)
        recipient_station_index = train_route.index(sender_destination)

        # ensure sender and recipient stations fall between the traveler's origin and destination
        if traveler_origin_index <= sender_station_index < recipient_station_index <= traveler_destination_index:
            print("The sender and recipient stations are valid and fall between the traveler's stations and PNR is valid.")
            return True, "The sender and recipient stations are valid and fall between the traveler's stations and PNR is valid."
        else:
            print("The sender and recipient stations do not fall between the traveler's stations but PNR is valid.")
            return False, "The sender and recipient stations do not fall between the traveler's stations but PNR is valid."
        
    except ValueError:
        # one or more stations not found in train route
        print("One or more stations are not found in the train route.")
        return False, "One or more stations are not found in the train route." 