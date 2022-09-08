# Script to get certificate details and renew the appropriate one 

from datetime import datetime, timezone
import time
import requests
import json
import dateutil.parser

# Details related to venafi
venafi_api_url = "https://api.venafi.cloud/outagedetection/v1/"
api_key = "8f67c5e6-04d3-4e2b-8575-1034632b891f" 
content_type = 'application/json'

# CSR file location
cert_csr_file = "/usr/app/src/domain.csr"

# New validity 
new_validity = "P1D" # P1D, means extend by one Day

# Global variables
global app_id 
global template_id 
global certificate_id
global cert_csr 
global json_data
global validity_end_date 


while True:
    # get current time object
    now = dateutil.parser.parse(datetime.now((timezone.utc)).isoformat())
    #print(datetime.now((timezone.utc)).isoformat())
    #print(now)
    
    data_certificatesearch =  {
        "expression": {
            "operands": [
                {
                    "operands": [
                        {
                            "field": "validityEnd",
                            "operator": "GT",
                            "value": "2022-09-03T11:17:10.720+00:00" #datetime.now((timezone.utc)).isoformat()
                        }
                    ]
                }
            ]
        },
        "ordering": {
            "orders": [
                {
                    "direction": "DESC",
                    "field": "certificatInstanceModificationDate"
                }
            ]
        },
        "paging": {
            "pageNumber": 0,
            "pageSize": 10
        }
    }

    data_app=""
    
    starttime = time.time()
    # Function to format string to JSON type
    def data_in_json(value):
        try:
            json_data=json.dumps(value)
            return json_data
        except: 
            print("Function data_in_json failed, check the parameters provided.")

    # Function to dispatch the request
    def send_request(api, type, data_to_send, key, content_type):
        try:
            if type == "post":
                return requests.post(venafi_api_url+api, data=data_in_json(data_to_send), headers={ 'tppl-api-key': key, 'Content-Type': content_type})
            if type == "get":
                return requests.get(venafi_api_url+api, data=data_in_json(data_to_send), headers={ 'tppl-api-key': key, 'Content-Type': content_type})
        except:
            print("Function send_request failed, check the parameters provided.")

    # Function to traverse json object for specific value
    def get_json_entity(json_object, value_to_check):
        for key in json_object:
            value = json_object[key]
            if (key == value_to_check):
                global details
                details=value  
        return details  

    # Function to get entity via for loop
    def get_entity_via_for_loop(object_to_loop, entity_to_find):
        global entity_found
        my_entity=entity_to_find
        for count in range(len(object_to_loop)):
            object_to_loops=object_to_loop[count]
            #print(get_json_entity(object_to_loops,"name"))
            entity_found=get_json_entity(object_to_loops,my_entity)
        return entity_found
    # Request to search certificates
    response = send_request("certificatesearch", "post", data_certificatesearch, api_key, content_type)
    
    json_object = response.json()

    cert_csr=""
    # Block to read the csr file
    try:
        f = open(cert_csr_file, "r")
        for x in f:
            #print(x)
            cert_csr+= x 
        f.close()
    except:
        print("Not able to read CSR file: " + cert_csr_file)
    else:
        print("Succesfully read CSR file.")

    #print(json_object)
    cert_details=get_json_entity(json_object,"certificates")

    for i in range(len(cert_details)):
        cert_json=cert_details[i]
        #print(cert_json)
        print("Found Certificate with Name: " + get_json_entity(cert_json,"certificateName")+ " and ID: " + get_json_entity(cert_json,"id") )
        #print("Certificate versionType " + get_json_entity(cert_json,"versionType"))
        #print("Certificate endValidity " + get_json_entity(cert_json,"validityEnd"))
        if (get_json_entity(cert_json,"versionType") != "OLD"):
            cert_id=get_json_entity(cert_json,"id")
            #print("Certificate endValidity " + get_json_entity(cert_json,"validityEnd"))
            validity_end_date = dateutil.parser.parse(get_json_entity(cert_json,"validityEnd"))
            diffretiation = validity_end_date - now
            if diffretiation.days < 1:
                print("WARNING: Certificate with Name: " + get_json_entity(cert_json,"certificateName")+ ", with ID, " + cert_id + ", about to expire." )
                certificate_id=cert_id 
            app_instances=get_json_entity(cert_json,"instances")

            # Loop to get Application ID
            for j in range(len(app_instances)):
                app_details=app_instances[j]
                application_Ids=get_json_entity(app_details,"applicationIds")
                # Only a single App ID required for renew https://docs.venafi.cloud/api/renewing-a-certificate-api/
                app_id = application_Ids[0]
            # Request to search applications
            response = send_request("applications", "get", data_app, api_key, content_type)
            json_object = response.json()
            all_app_details=get_json_entity(json_object,"applications")

            # Loop to get template ID
            for k in range(len(all_app_details)):
                all_app_detail=all_app_details[k]
                app=all_app_detail['certificateIssuingTemplateAliasIdMap']
                if get_json_entity(all_app_detail,"id") == app_id:
                    # Only a single template ID required for renew https://docs.venafi.cloud/api/renewing-a-certificate-api/
                    template_id=list(app.values())[0]
            
            data_certificate_renew = {
                #"certificateOwnerUserId": "54f59c20-2ad0-11ed-90f1-4792aa1219bb",
                "certificateSigningRequest": cert_csr,
                "applicationId": app_id,
                "certificateIssuingTemplateId": template_id,
                "validityPeriod": new_validity,
                "existingCertificateId": certificate_id
            }
            
            # Request to renew certificates
            response = send_request("certificaterequests", "post", data_certificate_renew, api_key, content_type)
            
            if response.status_code == 201 or response.status_code == 200:
                print ("SUCCESS: Certificate with ID: "+ certificate_id + " renewed.")
            else:
                print("FAILED: To renew Certificate with ID: "+ certificate_id )
            print("---------------------------------------------------------")

    print ("SLEEPING NOW...")
    time.sleep((60.0 - ((time.time() - starttime) % 60.0))*1380) # 60(sec) i.e. 1 min x (24*60=1440 (removing 60 min as grace time))
    #time.sleep(sleep_timer)

print("Script execution done.")


 