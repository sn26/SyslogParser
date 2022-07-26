import pandas as pd
import json

class ServiceSyslogParser:
    
    meses = {"1":"JAN", "2":"FEB", "3":"MAR", "4":"APR", "5":"MAY", "6":"JUN", "7":"JUL", "8":"AUG", "9":"SEP", "10":"OCT", "11":"NOV", "12":"DEC"}

    def __init__(self, csv_file ): 
        self.csv_file = csv_file
        return 

    def csv_to_json(self):
        h =  json.loads( pd.DataFrame( pd.read_csv(self.csv_file , sep = ",", header = 0, index_col = False )).to_json(orient = "records", date_format = "epoch", double_precision = 0, force_ascii = True, date_unit = "ms", default_handler = None) )
        return h

    def parse_time(self, date): 
        month =  ServiceSyslogParser.meses[date[0]]
        day = date[1]
        hr = int(date[-1].split(" ")[1].split(":")[0])
        mm = date[-1].split(" ")[1].split(":")[1] 
        ss = date[-1].split(" ")[1].split(":")[2]
       
        if date[-1].split(" ")[-1] == "PM": 
            hr  = int(date[-1].split(" ")[1].split(":")[0]) + 12 
        hrmmss = str(hr) + ":" + mm + ":" + ss
        return month + " " + day + " " +hrmmss 

    def parse_tag(self, src): 
        res = ""
        src = src.replace("-", "_")
        for i in range(0, len( src) ):
            if len(res) >= 32: 
                return res 
            if src[i].isalnum() == False: 
                return res
            res = res + src[i]
        return res 

    def parse_content(self, res ): 
        src = ""
        dst = ""
        if "(" in res["Traffic_Source"]: 
            src = res["Traffic_Source"].split("(")[1].split(")")[0]
        else: 
            src = res["Traffic_Source"]
        if "(" in res["Traffic_Destination"]: 
            dst = res["Traffic_Destination"].split("(")[1].split(")")[0]
        else: 
            dst = res["Traffic_Destination"]
        return "TYPE=" + str(res["Type"]) + " ACTION=" + str(res["Action"])  + " SRV_ID=" + str(res["Service ID"]) + " IP_SRC=" + str( src)  + " IP_DST=" + str(dst)  + " PORT_SRC=" + str(res["Source Port"]) + " PORT_DST=" + str(res["Destination Port" ]) + " SRC_ZONE=" + str( res["Source Zone"] )  + " DST_ZONE=" + str( res["Destination Zone"])  + " IFACE_NAME=" + str(res["Interface Name"]) + " USER="  + str(res["User"]) + " ID=" + str(res["Id"]) + " CON_DIR=" + str( res["Connection Direction"]) + "\n" 

    def parse_to_syslog(self):
        res = self.csv_to_json( )
        cad_final = ""
        for i in range( 0 , len(res )):
            cad_final = cad_final + "<158> " + self.parse_time( res[i]["Time"].split("/") ) + " " + self.parse_tag( res[i]["Device"]) + " " + res[i]["Traffic_Source"].split(" ")[0] + " " + self.parse_content(res[i])
        print(cad_final)
        return cad_final 

    def save_in_filepath(self, file_path):
        text_file = open(file_path, "w")
        text_file.write(self.parse_to_syslog())
        text_file.close()
        return

