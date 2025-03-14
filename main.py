from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Flask route to fetch country data from external API
@app.route('/get-countries', methods=['GET'])
def get_countries():
    external_api_url = "https://demo.jetworkflow.com/ims/jetapi.php?method=getRecords&key=7jZB5WVYlEqKiIhdw9KGhUikCXmAWHCj&id_form=48&project=demoleo"

    try:
        response = requests.get(external_api_url)
        data = response.json()

        # Extract country list
        countries = [item.get("country", "Unknown") for item in data.get("data", [])]

        return jsonify({"countries": countries})

    except Exception as e:
        return jsonify({"error": str(e), "countries": []}), 500


# Flask route to send data to external API
@app.route('/send-data', methods=['POST'])
def send_data():
    try:
        # Get JSON data from frontend
        user_data = request.json
        name = user_data.get("name")
        country = user_data.get("country")

        if not name or not country:
            return jsonify({"error": "Name and country are required"}), 400

        # External API endpoint
        external_api_url = "https://demo.jetworkflow.com/ims/jetapi.php?method=addRecord&key=c04f6fab7706a1dda30f7498b2774c7a&id_form=109&project=demoleo"

        # Prepare data for external API
        payload = {
            "name": name,
            "country": country
        }

        # Send POST request to external API
        response = requests.post(external_api_url, data=payload)

        # Check if request was successful
        if response.status_code == 200:
            return jsonify({"message": "Data sent successfully!"})
        else:
            return jsonify({"error": "Failed to send data", "details": response.text}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
