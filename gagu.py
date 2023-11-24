from flask import Flask, render_template, request, redirect, url_for
import json

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

current_image = {'url': "https://source.unsplash.com/random/512x512?monster,vfx,horror",
	'votes': {'yes': 0, 'no': 0}
	}

@app.route('/')
def index():
    return render_template('index.html', image=current_image)

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
    app.run(debug=False, port=42066)

