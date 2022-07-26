import argparse
from library_syslog.service import ServiceSyslogParser

def main():  
    script_main_function( parse_args() )
    return
  

def script_main_function(args): 
    ssparser = ServiceSyslogParser( args.file_csv_path )
    ssparser.save_in_filepath( args.file_output_path )
    return
    

#Function to get the entrance arguments from the client
def parse_args(): 
    parser = argparse.ArgumentParser()
    parser.add_argument("-fcp", "--file-csv-path", action='store', required=True,
                        help="Path where the original csv is stored. Required")
    parser.add_argument("-fop", "--file-output-path", action='store', required=True,
                        help="Path in which the result syslog parsed will be stored. Required")
    return parser.parse_args()

if __name__ == "__main__":
    main()
