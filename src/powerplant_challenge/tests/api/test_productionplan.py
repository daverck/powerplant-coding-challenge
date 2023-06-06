import json

from src.powerplant_challenge.core.config import settings


def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def test_payload_3(client):
    with open("src/powerplant_challenge/tests/example_payloads/payload3.json") as f:
        json_payload = json.load(f)

        # When
        response = client.post(
            url=f"{settings.API_V1_STR}/productionplan",
            json=json_payload,
        )

        # Then
        assert response.status_code == 200

    data = response.json()
    with open("src/powerplant_challenge/tests/example_payloads/response3.json") as f2:
        json_payload2 = json.load(f2)

        assert ordered(data) == ordered(json_payload2)


def test_payload_1(client):
    with open("src/powerplant_challenge/tests/example_payloads/payload1.json") as f:
        json_payload = json.load(f)

        # When
        response = client.post(
            url=f"{settings.API_V1_STR}/productionplan",
            json=json_payload,
        )

        # Then
        assert response.status_code == 200

    data = response.json()
    with open("src/powerplant_challenge/tests/example_payloads/response1.json") as f2:
        json_payload2 = json.load(f2)

        assert ordered(data) == ordered(json_payload2)


def test_payload_2(client):
    with open("src/powerplant_challenge/tests/example_payloads/payload2.json") as f:
        json_payload = json.load(f)

        # When
        response = client.post(
            url=f"{settings.API_V1_STR}/productionplan",
            json=json_payload,
        )

        # Then
        assert response.status_code == 200

    data = response.json()
    with open("src/powerplant_challenge/tests/example_payloads/response2.json") as f2:
        json_payload2 = json.load(f2)

        assert ordered(data) == ordered(json_payload2)