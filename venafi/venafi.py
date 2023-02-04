# Sample script to get certificate details and renew the appropriate one 
# This script is for demonstrating the API usage, not for deployment in a production environment

from datetime import datetime, timezone
import time
import requests
import json
import dateutil.parser

# Details related to venafi
venafi_api_url = "https://api.venafi.cloud/outagedetection/v1/"
api_key = "70402cab-746c-481d-980b-fe89bc67b4c8" 
content_type = 'application/json'
content_type_text = 'text/plain'
cert_download_type = '/contents?format=PEM&chainOrder=EE_ONLY'
template_name = "NTT Template"
#cert_id_download = 'fb5cab20-3d91-11ed-9ed4-7d61a4a777f8'

#Cert download location 
cert_download_location = "/usr/app/src/"

# CSR file location
cert_csr_file = "/usr/app/src/cert.csr"

# New validity 
new_validity = "P2D" # P2D, means extend by two Days

# Global variables
global app_id 
global template_id 
global certificate_id
global cert_csr 
global json_data
global validity_end_date 
#global certificate_name


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
                            "value": "2023-02-03T11:17:10.720+00:00" #datetime.now((timezone.utc)).isoformat()
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
            "pageSize": 20
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
        print("-----------------------------------------------------------------------------")
        print("Certificate ID " + get_json_entity(cert_json,"id"))
        print("Certificate Status " + get_json_entity(cert_json,"certificateStatus"))
        print("Certificate Name " + get_json_entity(cert_json,"certificateName"))
        print("Certificate versionType " + get_json_entity(cert_json,"versionType"))

        # For Demo purpose, selecting only the localhost cert 
        if get_json_entity(cert_json,"certificateName") == "localhost":
            if (get_json_entity(cert_json,"certificateStatus") != "RETIRED"):
                cert_id=get_json_entity(cert_json,"id")
                #print("Certificate endValidity " + get_json_entity(cert_json,"validityEnd"))
                validity_end_date = dateutil.parser.parse(get_json_entity(cert_json,"validityEnd"))
                diffretiation = validity_end_date - now
                if diffretiation.days < 2:
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
                        print("template id ->",app[template_name])
                        template_id=list(app.values())[0]
                
                # To get specific template
                try:
                    if template_id is not None:
                        pass
                except:
                    template_id = app[template_name]


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
                json_object = response.json()
                #cert_details=get_json_entity(json_object,"certificateIds")
                #new_cert_id=json_object['certificateRequests'][0]['certificateIds'][0]

                if response.status_code == 201 or response.status_code == 200:
                    print ("SUCCESS: Certificate with ID: "+ certificate_id + " renewed.")
                    time.sleep(10)
                    # To get all the certs including new 
                    new_response = send_request("certificatesearch", "post", data_certificatesearch, api_key, content_type)
                    if new_response.status_code == 201 or new_response.status_code == 200:
                        new_json_object = new_response.json()
                    else:
                        print("Failed to get proper response for new certificate search")
                    new_cert_details=get_json_entity(new_json_object,"certificates")
                    for i in range(len(new_cert_details)):
                        cert_json=new_cert_details[i]
                        if (get_json_entity(cert_json,"certificateStatus") != "RETIRED"):
                            if (get_json_entity(cert_json,"versionType") != "OLD"):
                                new_cert_id=get_json_entity(cert_json,"id")
                                print("Got new Certificate with ID: "+ new_cert_id )

                            #certificate_id = cert_id
                    # new - for download
                    try:
                        response = send_request("certificates/"+ new_cert_id + cert_download_type, "get", data_app, api_key, content_type_text)    
                        with open(cert_download_location +"new_cert.pem", "wb") as file: 
                            file.write(response.content)
                        print("SUCCESS: Downloaded renewed certificate from Venafi with ID: "+ new_cert_id)
                    except:
                        print("FAILED: To download the certificate from Venafi")
                else:
                    print("FAILED: To renew Certificate with ID: "+ certificate_id )
                print("**********************************************************************")

    print ("SLEEPING NOW...")
    time.sleep((60.0 - ((time.time() - starttime) % 60.0))*1380) # 60(sec) i.e. 1 min x (24*60=1440 (removing 60 min as grace time))
    #time.sleep(sleep_timer)




print("Script execution done.")


 

 
