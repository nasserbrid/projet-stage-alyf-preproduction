import json
import win32com.client
import time

import os
from . import Module
import pandas as pd
from datetime import date
from datetime import datetime
from django.core.cache import cache
import pathlib as pl

import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo_alyf.settings')
django.setup()

# Ces lignes définissent d'abord la variable d'environnement pour spécifier le fichier de configuration Django à utiliser (settings.py). Ensuite, elles initialisent Django pour rendre ses #  #fonctionnalités disponibles dans le script.
#permet d'initialiser l'environnement django, 


from dotenv import load_dotenv, dotenv_values 
# loading variables from .env file
load_dotenv() 



class ExcelFile:

    def __init__(self, workbook= None , worksheet= None):
        self.excel = win32com.client.Dispatch("Excel.Application")
        self.workbook = workbook
        self.worksheet = worksheet
      #   self.excel.Visible = False
      #   self.excel.DisplayAlerts = False
          

    def open_worksheet(self, sheetName, path = os.getenv("ALYFMASTERPATH")):
           
        
            self.excel.Visible = True
            self.excel.DisplayAlerts = True
        
       
            if self.excel.Visible == True:
                  # print(f"excel is {self.excel.Visible}")
                  
                                
                   try:
                                          
                       # self.workbook = self.EXCEL.Workbooks.Open("C:\\Users\\nasse\\projet-stage-Alyf\\Test-fichier-excel\\alyfData.xlsm")
                       
                        self.workbook = self.excel.Workbooks.Open(path)
                       
                        # print(self.workbook.Sheets)
                
                        self.worksheet = self.workbook.Sheets(sheetName)
                        

                        # print(self.workbook)
                      
                   except FileNotFoundError:
                         print("Le fichier Excel est introuvable.")
                         
                        
                         self.excel.Quit()

                         exit(1)
                   except Exception as e:
                        print('La feuille "DEV WEB" est introuvable:', e)
                        self.workbook.Close(SaveChanges=False)
                        #self.EXCEL.Quit()
                        self.excel.Quit()
                        exit(1)
                             

    def save_formateur_worksheet(self, formateur_name):
         
          
          self.worksheet.Cells(1, 8).Value = formateur_name
       
          self.workbook.SaveAs(os.getenv("ALYFDEVPATH"))
          #removed ConflictResolution=2
          
          self.workbook.Close(SaveChanges=True)
        
          self.excel.Quit()
    

    def save_instructor_sheet_separately(self, formateur_name, target_path):
            
            self.excel.Visible = True
            print(f"{self.excel.Visible}: excel visible?")
            self.excel.DisplayAlerts = True
            try:   
                print(f"{self.excel.Visible}: excel visible?")
                print("echo alpha bravo")
            # Set the formateur name in the worksheet
                self.worksheet.Cells(1, 8).Value = formateur_name

            # Copy the worksheet to a new workbook
                new_workbook = self.excel.Workbooks.Add()
                self.worksheet.Copy(Before=new_workbook.Sheets(1))
                # A FAIRE enlever le sheet1 des fichiers de planning individuels
            
           
                new_workbook.SaveAs(target_path, FileFormat=52)
                #removed conflict res  ConflictResolution=2
                new_workbook.Close(SaveChanges=True)
                print(f"Saved worksheet as new file: {target_path}")

            except Exception as e:
                 print(f"Error during operation: {e}")
            finally:
                 self.workbook.Close(SaveChanges=False)
                 self.excel.Quit()

          
          
    #Définir une méthode qui permet d'utiliser le dataframe et qui va récupérer des sessions dans "DEV WEB"
    def create_fullYearTeachingDataFrame_from_instructorSheet(self, path = os.getenv("ALYFDEVPATH") ):
           
           excel_path = path
           #print(path)
           
           #output_path = os.getenv("ALYFJSONPATH")
               
          # print("in create full year Teaching")
           try:
                  i=0 
                  df_fullYearTeachingData = pd.read_excel(excel_path, sheet_name="DEV WEB", header=None,  usecols=[i,i+1,i+2], skiprows=3, index_col=None)
                  df_fullYearTeachingData = df_fullYearTeachingData.fillna('')
               
                              
           except FileNotFoundError:
                   print("Le fichier Excel est introuvable.")
                   exit(1)
           except ValueError:
              print('La feuille "DEV WEB" est introuvable.')
              exit(1)
                  
           for month in range(2,13):
                   i +=3
                   df = pd.read_excel(excel_path, sheet_name="DEV WEB", header=None, usecols=[i, i+1, i+2], skiprows=3, index_col=None)
                   df = df.fillna('')
                                           

           
           # Renommer les colonnes de df2 pour qu'elles correspondent à celles de df1
                   df.columns = df_fullYearTeachingData.columns
                   #print(f"{df_fullYearTeachingData.columns} df1 colums")

           
           # Concaténation des deux DataFrames verticalement
                   df_fullYearTeachingData = pd.concat([df_fullYearTeachingData, df])
         

          # Réinitialisation de l'index si nécessaire
                   df_fullYearTeachingData.reset_index(drop=True, inplace=True)
       


      # Affichage du résultat
                   pd.set_option('display.max_rows', None)
         
                   df_fullYearTeachingData.dropna(subset=[0],  inplace= True)
                   #df_fullYearTeachingData = df_fullYearTeachingData.map(convert_dates)
       
           print(df_fullYearTeachingData)
           return df_fullYearTeachingData
           
       # Récupération des modules
                   #print(f"les valeurs unique sont :{df_fullYearTeachingData[1].unique()}")
        
 
    
    def create_modules(self, path = os.getenv("ALYFDEVPATH")):
            #cette methode permettra de recuperer toutes les infos du module
            # print("in create module")

           df  = self.create_fullYearTeachingDataFrame_from_instructorSheet(path)
           liste_de_cours = df[1].unique()
           liste_de_cours= list(filter(len, liste_de_cours))
           print(liste_de_cours)

           # A FAIRE need to have a method specifically designed to get all Indisponibilités for an instructor
           if "Indisponible" in liste_de_cours :
                 liste_de_cours.remove("Indisponible")
           print(f"{liste_de_cours} liste de cours")
           dico_module = {}
           
           for cours in liste_de_cours:
                  dico_module[cours] = {}
                  
                  #print(cours)
                  dates = df.index[df[1]==cours]
                  #print(f"datesindex: {dates}")
                  dates_vals = []
                  for date in dates:
                        # print(type(date))
                         dates_vals.append(date)
                 # print(f" dates_vals: {dates_vals} ")
                 # print(f"vérification de dates_vals : {dates_vals}")

                  blocks = [[dates_vals[0]]]

                  for i in range(1,len(dates_vals)):
                           if dates_vals[i] - dates_vals[i-1] == 1:
                                          blocks[-1].append(dates_vals[i])
                           else:
                                   blocks.append([])
                                   blocks[-1].append(dates_vals[i])
                          # print(f" blocks: {blocks}")
                  
                 # print(f"blocks:{blocks}")

                #   for date in blocks:
                #            print(df[0].iloc[date])
                     

                
                  for j in range(0, len(blocks)):
                            # print(j)
                             #modkey = j
                             dico_module[cours][j] = Module.Module(df[1].iloc[blocks[0][0]], df[0].iloc[blocks[j][0]], 
                                                  df[0].iloc[blocks[j][-1]],df[2].iloc[blocks[0][0]],[],[])
                             

                             listecoursterminesetfuturs = self.create_list_cours_termines_et_futur( dico_module[cours][j].get_nom_module(),
                                                                                                   self.find_session_type(dico_module[cours][j].get_session()), dico_module[cours][j].get_session())

                             dico_module[cours][j].set_modules_termines(listecoursterminesetfuturs[0])
                             dico_module[cours][j].set_modules_a_venir(listecoursterminesetfuturs[1])
                            #  dico_module[cours][j] = dico_module[cours][j].to_dict()
                             dico_module[cours][j] = dico_module[cours][j]
                  
                            #  dico_module[cours][j] = json.dumps(dico_module[cours][j])

                        #      print(f"modules terminés : {dico_module[cours][j].get_modules_termines()}")
                 
                        #      print(f"modules à venir : {dico_module[cours][j].get_modules_a_venir()}")
          #  test_a = json.dumps(dico_module)
          #  print(f"le type de test_a : type({test_a})")
        
          #  return json.dumps(dico_module)
           return dico_module
          # print(self.find_session_type(dico_module["Ecoute & Relation Clients"][0].get_session()))
                  
           #list_session = []
          # print(dico_module)

          # testmod = dico_module["Ecoute & Relation Clients"][0]

        #    listecoursterminesetfuturs = self.create_list_cours_termines_et_futur(testmod.get_nom_module(),self.find_session_type(testmod.get_session()), testmod.get_session())
        #   # print(listecoursterminesetfuturs)

        #    #print(f" liste cours termines et futur{listecoursterminesetfuturs}")

        #    c = self.create_list_cours_termines_et_futur(testmod.get_nom_module(),self.find_session_type(testmod.get_session()), testmod.get_session())

          # print(c[0])



        #    testmod.set_modules_termines(c[0])
        #    testmod.set_modules_a_venir(c[1])

        #    print(testmod.get_modules_termines())
        #    print(testmod.get_modules_a_venir())
                #       module_test.set_modules_a_venir = liste_cours_termines_et_futurs[1]
        #    for key in dico_module:
        #               for internal_key in dico_module[key]:
        #                              liste_cours_termines_et_futurs =  self.create_list_cours_termines_et_futur(dico_module[key][internal_key].get_nom_module ,self.find_session_type(dico_module[key][internal_key].get_session()),dico_module[key][internal_key].get_session())
        #                      # list_session.append(self.find_session_type(dico_module[key][internal_key].get_session()))
        #               print(liste_cours_termines_et_futurs)                 
                              
                  
                   
              
                 
            

        #    for k in range(0, len(dico_module)):
        #           print(dico_module[k].get_nom_module())
        #           print(dico_module[k].get_date_debut())
        #           print(dico_module[k].get_date_fin())
        #           print(dico_module[k].get_session())
                         
                 
                 
                               
                       
                               
                        
                              
                                
           #print(f"vérification de blocks : {blocks}")

           

           
            
                 

        #    module_test2 = Module.Module(df[1].iloc[blocks[0][0]], df[0].iloc[blocks[0][0]],df[0].iloc[blocks[0][-1]],df[2].iloc[blocks[0][0]],[],[] )
        #    print(f":nom de module:{module_test2.get_nom_module()}\n date de debut: {module_test2.get_date_debut()}\n date de fin: {module_test2.get_date_fin()}")

           
               
        #    for j in range(0, len(blocks)):
        #                       f"" = Module.Module(df[1].iloc[blocks[0][0]], df[0].iloc[blocks[j][0]], 
        #                                           df[0].iloc[blocks[j][-1]],df[2].iloc[blocks[0][0]],[], [])
                     
                     
          
                    
                #   print(module_test.get_nom_module())
                #       liste_cours_termines_et_futurs =  self.create_list_cours_termines_et_futur(module_test.get_nom_module ,self.find_session_type(module_test.get_session()))

                #       module_test.set_modules_termines = liste_cours_termines_et_futurs[0]
                #       module_test.set_modules_a_venir = liste_cours_termines_et_futurs[1]


                
                      
                #       print(module_test.get_nom_module())
                #       print(module_test.get_date_debut())
                #       print(module_test.get_date_fin())
                  
                #   for index_value in blocks[0]:
                #       print(df[0].iloc[index_value])
                    
     
    def find_session_type(self, session_name):
            
    
      keywords = {
        "Isitech - XEFI": ["isi", "ISI", "isitech", "xefi", "XEFI", "ISITECH", "XEFI"],
        "Sessions Alternantes": ["ALT", "alt", "Alt"],
        "Hors Cursus - Atos Générique": ["HC", "HORS CURSUS", "hors cursus", "horscursus", "ATOS", "atos", "ATOS GENERIQUE"]
     }
 
    # Check if any keyword from the lists is in the input string
      for key, values in keywords.items():
           if any(value in session_name for value in values):
             return key
 
    # Default return value if no match is found
      return "Sessions Continues"
 
        
     
    def get_session_dataframe(self, sheetName, sessionName): 
        # feuille = self.open_worksheet(self.find_session_type(sheetName))
         
         if cache.get("master_excel_file") != None:
               excel_path = cache.get("master_excel_file")
         else:
               excel_path = os.getenv("ALYFDEVPATH")
         #Faire 2 dataframes un avec seulement dates et l'autre présentera les sessions et les combiner par la suite
         df_session_name_and_dates = pd.read_excel(excel_path, sheet_name=sheetName, skiprows=1, nrows=3,  header=None ,index_col=None)
         df_session_name_and_dates = df_session_name_and_dates.fillna('')
        
         
         
       #   #print(df.head(1))
       #   df_test = df_session_name_and_dates.head(3)
       #   nom_session = "2iTECH-TSSR-2022 - ALT"
       #   print(df_test)
         
       
       #   print(ind)

         value =  sessionName
         print(f" value: {value}")
         #print(df_session_name_and_dates)

# Extract Column Names
         column_index = df_session_name_and_dates.columns[df_session_name_and_dates.eq(value).any()].tolist()[0]
         print(column_index+1)
         date_debut =df_session_name_and_dates[column_index+1][1]
         date_fin = df_session_name_and_dates[column_index+1][2]
        
         number_of_rows_delta = date_fin - date_debut
         number_of_rows = number_of_rows_delta.days
         
        

         date_debut_str =str(date_debut)
         #date de fin inutile pour l'instant 
         #date_fin_str = str(date_fin)

         df_index_calendrier_sessions = pd.read_excel(excel_path, sheet_name=sheetName, usecols=[0],skiprows=1, header=None)

         index_date_debut_session = list(df_index_calendrier_sessions.index[df_index_calendrier_sessions[0] == datetime.fromisoformat(date_debut_str)])[0]

         df_modules_session = pd.read_excel(excel_path, sheet_name=sheetName, skiprows=index_date_debut_session, nrows=number_of_rows,usecols=[column_index, column_index+1],  header=None, index_col=None)

         return df_modules_session
    
    def create_list_cours_termines_et_futur(self, module_name, sheet_name, session_name):
          df = self.get_session_dataframe(sheet_name,session_name)
          df = df.fillna("")
          #print(df)
          df.columns = [0,1]
  
        #   print(df.columns)
          unique_units = df[0].unique()
          print(f"unique_units : {unique_units}")
          
         
          unique_units = list(filter(len, unique_units))
          print(unique_units)
        #   print(type(unique_units))
       
          #unique_units.remove("FERIE")
          #print("FERIE" in unique_units)
          

          #print(unique_units)

          #il faut filtrer certains termes dont férié

       
          if module_name not in unique_units:
             print(f"Erreur: {module_name} n'est pas dans unique_units.")
             return [], []
          
          #A VERIFIER, le code sur la ligne 430 et dessous permettent de gerer les valeurs comme jours fériés, etc qu'on trouve qu'on trouve dans les cellules du fichier excel
          
                
          index_current_module  = unique_units.index(module_name)
        #   print(index_current_module)
          cours_termines = []
          cours_futurs = []

          for i in range(0,index_current_module):
                cours_termines.append(unique_units[i])
          for j in range(index_current_module,len(unique_units)):
                cours_futurs.append(unique_units[j])
         # print(f"cours termines: {cours_termines}, cours_futurs:{cours_futurs}" )

          return cours_termines, cours_futurs


    def retrieve_instructor_list(self, sheetName):
          
          print("je suios ds retrieve instructor list")
          
          self.excel.Visible = True
          self.excel.DisplayAlerts = True
         

          if cache.get("master_excel_file") != None:
               excel_path = cache.get("master_excel_file")
               self.open_worksheet(sheetName, excel_path)
          else:
               print
               print("right before  excel_path = os.getenv('ALYFDEVPATH') ")
               path = pl.Path("C:\\Users\\alyf\\projet-stage-Alyf-Django\\demo_alyf\\data\\alyf_master_data.xlsm")
               print(path.is_file())
               
               excel_path = os.getenv("ALYFDEVPATH")
               self.open_worksheet(sheetName)
          

          
          dico_formateur_module = {}
          df =  pd.read_excel(excel_path, sheet_name=sheetName, skiprows=1, nrows=150,usecols=[0, 1],  header=None ,index_col=None)
          df[[2, 3]] = df[0].apply(self.split_name).apply(pd.Series)
          df = df.drop(0, axis="columns")
          dico_formateur_module = df.to_dict("split")

          return dico_formateur_module["data"]
          
         
    def split_name(self,full_name):
        parts = full_name.split()
        split_point = next((i for i, part in enumerate(parts) if part.isupper()), len(parts))
        return ' '.join(parts[:split_point]), ' '.join(parts[split_point:])
    

   
# Assuming you have a DataFrame named 'df' with a column 'full_name'


# Apply the function to the column




          # df[['First Name', 'Last Name']] = df[0].str.split(' ', expand=True)
          
         
          
         
      
         
          

        
       

             
       

         
         

   
         


         
         
         
         
         
         
         
         
         
         
         
        
        
            
        
                    
               
                
                 
 

   
   
    
    