#######Intro to Gale Shapely Algo
## PatientPreference is a dictionary, and so is hospital preference.
# The flow of the program is, it starts with the patients that are present in the patients list.
# We start from each patient and assign them a hospital. If the hospital is not paired it directly add the current patient to the *pairs* dictionary.
# If the hospital is already paired, then it checks whether the existing patient has a better ranking as compared to the current patient.
# Over here the ranking to be considered is with respect to hospital because hospital is the one that has to make the change. If the ranking of the new patient
# is better than the existing one, then switch the patient w.r.t hospital in pair, and the removed exisitng one should be popped back in the remaining_patient list.
# If rank is not better, then we add the current patient back to the list.



#get current guy highest preference hospital, pop it from exisiting list so it does not occur again.
def getHighestPrefHospital(patientsPreference, hospitalPreference):
    pass

#get hospital preference w.r.t to the patient from the hospitalPreferenceList.
def getHospitalPrefWRTPatient(hospitalName, patient, hospitalPreference):
    pass

#Patients - List Of Patients we want to assign hospitals to
#patientsPreference - Data of patient preference w.r.t to hospital e.g. { (P1, {H1 : 0, H2:1, H4:2, H3:5})
#hospitalPreference - Data of hospital preference w.r.t. to patient e.g. { (H1, {P1 : 0, P2:1, P4:2, P3:5})
def gale_shapely(Patients, Hospitals, patientsPreference, hospitalPreference):
    pairs = dict() #Dictionary list of (Hospital_Name(Key), (Patient_name, Preference_No)(value))
    remaining_patients = set(Patients)

    while len(remaining_patients) > 0: # Run the code till all patients are assigned
        patient = remaining_patients.pop() #Patient List
        highestPreferenceHospital = getHighestPrefHospital(patientsPreference, hospitalPreference)
        hospitalName = highestPreferenceHospital[0] #(Hospital_name)
        pairsData = pairs.get(hospitalName) #(Patient_name, Preference_No)

        if pairsData is None: # If no pair against hospital is found directly add
            pairs[hospitalName] = (patient, getHospitalPrefWRTPatient(hospitalName, patient, hospitalPreference))
            #we are using hospital preference w.r.t patient and not the other way.
        else:

            allocatedPatientPreference = pairsData[1] #Hospital preference against Patient (Example of pairsData = (patient_name, hospitalprefw.r.tpatient))
            if allocatedPatientPreference < getHospitalPrefWRTPatient(hospitalName, patient): #if existing pair hospital preference rank is lower than the current one
                remaining_patients.add(patient) #no change add the exisiting patient back to the list

            else:
                remaining_patients.add(pairsData[0]) #current patient rank is better so add previous patient back into the list and add current patient against the hospital
                pairs[hospitalName] = (patient, getHospitalPrefWRTPatient(hospitalName, patient))

    return pairs