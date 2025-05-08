import requests
import pandas as pd
from datetime import datetime
import os

# API configuration
API_KEY = "a31850e8e37b74cf44a877ed72c095c7"
BASE_URL = "https://api.aviationstack.com/v1/flights"

# Phnom Penh airport codes
PNH_IATA = "PNH"
PNH_ICAO = "VDPP"

def get_flights(api_key, origin=None, destination=None):
    """
    Query the AviationStack API for flights with the specified origin or destination
    """
    params = {
        'access_key': api_key,
        'flight_status': 'landed',
        'limit': 100  # Adjust based on your needs
    }
    
    # Add filters for Phnom Penh airport
    if origin:
        params['dep_iata'] = origin
    if destination:
        params['arr_iata'] = destination
        
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching flight data: {e}")
        return None

def format_flight_data(data):
    """
    Extract and format the relevant flight information
    """
    flights = []
    
    if not data or 'data' not in data:
        return flights
    
    for flight in data['data']:
        # Safely get live aircraft data
        aircraft_iata = ''
        aircraft_icao = ''
        live_data = flight.get('live')
        if live_data and isinstance(live_data, dict):
            aircraft_data = live_data.get('aircraft')
            if aircraft_data and isinstance(aircraft_data, dict):
                aircraft_iata = aircraft_data.get('iata', '')
                aircraft_icao = aircraft_data.get('icao', '')
        
        flight_info = {
            # General info
            'flight_date': flight.get('flight_date', ''),
            'flight_status': flight.get('flight_status', ''),
            
            # Departure info
            'departure_airport': flight.get('departure', {}).get('airport', ''),
            'departure_iata': flight.get('departure', {}).get('iata', ''),
            'departure_icao': flight.get('departure', {}).get('icao', ''),
            'departure_delay': flight.get('departure', {}).get('delay', ''),
            'departure_scheduled': flight.get('departure', {}).get('scheduled', ''),
            'departure_estimated': flight.get('departure', {}).get('estimated', ''),
            'departure_actual': flight.get('departure', {}).get('actual', ''),
            
            # Arrival info
            'arrival_airport': flight.get('arrival', {}).get('airport', ''),
            'arrival_iata': flight.get('arrival', {}).get('iata', ''),
            'arrival_icao': flight.get('arrival', {}).get('icao', ''),
            'arrival_delay': flight.get('arrival', {}).get('delay', ''),
            'arrival_scheduled': flight.get('arrival', {}).get('scheduled', ''),
            'arrival_estimated': flight.get('arrival', {}).get('estimated', ''),
            'arrival_actual': flight.get('arrival', {}).get('actual', ''),
            
            # Airline info
            'airline_name': flight.get('airline', {}).get('name', ''),
            'airline_iata': flight.get('airline', {}).get('iata', ''),
            'airline_icao': flight.get('airline', {}).get('icao', ''),
            
            # Flight info
            'flight_number': flight.get('flight', {}).get('number', ''),
            'flight_iata': flight.get('flight', {}).get('iata', ''),
            'flight_icao': flight.get('flight', {}).get('icao', ''),
            
            # Aircraft info (using pre-extracted values)
            'aircraft_iata': aircraft_iata,
            'aircraft_icao': aircraft_icao
        }
        
        flights.append(flight_info)
    
    return flights

def display_flights_table(flights):
    """
    Display the flights in a nicely formatted table
    """
    if not flights:
        print("No flights found")
        return
    
    # Convert to DataFrame for easier handling
    df = pd.DataFrame(flights)
    
    # Format date and time fields
    for col in df.columns:
        if any(time_part in col for time_part in ['scheduled', 'estimated', 'actual']):
            df[col] = df[col].apply(lambda x: format_datetime(x) if x else '')
    
    # Create a more readable display with grouped columns
    print("\n=== FLIGHTS TO AND FROM PHNOM PENH ===\n")
    
    # Optionally save to CSV
    df.to_csv('phnom_penh_flights_landed_05.csv', index=False)
    print("\nData also saved to 'phnom_penh_flights_landed_05.csv'")

def format_datetime(dt_str):
    """Format datetime string for better readability"""
    if not dt_str:
        return ''
    try:
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M')
    except (ValueError, TypeError):
        return dt_str

def main():
    print("Fetching flights from Phnom Penh...")
    departures = get_flights(API_KEY, origin=PNH_IATA)
    
    print("Fetching flights to Phnom Penh...")
    arrivals = get_flights(API_KEY, destination=PNH_IATA)
    
    all_flights = []
    
    # Process departures
    if departures and 'data' in departures:
        departure_flights = format_flight_data(departures)
        all_flights.extend(departure_flights)
        print(f"Found {len(departure_flights)} departures from Phnom Penh")
    else:
        print("No departure data available or error occurred")
    
    # Process arrivals
    if arrivals and 'data' in arrivals:
        arrival_flights = format_flight_data(arrivals)
        all_flights.extend(arrival_flights)
        print(f"Found {len(arrival_flights)} arrivals to Phnom Penh")
    else:
        print("No arrival data available or error occurred")
    
    # Display consolidated results
    display_flights_table(all_flights)

if __name__ == "__main__":
    main()