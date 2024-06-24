import csv
from datetime import datetime, timedelta
from amadeus import Client, ResponseError

# Initialize Amadeus client
amadeus = Client(
    client_id='UGtfcPaxEoZ0pYAjQ8AHSlsOAoAujiYj',
    client_secret='284W2J39pXUiapNB'
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
        print(f"Error retrieving flight offers: {e}")
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
                # Extract departure and arrival times
                departure_time = segment['departure']['at']
                arrival_time = segment['arrival']['at']
                # Calculate flight time
                flight_time = (datetime.fromisoformat(arrival_time) - datetime.fromisoformat(departure_time)).total_seconds() / 3600
                parsed_data.append({
                    'Date': departure_date,
                    'Origin': segment['departure']['iataCode'],
                    'Destination': segment['arrival']['iataCode'],
                    'Last Ticketing Date': departure_date,
                    'Departure Time': departure_time,
                    'Arrival Time': arrival_time,
                    'Flight Time (hrs)': flight_time,
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
for origin, destination in airport_pairs:
    # Iterate over each departure date from May 1, 2023, to May 1, 2024
    start_date = datetime(2024, 5, 1)
    end_date = datetime(2024, 5, 3)
    delta = timedelta(days=1)
    while start_date <= end_date:
        print(f"Processing {origin} to {destination} for {start_date.strftime('%Y-%m-%d')}...")
        flight_offers = get_flight_offers(origin, destination, start_date)
        print(flight_offers)
        if flight_offers:
            parsed_data = parse_flight_offers(flight_offers)
            csv_data.extend(parsed_data)
        start_date += delta

# Export data to CSV file
csv_columns = ['Date', 'Origin', 'Destination', 'Last Ticketing Date','Departure Time','Arrival Time', 'Price', 'Validating Airline Code', 'Cabin Class']
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
