from utils.serializers import convert_b64_to_bytes
from PIL import Image as Img
from services.imgur import upload_from_bytes
from config import config
from io import BytesIO
from filetype import guess
from utils.gif_resizer import resize_gif


class _MediaBase:
    def __init__(self, b64string, max_size, allowed_formats):
        assert ((max_size * 4) / 3) > len(b64string), f"Media is too large, must be smaller than {max_size} bytes"
        self.bytes = BytesIO(convert_b64_to_bytes(b64string))
        self.extension = guess(self.bytes).extension
        assert self.extension in allowed_formats, "Invalid media format, must be in allowed formats"
        self.link = None

    def upload(self):
        try:
            self.bytes.seek(0)
            self.link = upload_from_bytes(self.bytes)
        except Exception as ex:
            print(ex)
            raise RuntimeError(f"Failed uploading, status: {ex}")
        else:
            return self.link


class ByteImage(_MediaBase):
    def __init__(self, b64string, img_format=config.IMAGE_FORMAT):
        super().__init__(b64string, config.MAX_IMAGE_SIZE, config.ALLOWED_IMAGE_FORMATS)
        if self.extension == config.ANIMATED_IMAGE_FORMAT.lower():
            self.format = config.ANIMATED_IMAGE_FORMAT
        else:
            self.format = img_format
        new_img = Img.open(self.bytes)
        if "duration" in new_img.info:
            self.duration = new_img.info["duration"]
        self.aspect_ratio = new_img.size[0] / new_img.size[1]
        self.size = new_img.size

    def resize(self, new_size: tuple = config.PFP_SIZE):
        new_img = None
        assert (new_size[0] / new_size[1]) == self.aspect_ratio, "New size's aspect ratio must be the same as " \
                                                                 "current image's aspect ratio"
        if self.format == config.ANIMATED_IMAGE_FORMAT:
            self.bytes = resize_gif(self.bytes, self.duration, new_size)
        else:
            out = BytesIO()
            new_img = Img.open(self.bytes)
            new_img.resize(new_size)
            new_img.save(out)
            out.seek(0)
            self.bytes = out
        if not new_img:
            new_img = Img.open(self.bytes)
        self.aspect_ratio = new_img.size[0] / new_img.size[1]
        self.size = new_img.size


class ByteVideo(_MediaBase):
    def __init__(self, b64string):
        super().__init__(b64string, config.MAX_VID_SIZE, config.ALLOWED_VIDEO_FORMATS)
