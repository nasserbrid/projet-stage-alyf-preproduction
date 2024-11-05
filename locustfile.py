from locust import HttpUser, task, between
import logging 
import random

class DjangoUser(HttpUser):
    wait_time = between(2,5)

    test_users = [{"username":"OMARI", "password":"Youssef"}, {"username":"BENCHIKA", "password":"Soukeina"}, {"username":"MONJI", "password":"Ulrich"}, {"username":"LAMNAH", "password":"Abderraman"}]


    @task
    def on_start (self):
        self.user_credentials =random.choice(self.test_users)
        self.client.get("/login/")
        
    @task(1)
    def login(self):
        credentials = {
            "username":self.user_credentials['username'],
             "password":self.user_credentials['password'],
            
            "csrfmiddlewaretoken": self.client.cookies.get('csrftoken')
        }

        headers = {"X-CSRFToken": self.client.cookies.get('csrftoken')}
        with self.client.post("/login/", data=credentials, headers = headers, catch_response=True) as response:
            print(f"Status:{response.status_code}")
            print(f"Response:{response.text}")
            if response.status_code != 200:
                response.failure(f"Login failed with status {response.status_code}")
    

    @task()
    def getcalendar(self):
        credentials = { "csrfmiddlewaretoken": self.client.cookies.get('csrftoken')}
        headers = {"X-CSRFToken": self.client.cookies.get('csrftoken')}

        with self.client.post("/calendar/", data=credentials, headers = headers, catch_response=True) as response:
            print(f"Status:{response.status_code}")
            print(f"Response:{response.text}")
            if response.status_code != 200:
                response.failure(f"Login failed with status {response.status_code}")
