from amadeus import Client, ResponseError

amadeus = Client(
    client_id = 'BH2FM1RPZ1arymI7C26RsgnWMGS8gzJH',
    client_secret = 'yDG248YxWpPrnBsJ'
)

try:
    
    response = amadeus.shopping.flight_offers_search.get(
        originLocationCode='MAD',
        destinationLocationCode='ATH',
        departureDate='2024-11-01',
        adults=1,
        max=2)
    print(response.data)

except ResponseError as error:
    print("Error:", error)
    print("Response body:", error.response_body)