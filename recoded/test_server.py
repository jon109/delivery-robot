import requests


# Send a POST request to the server to submit a number

# Send a GET request to the server to retrieve the submitted number

response = requests.post('http://jon10.pythonanywhere.com/state', json={'state': 1})
if response.status_code != 200:
    
    print('Error submitting number')
else:
    print('Number submitted successfully')