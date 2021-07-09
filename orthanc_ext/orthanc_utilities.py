"""
Convenience methods to work with the Orthanc REST API
"""


def anonymize(client, series_id):
    request = {'Force': False, 'KeepPrivateTags': True, 'Permissive': True, }
    resp = client.post(f'{series_id}/anonymize', json=request)
    resp.raise_for_status()
    return resp.json()


def get_metadata_of_first_instance_of_series(client, series_id, metadata_key):
    instances = client.get(f'/series/{series_id}/instances').json()
    assert len(instances) > 0, f'expected at least one instance in series {series_id}'
    resp = client.get(f'/instances/{instances[0]["ID"]}/metadata/{metadata_key}')
    resp.raise_for_status()
    return resp.text
