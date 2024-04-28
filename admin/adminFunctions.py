import os

from models import UploadedMedia
from server import db


def delete_media(media_id):
    try:
        image = UploadedMedia.query.filter_by(id=media_id).first()
        if image is not None:
            image_path = '/home/babatee/oh-server' + image.path + '/' + image.filename
            if os.path.exists(image_path):
                os.remove(image_path)
                db.session.delete(image)
                db.session.commit()
                return 1
            else:
                return image_path
        else:
            return 3
    except Exception as e:
        print('Failed to delete image {}- {}'.format(media_id, e))
        return 4
