import requests
from datetime import datetime, timedelta
import json
BASE_URL = "http://test-ticket.gofromir.local"

'''Доступ к API'''
CONFIG = {
    "login": "reports_portal",
    "password": "PEJjZuSp"
}

def get_auth_access():
    url = "http://test-ticket.gofromir.local/assets/components/helpdesk/action.php?auth=1"
    response = requests.post(url, json=CONFIG)
    if response.status_code == 200:
        token = response.json().get("object").get("token")
        print("good")
        return {"Api-Token": f"{token}"}
    return "Error"

'''1 таблица'''
def data_app(period):
    auth = get_auth_access()
    period_iso = {
        "date1": str(datetime.fromisoformat(period.get("date1")).timestamp()).split(".")[0],
        "date2": str(datetime.fromisoformat(period.get("date2")).timestamp()).split(".")[0]
    }
    response = requests.get(f"http://test-ticket.gofromir.local/rest/orders?filter[createdon:gt]={period_iso.get('date1')}&filter[createdon:lt]={period_iso.get('date2')}", headers=auth).json()
    tasks = []
    for task in response.get("results"):
        tmp = [task.get("id"), task.get("Data").get("status"), task.get("pagetitle"), requests.get(f"http://test-ticket.gofromir.local/rest/contacts?filter[id]={task.get('Data').get('contact')}", headers=auth).json().get("results")[0].get("name"),
                   task.get("Data").get("createdon")]
        if task.get("Data").get("startedon"):
            tmp.append(f"с {task.get('Data').get('startedon')}")
        else:
            tmp.append("-")
        if task.get("Data").get("finishedon"):
            date_obj = datetime.strptime(task.get("Data").get("finishedon"), '%Y-%m-%d %H:%M:%S') - datetime.now()
            print(f"{date_obj.days * 24} ч.")
            tmp.append(f"{date_obj.days * 24} ч.")
        if task.get("Data").get("status") == 8:
            tmp.append("+")
        else:
            tmp.append("-")
        tmp.append( requests.get(f"http://test-ticket.gofromir.local/rest/profiles?filter[id]={task.get('createdby')}", headers=auth).json().get("results")[0].get("fullname"))
        tmp.append(requests.get(f"http://test-ticket.gofromir.local/rest/profiles?filter[id]={task.get('Data').get('it')}",headers=auth).json().get("results")[0].get("fullname"))
        tmp.append(task.get('Data').get("guid"))
        if task.get('Data').get("tags"):
            tmp.append(", ".join(task.get('Data').get("tags")))
        else:
            tmp.append("-")
        tmp.append(task.get('Data').get('type_cf'))
        tmp.append(task.get('content'))
        tasks.append(tmp)
    return tasks
