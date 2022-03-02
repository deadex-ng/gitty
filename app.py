import json
import base64
import requests
from requests.auth import HTTPBasicAuth
from pprint import pprint
from github import Github
from flask import Flask, jsonify

app = Flask(__name__)

# We use the route() decorator to tell Flask what URL
# should trigger our function.
@app.route('/<username>')
def profile_data(username):
    """
    The function to return user profile data

    Parameters:
       usernane (str): The githun username
    
    Returns:
        user_data: A json object with user profile data
    """
    url = f"https://api.github.com/users/{username}"
    user_data = requests.get(url).json()
    return user_data

@app.route('/<username>/repos')
def get_all_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    repos = requests.get(url).json()
    return jsonify(repos)

@app.route('/repos/<username>/<repo>')
def repo_metadata(username, repo):
    """
    The function to return repository metadata

    Parameters:
       usernane (str): The githun username
       repo (str): The github repository
    
    Returns:
        repo_data: A json object with repository metadata
    """
    url = f"https://api.github.com/repos/{username}/{repo}"
    repo_data = requests.get(url).json()
    return repo_data

@app.route('/repos/<username>/<repo>/<token>/traffic')
def repo_traffic(username,repo,token):
    """
    The function to return repository traffic adata

    Parameters:
       usernane (str): The githun username
       repo (str): The github repository
       token (str): Github token
    
    Returns:
        traffic_data: A json object with repository traffic adata
    """
    traffic = {}
    g = Github(token)
    repo = g.get_repo(username + "/" + repo)
    clones = repo.get_clones_traffic(per="day")
    views = repo.get_views_traffic(per="day")

    traffic["clones_count"] = clones['count']
    traffic["clones_unique"] = clones['uniques']
    traffic["views_count"] = views['count']
    traffic["views_unique"] = views['uniques']
    #traffic_data = json.dumps(traffic)
    return jsonify(traffic)
# main driver function
if __name__ == "__main__":
    # run() method of Flask class runs the
    # application on the local development server.
    app.run(debug=True)
    


