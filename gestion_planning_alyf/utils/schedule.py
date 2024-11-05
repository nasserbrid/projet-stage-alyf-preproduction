import os
import django
import subprocess
import time
from apscheduler.schedulers.background import BackgroundScheduler
from requests import head
import requests
# import psutil
# from dotenv import load_dotenv, dotenv_values 

# load_dotenv() 
# # Initialiser Django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo_alyf.settings')
# django.setup()

def restart_django_app():
    manage_py_path = os.path.join("C:\\Users\\alyf\\projet-stage-Alyf-Django\\demo_alyf", "manage.py")
    while True:
        try:
            process = subprocess.Popen(['python', manage_py_path, 'runserver', '0.0.0.0:8000'], creationflags=subprocess.CREATE_NO_WINDOW)
            print("Django application started. PID:", process.pid)
            
            print(f"{os.getpid()} : pid2")
            
            process.wait()
            print(f"{process.wait()} : process wait")
            print("Django application crashed. Restarting in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            print(f"An error occurred: {e}")
            break

def relance_si_pas_de_reponse():
    url = "http://localhost:8000/calendar/"
    try:
        response = requests.head(url)
        print("Application en fonctionnement.")
        print(f"{os.getpid()} : pid3")
    except Exception as e:
        restart_django_app()
        print("Erreur détectée, redémarrage en cours.")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(relance_si_pas_de_reponse, 'interval', minutes=1)
    print(f"{os.getpid()} : pid4")
    scheduler.start()
