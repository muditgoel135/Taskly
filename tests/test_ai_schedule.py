def test_ai_schedule(client):
    payload = {
        'tasks':[{'title':'Essay','duration':60,'due':'2025-09-20','priority':2}],
        'prefs':{'start_hour':16,'end_hour':21,'break_min':5},
        'constraints':{}
    }
    r = client.post('/api/v1/ai/schedule', json=payload)
    assert r.status_code == 200
    assert 'blocks' in r.get_json()
