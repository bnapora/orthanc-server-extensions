import orthanc, sys, json, requests, inspect, numbers, pprint
   
def study_stable_to_rest(changeType, level, resourceId):
    if changeType == orthanc.ChangeType.STABLE_STUDY:
        print('Stable study: %s' % resourceId)
        study_metadata = json.loads(orthanc.RestApiGet(f'/studies/{resourceId}'))
        print(f'StudyMetadataJSON={study_metadata}')
        
        # study_shared_metadata = json.loads(orthanc.RestApiGet(f'/studies/{resourceId}/shared-tags'))
        # print(f'StudySharedMetadataJSON={study_shared_metadata}')
        
        studyinstanceUid = study_metadata['MainDicomTags']['StudyInstanceUID']
        print(f'StudyInstanceUID={studyinstanceUid}')
        
        # study_dicomweb_metadata = json.loads(orthanc.RestApiGetAfterPlugins(f'/dicom-web/studies/{studyinstanceUid}/metadata'))    
        # print(f'StudyDICOMWebMetadataJSON={study_dicomweb_metadata}')

        studyUid = study_metadata['MainDicomTags']['StudyInstanceUID']
        if studyUid is None or studyUid == '':
          raise Exception("Cannot send StudyMetadata without StudyInstanceUID")

        # Medplum Application Auth
        client_application_id = 'dea997cc-8954-4787-a193-d2450f86009e'
        client_secret = 'cfdacdb6e518f9f439463d24baf2fde5234407ddbd70573a254cc4e76c3b49a2'
        url_medplum = f'http://{client_application_id}:{client_secret}@host.docker.internal:8103/fhir/R4/Bot/9a63c1df-fd82-4f2b-9d37-0517faae59c8/$execute'
        print(f'URL_MEDPLUM={url_medplum}')
        
        # # Format URL Request
        # response = requests.request(
        #     method="POST",
        #     url=url_medplum,
        #     headers={'Content-Type': 'application/json'},
        #     data=study_metadata
        # )
        # print(response.text)
        
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
        
orthanc.RegisterOnChangeCallback(study_stable_to_rest)
