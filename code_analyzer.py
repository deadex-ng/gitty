#set environment to clone remote repo
#install wily
#run wily to analyze code
#wily produces html report
#turn html to json
#send json data
import subprocess
import html_to_json
from  git import Repo
from pathlib import Path
import os

def set_localenv(repo_url):
    """
      Function to set the environment for cloning repo
    """
    home_dir = Path.home()
    repo_name = repo_url.split("/")[-1]
    clone_dir = os.path.join(home_dir, repo_name)
    Repo.clone_from(repo_url + ".git",clone_dir)

def get_wily_report():
    """
      Function to run wily and return report in html
    """
    build = subprocess.run(['wily', 'build', 'gitty'])

    if build.returncode == 0:
        print("Build successful")
        report = subprocess.run(['wily','report','--format','HTML', 'app.py'])
        if report.returncode == 0:
            print("Report generated")
        else:
            print(report.error)
    else:
        print(build.error)
    return build

def get_json_report():
    """
      Function to generate report in json
    """
    html = open("/root/gitty/wily_report/index.html","r")
    table = html_to_json.convert_tables(html)
    return table

#get_wily_report()
#html_t_json()
set_localenv('https://github.com/deadex-ng/UserAnalyticsTelecom')
