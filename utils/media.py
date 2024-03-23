from utils.serializer import convert_b64_to_image
from PIL import Image as Img
from services.imgur import upload_from_bytes
from config import config
from io import BytesIO


class Image:
    def __init__(self, b64string, img_format=config.IMAGE_FORMAT):
        self.error = None
        self.format = img_format
        img_data = BytesIO(convert_b64_to_image(b64string))
        self.image = Img.open(img_data)
        self.aspect_ratio = self.image.size[0] / self.image.size[1]
        self.link = None

    def upload(self):
        try:
            self.link = upload_from_bytes(self._image_to_bytes())
        except Exception as ex:
            print(ex)
            self.error = ex
            return False
        else:
            self.clean_up()
            return self.link

    def _image_to_bytes(self):
        img_bytes = BytesIO()
        self.image.save(img_bytes, format=self.format)
        img_bytes.seek(0)
        return img_bytes

    def resize(self, new_size: tuple = config.PFP_SIZE):
        new_img = self.image.resize(new_size)
        self.image.close()
        self.image = new_img

    def clean_up(self):
        self.image.close()


class Video:
    def __init__(self, b64string, video_format=config.VIDEO_FORMAT):
        pass
