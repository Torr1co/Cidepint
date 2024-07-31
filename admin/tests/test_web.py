from tests import client


def test_web():
    """
    Basic test to check if the web app is running
    """
    response = client.get("/")
    assert response.status_code == 200
