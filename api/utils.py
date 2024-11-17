stationOrder = ['patna', 'banglore', 'jammu', 'goa','guna']

def isStationBetween(station, origin, destination, station_list=stationOrder):
    try:
        origin_index = station_list.index(origin)
        destination_index = station_list.index(destination)
        station_index = station_list.index(station)
        return origin_index <= station_index <= destination_index
    except ValueError:
        return False