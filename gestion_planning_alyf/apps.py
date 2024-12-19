from django.apps import AppConfig
#from .utils.schedule import check_server_status
from .utils.schedule import start_scheduler
import os

class GestionPlanningAlyfConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestion_planning_alyf'
    # scheduler_started = False 
    

   # def ready(self):
    #   start_scheduler()
         
       
        # if not GestionPlanningAlyfConfig.scheduler_started:
        #     if os.environ.get('RUN_MAIN', None) != 'true':
        #         GestionPlanningAlyfConfig.scheduler_started = True
                # from .tasks import start_scheduler
                # start_scheduler()
        
        
       
            
            
        

