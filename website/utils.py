# 自定義共用函式
import os
from uuid import uuid4
from django.utils.deconstruct import deconstructible

# 媒體上傳路徑，並會將檔案檔名改為uuid
# def media_path_rename_uuid4(file_path):
#     def wrapper(instance, filename):
#         ext = filename.split('.')[-1]
#         # set filename as random string
#         filename = '{}.{}'.format(uuid4().hex, ext)
#         # return the whole path to the file
#         return os.path.join(file_path, filename)
#     return wrapper

@deconstructible
class MediaPathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)