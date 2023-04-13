def grab_interfaces(file):
    pass
    
def get_BW(string):

    i = string.find(" ")
    j = string.find("M")

    aux_str = string[i:j]
    
    return aux_str

with open("C:\\Users\\fbova\\Desktop\\Tacanitas.log","r") as file_config:

    config_of_interface = []
    list_of_interfaces = []
    
    INTERNET = []
    PW = []
    Multicast = []
    
    is_internet = False;
    is_pw = False;
    is_multicast = False;
    
    BW = 0
        
    for line in file_config:
        
        if(line.find("GigabitEthernet")>0):

            aux_str = str(line).strip()
            config_of_interface.append(aux_str)
            while(aux_str != '#'):
                
               #print(aux_str)
               aux_str = file_config.readline().strip()
               config_of_interface.append(aux_str)
               
            aux_list = list(config_of_interface)
            list_of_interfaces.append(aux_list)
            config_of_interface.clear()
    
    for interface in list_of_interfaces:
    
        for parameter in interface:
        
            if(parameter.find("INTERNET")>0):
            
                is_internet = True;
                
            if(parameter.find("mpls l2vc")==0):
            
                is_pw = True;
            
            elif(parameter.find("qos-profile")==0):
            
                    BW = int(get_BW(parameter))
                    break
            
        if(is_internet):
            INTERNET.append(BW)
            is_internet = False
        elif(is_pw):
            PW.append(BW)
            is_pw = False
            
    print("Internet configurado")
    print(sum(INTERNET))
    print("Pseudowires confugurados")
    print(sum(PW))

         

