def get_BW_qos_profile(string):

    i = string.find(" ")
    j = string.find("M")

    aux_str = string[i:j]
    
    try:
        aux_int = int(aux_str)
    except ValueError:
        aux_int = -1
    
    return aux_int
    
def get_BW_traffic_policy(string):

    i = string.find("-I")
    j = string.find("M")
    
    aux_str = string[i+2:j]
    aux_num_1 = int(aux_str)
    
    i = string.find("-C")
    j = string.find("M", i)
    
    aux_str = string[i+2:j]
    aux_num_2 = int(aux_str)
    
    return aux_num_1 + aux_num_2

def analyzer(router):

	with open(router + ".log","r") as file_config:
    
            config_of_interface = []
            list_of_interfaces = []
            errors = []
        
            INTERNET = []
            PW = []
            Multicast = []
            Trebol = []
            return_value = []
        
            is_internet = False
            is_internet_or_trebol = False
            is_pw = False
            is_multicast = False
            is_trebol = False
            qos_profile_present = False
            traffic_policy_present = False
            interface_configured = False
            
            string_errors = ""
            
            BW = 0
            INTERNET_configured = 0
            PW_configured = 0
            Multicast_configured = 0
            Trebol_configured = 0
            BW_total_configured = 0
            
            for line in file_config:
                
                if(line.find("GigabitEthernet")>0   or   line.find("Eth-Trunk")>0):

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
                        interface_configured = True
                        
                    elif(parameter.find("mpls l2vc")==0):
                    
                        is_pw = True;
                        interface_configured = True
                        
                    elif(parameter.find("l2-multicast static-group")==0):
                    
                        is_multicast = True;
                        interface_configured = True
                        
                    elif(parameter.find("igmp static-group")==0):
                    
                        is_multicast = True;
                        interface_configured = True
                    
                    elif(parameter.find("qos-profile")==0):
                    
                        BW = get_BW_qos_profile(parameter)
                        
                        if(BW > 0):
                            qos_profile_present = True
                        break
                            
                    elif(parameter.find("traffic-policy TSERV")==0):
                    
                        is_trebol = True
                        is_internet = False
                        traffic_policy_present = True
                        BW = get_BW_traffic_policy(parameter)
                        break
                        
                if(interface_configured and not (qos_profile_present or traffic_policy_present)):
                        
                    if(len(errors) == 0):
                        
                        string_errors = str(router + "," + interface[0])
                        
                    else:
                        
                        string_errors += "\n" + str(router + "," + interface[0])
                        
                    #print("UTCKAG11: sin BW configurado en interface ",interface[0])
                    
                if(is_internet and qos_profile_present):
                    INTERNET.append(BW)
                    #is_internet = False
                    #is_internet_or_trebol = False
                elif(is_pw and qos_profile_present):
                    PW.append(BW)
                    #is_pw = False
                elif(is_multicast and qos_profile_present):
                    Multicast.append(BW)
                    #is_multicast = False
                elif(is_trebol and traffic_policy_present):
                    Trebol.append(BW)
                    #is_trebol = False
                    #is_internet_or_trebol = False
                
                BW = 0
                is_internet = False
                is_pw = False
                is_multicast = False
                is_trebol = False
                is_internet_or_trebol = False
                qos_profile_present = False
                traffic_policy_present = False
                interface_configured = False
                
            INTERNET_configured = sum(INTERNET)
            BW_total_configured += INTERNET_configured
            PW_configured = sum(PW)
            BW_total_configured += PW_configured
            Multicast_configured = sum(Multicast)
            BW_total_configured += Multicast_configured
            Trebol_configured = sum(Trebol)
            BW_total_configured += Trebol_configured
            
            services = str(router + "," + str(INTERNET_configured) + "," + str(PW_configured) + "," + str(Multicast_configured) + "," +
                                            str(Trebol_configured) + "," + str(BW_total_configured))
            
            return_value.append(services)
            
            if(len(string_errors) > 0):
                return_value.append(string_errors)
            
            return(return_value) 