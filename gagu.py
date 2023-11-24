from flask import Flask, render_template, request, redirect, url_for
import json
import requests

app = Flask(__name__)

# File to store user submissions
submissions_file = 'submissions.json'

def load_submissions():
    try:
        with open(submissions_file, 'r') as file:
            submissions = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        submissions = {"yes": 0, "no": 0, "submissions": []}
    return submissions

def save_submissions(submissions):
    with open(submissions_file, 'w') as file:
        json.dump(submissions, file)

def get_final_image_url():
    base_url = "https://source.unsplash.com/random?monster,horror"
    
    # Make a request to the Unsplash /random page to get a random image
    response = requests.get(base_url, allow_redirects=False)
    
    # Check if the request was redirected
    if response.status_code == 302 and 'Location' in response.headers:
        # Extract the final URL after following redirects
        final_image_url = response.headers['Location']
        return final_image_url
    else:
        # If the request fails or there is no redirect, return None
        return None
current_image = {'url': "",
	'votes': {'yes': 0, 'no': 0}
	}

@app.route('/')
def index():
    url = get_final_image_url()
    current_image['url'] = url
    return render_template('index.html', image=current_image)

@app.route('/results')
def results():
    # Load existing submissions
    submissions = load_submissions()

    # Calculate total votes
    total_yes = submissions['yes']
    total_no = submissions['no']

    return render_template('results.html', results={'yes': total_yes, 'no': total_no, 'submissions': submissions['submissions']})



@app.route('/vote', methods=['POST'])
def vote():
    user_vote = request.form.get('vote')

    # Check if the user has entered a valid vote
    if user_vote in ['yes', 'no']:
        current_image['votes'][user_vote] += 1

        # Load existing submissions
        submissions = load_submissions()

        # Add current vote to submissions
        submissions['submissions'].append({"url": current_image['url'], "vote": user_vote})

        # Update total counts
        submissions[user_vote] += 1

        # Save submissions
        save_submissions(submissions)

        return redirect(url_for('index'))
    else:
        return "Invalid vote, please enter 'yes' or 'no'."

if __name__ == '__main__':
    app.run(debug=False, port=42066, host="0.0.0.0")

