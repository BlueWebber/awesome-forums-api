import json
import base64


class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return super().default(obj)
        except TypeError:
            return str(obj)


def convert_b64_to_image(b64_string):
    return base64.decodebytes(b64_string.encode())

