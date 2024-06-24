import csv
from collections import defaultdict
from amadeus.client.decorator import Decorator
from amadeus import Client, ResponseError



class DirectDestinations(Decorator, object):
    def get(self, **params):
        '''
        Returns airport direct routes.

        .. code-block:: python

            amadeus.airport.direct_destinations.get(
                            departureAirportCode='BLR')

        :param departureAirportCode: the departure Airport code following
            IATA standard. ``"BLR"``, for example for Bengaluru

        :rtype: amadeus.Response
        :raises amadeus.ResponseError: if the request could not be completed
        '''
        return self.client.get('/v1/airport/direct-destinations', **params)

amadeus = Client(
    client_id = 'BH2FM1RPZ1arymI7C26RsgnWMGS8gzJH',
    client_secret = 'yDG248YxWpPrnBsJ'
)

direct_destinations = DirectDestinations(amadeus)

# Read the list of airport IATA codes from the file
with open('airport_codes1.txt', 'r') as file:
    airport_iata_codes = file.read().splitlines()

# Create a defaultdict to store the direct destinations for each airport
airport_destinations = defaultdict(set)

# Iterate over each airport IATA code
for airport_code in airport_iata_codes:
    try:
        # Get direct destinations for the current airport
        response = direct_destinations.get(departureAirportCode=airport_code)
        destinations = response.data

        # Add unique destination IATA codes to the airport_destinations dictionary
        for destination in destinations:
            airport_destinations[airport_code].add(destination['destination']['iataCode'])
    except Exception as e:
        print(f"Error retrieving direct destinations for {airport_code}: {e}")

# Flatten the defaultdict and remove duplicate entries
flattened_destinations = [(airport_code, destination) for airport_code, destinations in airport_destinations.items() for destination in destinations]

# Export the pairs into a CSV file
with open('airport_direct_destinations.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['OriginAirport', 'DestinationAirport'])
    writer.writerows(flattened_destinations)

print("Airport direct destinations exported to airport_direct_destinations.csv")
