from amadeus import Client, Location, ResponseError

amadeus = Client(
    client_id='30p6SGd1iGzHZdAHE4DEgxk9GFJ8sTlI',
    client_secret='cpnaHq3o3khOdGJX'
)

try:
    response = amadeus.reference_data.locations.get(
        keyword='LON',
        subType=Location.AIRPORT,
    )    
    print(response.data)
except ResponseError as error:
    print(error)
