## 1. Find Optimal Medications

#This program iterates through the medications and perscriptions, 
#when it finds a non-generic medication, it searches through the medication 
#list to find a generic equavilent if possible. It then outputs all switches 
#necessary by perscription id and new medication id.



import requests
import json

scriptUpdates = [] #maintains a list of what perscription to update

mList = requests.get('http://api-sandbox.pillpack.com/medications')
if mList.status_code != 200: # Something went wrong, prints status
    raise Exception('GET /mList/ {}'.format(mList.status_code))
    
sList = requests.get('http://api-sandbox.pillpack.com/prescriptions')
if sList.status_code != 200: # Something went wrong, prints status
    raise Exception('GET /sList/ {}'.format(sList.status_code))
    
for script in sList.json(): #Go through all perscriptions pulling IDs and medication IDs
    scriptID = '{}'.format(script['id'])
    medID = '{}'.format(script['medication_id'])
    for meds in mList.json(): #Go through medications
        if medID == '{}'.format(meds['id']): #match ID to what is needed for prescription
            if '{}'.format(meds['generic']) != 'True': #if not GENERIC find a generic version if possible
                RX = '{}'.format(meds['rxcui']) #Gets RXCUI to match medications
                for meds2 in mList.json():
                    if RX == '{}'.format(meds2['rxcui']) and '{}'.format(meds2['generic']) == 'True': #Matches RXCUI and being GENERIC
                        scriptUpdates.append({"prescription_id": scriptID, "medication_id": '{}'.format(meds2['id']) }) #Adds perscription to the update list


with open("prescription_updates.json", "w") as file: #Makes the JSON file telling what scripts to update
    json.dump(scriptUpdates, file)







## 2. Find Optiamal Medications (with Pre-Processing)

#This program does the same as the previous, but process 
#the medication list first, building a list of only medications 
#that can be updated to a cheaper version

import requests
import json

scriptUpdates = [] #maintains a list of what perscription to update
quickScript = [] #maintains a list of what medication numbers have a generic equavilant  

mList = requests.get('http://api-sandbox.pillpack.com/medications')
if mList.status_code != 200: # Something went wrong, prints status
    raise Exception('GET /mList/ {}'.format(mList.status_code))

#Pre-Process Medications
for meds in mList.json(): #Go through medications
    if '{}'.format(meds['generic']) != 'True': #if not GENERIC find a generic version if possible
        RX = '{}'.format(meds['rxcui']) #RXCUI number
        oldID = '{}'.format(meds['id']) #Gets id for what medications can be switched
        for meds2 in mList.json(): #Finds medication to switch to
            if RX == '{}'.format(meds2['rxcui']) and '{}'.format(meds2['generic']) == 'True': #Matches RXCUI and being GENERIC
                quickScript.append({"old_med_id": oldID, "new_med_id": '{}'.format(meds2['id']) }) #Adds the med_id and the new one GENERIC one to a list  
 
sList = requests.get('http://api-sandbox.pillpack.com/prescriptions')
if sList.status_code != 200: # Something went wrong, prints status
    raise Exception('GET /sList/ {}'.format(sList.status_code))

for script in sList.json(): #Go through all perscriptions pulling IDs and medication IDs
    scriptID = '{}'.format(script['id'])
    medID = '{}'.format(script['medication_id'])
    for updates in quickScript: #iterate through all updatable medication IDs
        if medID == '{}'.format(updates['old_med_id']): #If match is found add the script and new med_id to the update list
            scriptUpdates.append({"prescription_id": scriptID, "medication_id": '{}'.format(updates['new_med_id']) })

    
with open("prescription_updates2.json", "w") as file: #Makes the JSON file telling what scripts to update
    json.dump(scriptUpdates, file)
    