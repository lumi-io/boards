import json

def test_submission(test_client):
    """ Test for application submission """
    def submission(client, posting_id):
        data = {
            "profilePic": "n",
            "elavatorPitch": "n",
            "resume": "n",
            "applicantName": "John Chai",
            "graduatingYear": 2023,
            "phoneNumber": "8178001711",
            "GPA": 3.9,
            "major": "CS",
            "college": "CAS",
            "email": "jchai23@bu.edu",
            "role": "applicant"
        }
        response = client.post(
            f"/user/applications/submit/{posting_id}",
            json=data
        )
        return response
    #test for correct posting_id
    assert submission(test_client, "5fec8dd5bf32a87a49998afd").status_code == 400

    #test for incorrect posting_id
    assert submission(test_client, "5fec8dd5bf32a87a49998ajk").status_code == 200
