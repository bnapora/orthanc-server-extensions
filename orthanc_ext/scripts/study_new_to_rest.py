'''
NOTE: The Orthanc Docker image won't contain additional packages, like requests. Therefore,
    you'll have to build your own image and add these dependencies using pip. See example at:
    https://stackoverflow.com/questions/66595413/getting-no-module-named-requests-with-jodogne-orthanc-python
'''
import orthanc, sys, json, requests, inspect, numbers, pprint

def InspectOrthancModule(object):
    # for (name, obj) in inspect.getmembers(object):
    #     if inspect.isroutine(obj):
    #         print('Function %s():\n  Documentation: %s\n' % (name, inspect.getdoc(obj)))
            
    #     elif inspect.isclass(obj):
    #         print('Class %s:\n  Documentation: %s' % (name, inspect.getdoc(obj)))

    #         # Loop over the members of the class
    #         for (subname, subobj) in inspect.getmembers(obj):
    #             if isinstance(subobj, numbers.Number):
    #                 print('  - Enumeration value %s: %s' % (subname, subobj))
    #             elif (not subname.startswith('_') and
    #                 inspect.ismethoddescriptor(subobj)):
    #                 print('  - Method %s(): %s' % (subname, inspect.getdoc(subobj)))
    #         print('')
    for attr, value in object.__dict__.items():
                print(attr, value)


# def study_new_to_rest(dicom, instanceId, **request):
def study_new_to_rest(changeType, level, resourceId, **request):
    print(f'changeType={changeType}')
    print(f'Level={level}')
    print(f'ResourceID={resourceId}')
    if changeType == orthanc.ChangeType.STABLE_STUDY:
        print('Stable study: %s' % resourceId)
    
    
        
        
        
    '''
    Sample request:
    {
        "AccessionNumber": "",
        "Level": "STUDY",
        "OriginatorAET": "BLAH",
        "OriginatorID": 1,
        "PatientID": "",
        "SOPInstanceUID": "",
        "SeriesInstanceUID": "",
        "SourceAET": "ORTHANC",
        "StudyInstanceUID": "1.3.6.1.4.1.14519.5.2.1.6279.6001.300027087262813745730072134723",
        "TargetAET": "BLAH"
    }
    '''
    # print('############# Start - Orthanc Object Iter')
    # InspectOrthancModule(orthanc)
    # print('############# End - Orthanc Object Iter')
    
    # print('############# Start - DICOM Object Iter')
    # InspectOrthancModule(dicom)
    # print('############# End - DICOM Object Iter')
    
    # print(f'InstanceID = {instanceId}')
    # level = request['Level']
    # if level != 'STUDY':
    #     raise Exception("Cannot handle any C-MOVE **not** on the STUDY level")

    study_uid = request['StudyInstanceUID'] if 'StudyInstanceUID' in request else None
    # target_aet= request['TargetAET']
    target_aet='MIRTH'

    if study_uid is None or study_uid == '':
        raise Exception("Cannot handle any C-MOVE without Study Instance UID")

    # Make call to RESTful API and provide these two bits of information
    # GET Example
    url = f"https://myserver/endpoint?study_uid={study_uid}&target_aet={target_aet}"
    print(url)
    response = requests.request(
        method="GET",
        url=url,
        headers={'Content-Type': 'application/json'}
    )
    print(response.text)

    # POST payload Example
    '''
    payload = {'study_uid':study_uid, 'target_aet': target_aet}
    response = requests.request(
        method="POST",
        url="https://myserver/endpoint",
        headers={'Content-Type': 'application/json'},
        data=payload
    )
    print(response.text)
    '''
def OnStoredInstance(dicom, instanceId):
    print('Received instance %s of size %d (transfer syntax %s, SOP class UID %s)' % (
        instanceId, dicom.GetInstanceSize(),
        dicom.GetInstanceMetadata('TransferSyntax'),
        dicom.GetInstanceMetadata('SopClassUid')))

    # Print the origin information
    if dicom.GetInstanceOrigin() == orthanc.InstanceOrigin.DICOM_PROTOCOL:
        print('This instance was received through the DICOM protocol')
    elif dicom.GetInstanceOrigin() == orthanc.InstanceOrigin.REST_API:
        print('This instance was received through the REST API')
    # Print the DICOM tags
    # pprint.pprint(json.loads(dicom.GetInstanceSimplifiedJson()))
    pprint.pprint(json.loads(dicom.GetInstanceJson()))
    
def study_stable_to_rest(changeType, level, resourceId, **request):
    if changeType == orthanc.ChangeType.STABLE_STUDY:
        print('Stable study: %s' % resourceId)
        result = json.loads(orthanc.RestApiPost("/tools/lookup", resourceId))
        print(f'ResultJSON={result}')
        study_metadata = json.loads(orthanc.RestApiGet(f'/studies/{resourceId}'))
        print(f'StudyMetadataJSON={study_metadata}')
        study_shared_metadata = json.loads(orthanc.RestApiGet(f'/studies/{resourceId}/shared-tags'))
        print(f'StudySharedMetadataJSON={study_shared_metadata}')
        studyinstanceUid = study_metadata['MainDicomTags']['StudyInstanceUID']
        print(f'StudyInstanceUID={studyinstanceUid}')
        study_dicomweb_metadata = json.loads(orthanc.RestApiGetAfterPlugins(f'/dicom-web/studies/{studyinstanceUid}/metadata'))
        # study_dicomweb_metadata = json.loads(orthanc.RestApiGetAfterPlugins('/dicom-web/studies/1.2.826.0.1.3680043.8.498.13230779778012324449356534479549187420/metadata'))
        
        print(f'StudyDICOMWebMetadataJSON={study_dicomweb_metadata}')



# orthanc.RegisterOnStoredInstanceCallback(OnStoredInstance)
orthanc.RegisterOnChangeCallback(study_stable_to_rest)
# orthanc.RegisterOnChangeCallback(study_new_to_rest)
