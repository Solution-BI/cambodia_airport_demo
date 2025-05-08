# Cambodia Airport Demo

This project fetches flight information from the AviationStack API, extracting data on both departing and arriving flights at Phnom Penh International Airport. The collected data is stored in an Excel table. Additionally, the project includes reference datasets such as airline, airport, and other related information.

## Features

- Fetches flights information using the aviationstack API.
- Extracts full flight events from API URLs.
- Saves flight events to a Excel file.

## Data Model

The logical data model below outlines the relationships between key entities such as Flights, Scheduled FLight, Aircraft, Airline, and Airports.

![Logical Data Model](docs/Cambodia%20Airport%20Data%20Modeling%20-%20Logical%20Data%20Model.png)

## Prerequisites

- Python 3.8 or higher
- Aviationstack account
- Aviationstack API key

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```

2. Install the required Python packages:
   ```bash
   pip install requests, pandas
   ```

## Usage

1. Run the script:
   ```bash
   python aviationstack_flights.py
   ```

2. The script will:
   - Fetch flight events from the aviationstack API for the specified filter (eg. flight_status).
   - Extract full flight events content.
   - Save the flight events as `phnom_penh_flights_landed_05.csv` in the same directory.

## Requirements

The following Python packages are required and listed above:

- `requestsn`
- `pandas`

## File Structure

- `aviationstack_flights.py`: The main script for fetching, processing, and storing the flight events.
- `phnom_penh_flights_landed_05.csv`: The CSV file where flight events are saved locally.
- `data folder`: Store the rest of the referential datasets such as aircraft, airline, airport, scheduled flight, and fact flight
- `docs folder`: Logical data model of the project

## Acknowledgments

- [Aviationstack API](https://aviationstack.com/documentation) for providing the flight data.
