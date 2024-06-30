from flask import Flask, jsonify, request
import collector

app = Flask(__name__)

# Przykładowe dane - w rzeczywistym środowisku użyj bazy danych
events = [
    {"timestamp": "test", "description": "Description test"}
]


@app.route('/events', methods=['GET'])
def get_events():
    return jsonify(events)


@app.route('/save_event', methods=['POST'])
def save_events():
    data = request.get_data(as_text=True)
    lines_of_data = data.splitlines()
    for line in lines_of_data:
        collector.save_event_to_db(line)
    return "Event saved successfully!"


if __name__ == '__main__':
    app.run(debug=True)
