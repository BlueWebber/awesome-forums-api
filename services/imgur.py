from imgurpython import ImgurClient
from os import environ

client_id = environ.get('imgur_client_id')
client_secret = environ.get('imgur_client_secret')

client = ImgurClient(client_id, client_secret)


def upload_from_path(path):
    result = client.upload_from_path(path)
    return get_image_by_id(result["id"])


def get_image_by_id(image_id):
    obj = client.get_image(image_id)
    return obj.link


def upload_from_bytes(bytes_obj):
    result = client.upload(bytes_obj)
    return get_image_by_id(result["id"])
