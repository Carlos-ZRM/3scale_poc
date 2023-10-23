from flask import Flask, jsonify, request
import os  # Import the os module
import requests


app = Flask(__name__)

# Define the coordinates for Greenland (You can adjust this if needed)
latitude = 71.7069
longitude = -42.6043
nasa_api_url = 'https://worldview.earthdata.nasa.gov/earthdata/clouds.json?C=I&REQUEST=GetCoverage&SERVICE=WCS'

def get_public_ip():
    client_ip = request.remote_addr  # Get the public IP address of the client
    return jsonify({'public_ip': client_ip})

@app.route('/get_location', methods=['GET'])
def get_location():
    client_ip = request.remote_addr  # Get the public IP address of the client
    print(client_ip)
    # Use ipinfo.io to get location information
    ipinfo_url = f'http://ipinfo.io/{client_ip}/json'
    ipinfo_response = requests.get(ipinfo_url)
    location_data = ipinfo_response.json()

    # Extract latitude and longitude
    lat, lon = location_data.get('loc', ',').split(',')

    return jsonify({
        'latitude': lat,
        'longitude': lon,
    })

@app.route('/get_weather_and_ice_data', methods=['GET'])
def get_weather_and_ice_data():
    try:
        # Read the API key from an environment variable
        openweathermap_api_key = os.environ.get('OPENWEATHERMAP_API_KEY')

        if not openweathermap_api_key:
            return jsonify({'error': 'OpenWeatherMap API key not found in environment variable.'}), 500
        
        latitude = str(request.args.get('latitude'))
        longitude = str(request.args.get('longitude'))

        if latitude is None or longitude is None:
            return jsonify({'error': 'Latitude and longitude parameters are required.'}), 400

        # Convert latitude and longitude to float
        latitude = float(latitude)
        longitude = float(longitude)
        # Fetch weather data from OpenWeatherMap
        weather_url = f'http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={openweathermap_api_key}'
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()
        # Get the temperature from the weather data
        temperature_kelvin = weather_data['main']['temp']
        temperature_celsius = temperature_kelvin - 273.15

        # Fetch ice cover data from NASA Worldview
        nasa_params = {
            'request': 'GetCoverage',
            'service': 'WCS',
            'COVERAGE': 'MODIS_Terra_CorrectedReflectance_TrueColor',
            'CRS': 'EPSG:4326',
            'format': 'image/png',
            'width': 512,
            'height': 512,
            'bbox': f'{longitude-1},{latitude-1},{longitude+1},{latitude+1}',
        }
        nasa_response = requests.get(nasa_api_url, params=nasa_params)
        print("nasa_response",  nasa_response.json())
        # Calculate the percentage of ice cover (you may need to adapt this based on the specific data you retrieve)
        ice_cover_percentage = (nasa_response.content.count(b'\x00') / 512 / 512) * 100

        # Create a JSON response
        response_data = {
            'temperature_celsius': temperature_celsius,
            'ice_cover_percentage': ice_cover_percentage,
        }


        return jsonify(response_data)

    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Error during the API request.'}), 500

    except KeyError as e:
        return jsonify({'error': 'Data not found in the API response.'}), 500

@app.route('/get_weather_and_ice_data_mongo', methods=['GET'])
def get_weather_and_ice_data_mongo():
    try:
        # Read the API key from an environment variable
        openweathermap_api_key = os.environ.get('OPENWEATHERMAP_API_KEY')
        mongo_host = os.environ.get('MONGO_HOST')
        mongo_port = int(os.environ.get('MONGO_PORT'))
        mongo_db_name = os.environ.get('MONGO_DB_NAME')
        if not openweathermap_api_key:
            return jsonify({'error': 'OpenWeatherMap API key not found in the environment variable.'}), 500

        # Get latitude and longitude from the request parameters
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')

        if latitude is None or longitude is None:
            return jsonify({'error': 'Latitude and longitude parameters are required.'}), 400

        # Convert latitude and longitude to float
        latitude = float(latitude)
        longitude = float(longitude)

        # Fetch weather data from OpenWeatherMap
        weather_url = f'http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={openweathermap_api_key}'
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()

        # Fetch ice cover data from NASA Worldview
        nasa_params = {
            'request': 'GetCoverage',
            'service': 'WCS',
            'COVERAGE': 'MODIS_Terra_CorrectedReflectance_TrueColor',
            'CRS': 'EPSG:4326',
            'format': 'image/png',
            'width': 512,
            'height': 512,
            'bbox': f'{longitude-1},{latitude-1},{longitude+1},{latitude+1}',
        }
        nasa_response = requests.get(nasa_api_url, params=nasa_params)

        # Calculate the percentage of ice cover (you may need to adapt this based on the specific data you retrieve)
        ice_cover_percentage = (nasa_response.content.count(b'\x00') / 512 / 512) * 100

        # Store the data in MongoDB
        weather_data_entry = {
            'timestamp': datetime.now(),
            'latitude': latitude,
            'longitude': longitude,
            'weather_response': weather_data,
            'nasa_response': nasa_response.content.decode('utf-8')
        }
        mongo_db.weather_data.insert_one(weather_data_entry)

        # Create a JSON response
        response_data = {
            'temperature_celsius': weather_data['main']['temp'],
            'ice_cover_percentage': ice_cover_percentage
        }

        return jsonify(response_data)

    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Error during the API request.'}), 500

    except KeyError as e:
        return jsonify({'error': 'Data not found in the API response.'}), 500

@app.route('/get_antarctica_ice_cover', methods=['GET'])
def get_antarctica_ice_cover():
    try:
        # Define the coordinates for Antarctica
        antarctica_latitude = -90
        antarctica_longitude = 0

        # Fetch ice cover data for Antarctica from NASA Worldview
        nasa_params = {
            'request': 'GetCoverage',
            'service': 'WCS',
            'COVERAGE': 'MODIS_Terra_CorrectedReflectance_TrueColor',
            'CRS': 'EPSG:4326',
            'format': 'image/png',
            'width': 512,
            'height': 512,
            'bbox': f'{antarctica_longitude-10},{antarctica_latitude-10},{antarctica_longitude+10},{antarctica_latitude+10}',
        }
        nasa_response = requests.get(nasa_api_url, params=nasa_params)
        print("nasa_response" , str(nasa_response.content))
        # Calculate the percentage of ice cover for Antarctica (you may need to adapt this based on the specific data you retrieve)
        ice_cover_percentage = (nasa_response.content.count(b'\x00') / 512 / 512) * 100

        # Create a JSON response
        response_data = {
            'ice_cover_percentages': ice_cover_percentage,
        }

        return jsonify(response_data)

    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Error during the API request.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
