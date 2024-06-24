from amadeus import Client, ResponseError

amadeus = Client(
    client_id='BH2FM1RPZ1arymI7C26RsgnWMGS8gzJH',
    client_secret='yDG248YxWpPrnBsJ'
)

output_file = "airline_icao_codes2.txt"

try:
    response = amadeus.reference_data.airlines.get()
    airlines = response.data

    with open(output_file, "w") as file:
        for airline in airlines:
            icao_code = airline.get('icaoCode', 'N/A')
            business_name = airline.get('businessName', 'N/A')

            # Write the ICAO code to the output file
            if icao_code != 'N/A':
                file.write(f"{icao_code}\n")

            print(f"{business_name} - ICAO code: {icao_code}")

    print(f"ICAO codes of airlines exported to {output_file}")
except ResponseError as error:
    print("Error:", error)
