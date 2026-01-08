# --- Configuration for Data Collection ---
TRACKED_AIRLINES = ['AA', 'DL', 'UA'] # Airlines you want to track
TRACKED_ROUTES = [
    {'origin': 'BOS', 'destination': 'LAX'},
    {'origin': 'JFK', 'destination': 'SFO'},
    # Add more routes as needed
]
# The specific departure date you are tracking (e.g., 15 days from now)
DEPARTURE_DATE = date(2025, 6, 15) # YYYY, M, D

# Collection Schedule (how often to poll for testing in Colab)
# For a full day of tracking, you'd extend this or run it in a loop.
# For demo, let's simulate a few collection times across a shorter period.
COLLECTION_TIMES_UTC = [
    datetime(2025, 6, 1, 10, 0, 0), # June 1st, 10:00 AM UTC
    datetime(2025, 6, 1, 12, 0, 0), # June 1st, 12:00 PM UTC
    datetime(2025, 6, 1, 14, 0, 0)  # June 1st, 02:00 PM UTC
]

# Amadeus API Specifics
NUMBER_OF_ADULTS = 1
TRAVEL_CLASS = 'ECONOMY' # We'll primarily focus on Economy for PE_Current
MAX_OFFERS_PER_SEARCH = 10 # Number of flight offers to retrieve per search

# Data Storage
OUTPUT_CSV_FILE = 'amadeus_flight_data_collection.csv'

# --- Helper Function to Process Amadeus Response ---
def process_amadeus_response(response_data, current_collection_timestamp, observation_id_start):
    """
    Parses Amadeus Flight Offers Search response and extracts relevant data.
    Returns a list of dictionaries, each representing a row in our dataset.
    """
    observations = []
    current_obs_id = observation_id_start

    if not response_data:
        return [], current_obs_id

    for offer in response_data:
        # We'll take the first itinerary for simplicity in this example
        # Real-world: you might process all itineraries or filter more rigorously
        if not offer.get('itineraries') or not offer['itineraries'][0].get('segments'):
            continue # Skip invalid offers

        itinerary = offer['itineraries'][0]
        segments = itinerary['segments']
        first_segment = segments[0]
        last_segment = segments[-1] # For arrival airport/time of the last segment

        try:
            # Core Identifiers & Time
            # Note: Flight_Unique_ID should represent the unique *instance* of a scheduled flight
            # A single flight number might have multiple offers at different prices.
            # Here, we're taking the first flight number in the itinerary.
            flight_number_str = first_segment.get('number', 'UNKNOWN')
            carrier_code = first_segment.get('carrierCode', 'UNK')
            origin_iata = first_segment.get('departure', {}).get('iataCode', 'UNK')
            destination_iata = last_segment.get('arrival', {}).get('iataCode', 'UNK')
            departure_datetime_str = first_segment.get('departure', {}).get('at')

            # Ensure departure_datetime_str is valid before parsing
            if not departure_datetime_str:
                print(f"Warning: Skipping offer due to missing departure_datetime: {offer}")
                continue

            departure_datetime_obj = datetime.fromisoformat(departure_datetime_str.replace('Z', '+00:00')) # Ensure timezone aware for parsing

            flight_unique_id = (
                f"{carrier_code}{flight_number_str}_"
                f"{origin_iata}{destination_iata}_"
                f"{departure_datetime_obj.strftime('%Y%m%d%H%M')}" # Use precise time for unique ID
            )

            # Pricing
            pe_current = float(offer.get('price', {}).get('grandTotal', 0.0))

            # PF_Current is complex: would need separate search for BUSINESS/FIRST class
            # For now, it's None.
            pf_current = None # Requires separate search or sophisticated parsing

            # Aircraft Type Code - can be challenging to get consistently from offers search
            aircraft_type_code = first_segment.get('aircraft', {}).get('code', 'UNKNOWN')

            # --- Construct Data Point ---
            data_point = {
                'Observation_ID': current_obs_id,
                'Flight_Unique_ID': flight_unique_id,
                'Collection_Timestamp': current_collection_timestamp.isoformat(),
                'Departure_DateTime': departure_datetime_obj.isoformat(),
                'Airline_Code': carrier_code,
                'Route': f"{origin_iata}-{destination_iata}",
                'Origin_Airport_Code': origin_iata,
                'Destination_Airport_Code': destination_iata,
                'Flight_Number': flight_number_str,
                'Aircraft_Type_Code': aircraft_type_code,
                'Number_of_Stops': len(segments) - 1,
                'PE_Current': pe_current,
                'PF_Current': pf_current, # Placeholder
                'Price_Bucket_1': pe_current * 0.8, # Synthetic placeholder for first bucket
                'Price_Bucket_2': pe_current * 0.9, # Synthetic placeholder for second bucket

                # --- Placeholder for Amadeus-derived competitive pricing ---
                # These will be calculated *after* collecting all relevant offers from competitors
                'CP_Cheapest_Flight_Price': None,
                'CP_Avg_Bucket_Fare': None,

                # --- Placeholder for Derived & Engineered Features (calculate after collection) ---
                'DT_Days_to_Departure': (departure_datetime_obj.date() - current_collection_timestamp.date()).days,
                'DT_Hours_to_Departure': (departure_datetime_obj - current_collection_timestamp).total_seconds() / 3600,
                'Departure_Hour_UTC': departure_datetime_obj.hour,
                'Departure_Day_of_Week': departure_datetime_obj.weekday(),
                'Collection_Hour_of_Day_UTC': current_collection_timestamp.hour,
                'Weekday_Morning': 1 if current_collection_timestamp.weekday() < 5 and 6 <= current_collection_timestamp.hour <= 10 else 0,
                'Weekend_Night': 1 if current_collection_timestamp.weekday() >= 5 and 20 <= current_collection_timestamp.hour <= 23 else 0,

                # --- Placeholder for other Amadeus or External Data (currently not collected) ---
                'Total_Aircraft_Seats': None,
                'AS_Total': None,
                'AS_Economy': None,
                'AS_First': None,
                'Booked_Seats_Economy': None,
                'Booked_Seats_First': None,
                'BR_Economy': None,
                'BR_First': None,
                'CPV_Lowest_Price_Volatility': None,
                'CPV_Avg_Price_Volatility': None,
                'RC_Num_Competitors': None, # Will fill this after all searches for a route/time
                'RC_Weighted_Index': None,
                'ER_Deviation_Ratio': None,
                'ET_Daily_Target_Ratio': None,
                'Total_Booked_Seats_for_Day': None,
                'SFPI_Avg_Load_Factor': None,
                'SFPI_Avg_Price_Deviation': None,
                'SFPI_Avg_Booking_Rate': None,
                'Temp_Dest_C': None,
                'Oil_Price_USD': None,
                'Fuel_Cost_Index': None,
                'Interest_Limit_Score': None,
                'UE_Score': None,
                'SE_Score': None,
                'CE_Score': None,
                'ANIS_Score': None,
                'Social_Media_Sentiment_Score': None,
            }
            observations.append(data_point)
            current_obs_id += 1

        except Exception as e:
            print(f"Error processing offer: {e}. Offer data: {offer}")
            continue # Skip to the next offer if one fails

    return observations, current_obs_id


# --- Main Data Collection Loop ---
all_flight_observations = []
observation_id_counter = 1
MIN_DELAY_BETWEEN_CALLS_SECONDS = 0.5 # To avoid hitting rate limits

print(f"Starting data collection for flights departing on {DEPARTURE_DATE}...")

for collection_ts in COLLECTION_TIMES_UTC:
    print(f"\n--- Collecting data at: {collection_ts.isoformat()} ---")

    # Store offers for this specific collection time to calculate competitive pricing later
    offers_at_this_time = {} # Key: route_str, Value: list of offers

    for route in TRACKED_ROUTES:
        origin = route['origin']
        destination = route['destination']
        route_key = f"{origin}-{destination}"

        print(f"  Searching for {origin}-{destination} on {DEPARTURE_DATE}...")

        try:
            # Make the Amadeus Flight Offers Search API call
            # We are not filtering by airline in the search, because we want to see all competitors
            # and then filter/process them.
            response = amadeus.shopping.flight_offers.search.get(
                originLocationCode=origin,
                destinationLocationCode=destination,
                departureDate=DEPARTURE_DATE.isoformat(),
                adults=NUMBER_OF_ADULTS,
                travelClass=TRAVEL_CLASS,
                max=MAX_OFFERS_PER_SEARCH # Limit the number of offers to retrieve
            )

            if response.data:
                # Store raw offers for competitive analysis
                offers_at_this_time.setdefault(route_key, []).extend(response.data)

                # Process and append to main list (for individual flight data)
                new_observations, observation_id_counter = process_amadeus_response(
                    response.data, collection_ts, observation_id_counter
                )
                all_flight_observations.extend(new_observations)
                print(f"    Collected {len(new_observations)} individual flight observations.")
            else:
                print(f"    No flight offers found for {route_key} at {collection_ts}.")

        except ResponseError as e:
            print(f"  Amadeus API Error for {route_key}: {e} (HTTP {e.response.status_code})")
            if e.response.status_code == 429: # Rate limit exceeded
                print("    Rate limit hit. Waiting for 60 seconds...")
                time.sleep(60) # Wait a bit longer
            # Decide on retry logic here if needed
        except Exception as e:
            print(f"  An unexpected error occurred for {route_key}: {e}")

        time.sleep(MIN_DELAY_BETWEEN_CALLS_SECONDS) # Small delay between each search

    # --- After collecting all offers for a given collection_ts, calculate competitive pricing ---
    for route_k, offers_list in offers_at_this_time.items():
        all_prices_for_route = []
        unique_airlines_for_route = set()

        for offer_data in offers_list:
            if offer_data.get('price', {}).get('grandTotal'):
                all_prices_for_route.append(float(offer_data['price']['grandTotal']))
            if offer_data.get('itineraries') and offer_data['itineraries'][0].get('segments'):
                unique_airlines_for_route.add(offer_data['itineraries'][0]['segments'][0]['carrierCode'])

        if all_prices_for_route:
            cheapest_flight_price = min(all_prices_for_route)
            avg_bucket_fare = sum(all_prices_for_route) / len(all_prices_for_route)
            num_competitors = len(unique_airlines_for_route)
        else:
            cheapest_flight_price = None
            avg_bucket_fare = None
            num_competitors = 0

        # Now, update the observations that belong to this route and collection_ts
        for obs in all_flight_observations:
            if obs['Route'] == route_k and obs['Collection_Timestamp'] == collection_ts.isoformat():
                obs['CP_Cheapest_Flight_Price'] = cheapest_flight_price
                obs['CP_Avg_Bucket_Fare'] = avg_bucket_fare
                obs['RC_Num_Competitors'] = num_competitors
        print(f"  Updated competitive pricing for {route_k}.")


print("\nData collection complete for specified period.")

# --- Convert to DataFrame and Save ---
if all_flight_observations:
    df = pd.DataFrame(all_flight_observations)
    df.to_csv(OUTPUT_CSV_FILE, index=False)
    print(f"Data saved to {OUTPUT_CSV_FILE}")
    print("\n--- Sample Data (first 5 rows) ---")
    print(df.head().to_markdown(index=False)) # Use to_markdown for better display in Colab
    print(f"\nTotal observations collected: {len(df)}")
else:
    print("No observations collected.")