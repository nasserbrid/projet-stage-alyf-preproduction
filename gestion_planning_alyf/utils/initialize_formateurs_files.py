import hashlib
from django.core.cache import cache 


import tempfile

import os
import django
from dotenv import load_dotenv, dotenv_values

load_dotenv()


# Définir la variable d'environnement DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo_alyf.settings')

# Initialiser Django
django.setup()

from ..services import ExcelFile,Formateur
#from .getinstructorlist import getinstructorlist




def build_schedule_files_for_formateurs():

    x = cache.get("master_excel_file")
    print(f"{x} cache" )

    excel = ExcelFile()
    excel.open_worksheet("DEV WEB")
    print(excel)
    instructors = excel.retrieve_instructor_list("FORMATEURS - MODULES")
    print(instructors)

    formateurs = []

    # excelfile = ExcelFile()
    # excelfile.open_worksheet("DEV WEB")
    print("past open worksheet")

    for instructor in instructors:
        formateurs.append(Formateur(instructor[1], instructor[2],instructor[0]))


   

# Suppose you have a list of instructors


# Create a dictionary to store the temporary file paths
    directory_of_individual_instructor_sheet_in_temp_storage = {}
    alyfmasterfile = cache.get("master_excel_file")
    print(f"{alyfmasterfile}: alyfmasterfile")
    print(f"{directory_of_individual_instructor_sheet_in_temp_storage}: directory")

# Create a unique temporary file for each instructor
    for formateur in formateurs:
         excelfile = ExcelFile()
         
         excelfile.open_worksheet("DEV WEB", alyfmasterfile)
         print("past open_worksheet with alyfmasterfile in param ")
   
         temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsm').name
         print(f"{temp_file}:temp_file")
         directory_of_individual_instructor_sheet_in_temp_storage[formateur] = temp_file
         print(formateur.get_last_name())
         excelfile.save_instructor_sheet_separately(formateur.get_last_name(), temp_file)
    # cache.set("dict_sheets_temp_storage", directory_of_individual_instructor_sheet_in_temp_storage)
    print(directory_of_individual_instructor_sheet_in_temp_storage)
    cache.set("dict_sheets_temp_storage", directory_of_individual_instructor_sheet_in_temp_storage)


# Now you can refer to each instructor's temp file through the dictionary
# for instructor, file_path in temp_files.items():
#     print(f"The temporary file for {instructor} is located at: {file_path}")

    
   
#build_schedule_files_for_formateurs()