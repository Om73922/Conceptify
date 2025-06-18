import streamlit as st
import requests
from io import BytesIO

def get_image(image_url):
    """
    Fetch an image from a given URL and return a BytesIO object.

    Parameters:
    - image_url (str): The URL of the image to download.

    Returns:
    - BytesIO: Image data if successful.
    - None: If there is any error during fetch.
    """
    print(f" Starting image download from: {image_url}")

    try:
        # Send a GET request to fetch the image
        response = requests.get(image_url, timeout=20)
        print(f" HTTP status code received: {response.status_code}")

        # Raise an error if status code is not 200 OK
        response.raise_for_status()

        # Wrap the content in BytesIO
        image_data = BytesIO(response.content)
        print(f" Image download successful. Image size: {len(response.content)} bytes")

        return image_data

    except requests.exceptions.HTTPError as http_err:
        print(f" HTTP error: {http_err}")
    except requests.exceptions.ConnectionError:
        print(" Connection error: Could not retrieve the image.")
    except requests.exceptions.Timeout:
        print(" Request timed out.")
    except requests.exceptions.RequestException as req_err:
        print(f" Request error: {req_err}")
    except Exception as e:
        print(f" Unexpected error: {e}")

    # Return None if any error occurred
    return None
