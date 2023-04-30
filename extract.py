import csv
import requests

csv_filename = 'gun.csv'

# Open the CSV file
with open(csv_filename, 'r') as csvfile:
    reader = csv.DictReader(csvfile)

    # Extract the column names
    columns = reader.fieldnames

    # Extract the data from the CSV
    data = list(reader)



    for row in data:
        locations = row['location'].split(',')
        row['city']=locations[0].strip()
        row['state']=locations[1].strip()

        state = row['state']

        # Make a request to the Google Search API to fetch coordinates
        # Replace 'API_KEY' with your actual API key
        api_key = 'AIzaSyAn5zgznNL13mpM1uJ1V1wbao7ENoAqQOI'
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={state}&key={api_key}"
        response = requests.get(url)

        # Parse the response and extract the coordinates
        if response.status_code == 200:
            result = response.json()
            if result['status'] == 'OK':
                coordinates = result['results'][0]['geometry']['location']
                row['Coordinate-N'] = f"{coordinates['lat']}"
                row['Coordinate-W'] = f"{coordinates['lng']}"

    new_columns = ['city','state', 'Coordinate-N', 'Coordinate-W']

    # Create a new data structure with the additional columns
    new_data = []
    for column in columns:
        new_data.append({column: '' for column in columns + new_columns})
    output_filename = 'output_file.csv'

    # Write the data to the output CSV file
    with open(output_filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns + new_columns)
        writer.writeheader()
        writer.writerows(data)
