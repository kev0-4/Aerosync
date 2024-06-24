import csv
from datetime import datetime, timedelta
from amadeus import Client, ResponseError

# Initialize Amadeus client
amadeus = Client(
    client_id='BH2FM1RPZ1arymI7C26RsgnWMGS8gzJH',
    client_secret='yDG248YxWpPrnBsJ'
)

# Function to get flight offers for a given route and date
def get_flight_offers(origin, destination, departure_date):
    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin,
            destinationLocationCode=destination,
            departureDate=departure_date.strftime('%Y-%m-%d'),
            adults=1,
            max=2  # Adjust as needed
        )
        return response.data
    except ResponseError as e:
        print(f"Error retrieving flight offers for {origin} to {destination} on {departure_date.strftime('%Y-%m-%d')}: {e}")
        return None

# Function to parse flight offers and extract relevant information
def parse_flight_offers(flight_offers):
    parsed_data = []
    if not flight_offers:
        return parsed_data
    for offer in flight_offers:
        departure_date = offer.get('lastTicketingDate')
        price = offer.get('price', {}).get('total')
        validating_airline_codes = offer.get('validatingAirlineCodes', [])
        itineraries = offer.get('itineraries', [])
        for itinerary in itineraries:
            segments = itinerary.get('segments', [])
            for segment in segments:
                cabin_class = segment.get('cabin', 'Unknown')
                parsed_data.append({
                    'Date': departure_date,
                    'Origin': segment['departure']['iataCode'],
                    'Destination': segment['arrival']['iataCode'],
                    'Last Ticketing Date': departure_date,
                    'Price': price,
                    'Validating Airline Code': validating_airline_codes,
                    'Cabin Class': cabin_class
                })
    return parsed_data

# Read origin and destination airport codes from CSV
airport_pairs = []
with open('airport_direct_destinations_mini.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        airport_pairs.append((row['originLocationCode'], row['destinationLocationCode']))

# Collect and export data to CSV
csv_data = []
skip_next_iteration = False
for origin, destination in airport_pairs:
    # Skip iteration if flag is set
    if skip_next_iteration:
        skip_next_iteration = False
        continue
    
    # Iterate over each departure date from May 1, 2023, to May 1, 2024
    start_date = datetime(2023, 5, 1)
    end_date = datetime(2024, 2, 1)
    delta = timedelta(days=1)
    
    while start_date <= end_date:
        print(f"Processing {origin} to {destination} for {start_date.strftime('%Y-%m-%d')}...")
        flight_offers = get_flight_offers(origin, destination, start_date)
        
        if flight_offers:
            parsed_data = parse_flight_offers(flight_offers)
            if parsed_data:
                csv_data.extend(parsed_data)
                break  # Exit the loop if successful flight offers are retrieved
            else:
                # Set flag to skip next iteration of outer loop
                print(f"No valid flight data found for {origin} to {destination} on {start_date.strftime('%Y-%m-%d')}. Skipping next iteration.")
                skip_next_iteration = True
                break
        
        start_date += delta
    else:
        print(f"No flight offers found for {origin} to {destination}")

# Export data to CSV file
csv_columns = ['Date', 'Origin', 'Destination', 'Last Ticketing Date', 'Price', 'Validating Airline Code', 'Cabin Class']
csv_file = "flight_data.csv"
try:
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in csv_data:
            writer.writerow(data)
    print(f"CSV data successfully exported to {csv_file}")
except IOError:
    print("I/O error")
