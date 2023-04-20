import json
import analyzer
from os.path import exists
import time

with open("Network elements.json", "r") as network_elements:

    aux_str = network_elements.read()
    global ne
    ne = json.loads(aux_str)
  
with open("report.csv","w") as file:
    
    file.write("\"" + "Reporte de configuracion en interfaces - Ingenieria IP\"\n")
    file.write("\"" + time.strftime("%c") + "\"\n")
    file.write("\n")
    file.write("\"Acronimo\",\"Internet\",\"Lan2Lan\",\"Multicast\",\"Trebol\",\"Total BW\"\n")
    
with open("errors.csv","w") as file:
    
    file.write("\"" + "Reporte de configuracion en interfaces - Ingenieria IP\"\n")
    file.write("\"" + time.strftime("%c") + "\"\n")
    file.write("\n")
    file.write("\"Acronimo\",\"Interface sin config de BW\"\n")
  
for router in ne:
    
    #file_exists = exists("report.csv")
    
    #if not(file_exists):
    router_list = analyzer.analyzer(ne[router]) 
    
    with open("report.csv","a") as f1:
        f1.write(router_list[0] + "\n")
        
    if(len(router_list) > 1):
        with open("errors.csv","a") as f2:
            f2.write(analyzer.analyzer(ne[router])[1] + "\n")
    #print(analyzer.analyzer(ne[router]))

     

