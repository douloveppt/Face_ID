import base64

from aip import AipFace

APP_ID = '16107099'
API_KEY = 'rxLjyBRzORyAszxGDmPOfjG4'
SECRET_KEY = 'cwHoAmfm7ecPi4tZgL2pNN2hBGBvjAQ0'

client = AipFace(APP_ID, API_KEY, SECRET_KEY)


def register_face_user(image, user_id, image_type='BASE64', group_id='user'):
    response = client.addUser(image, image_type, group_id, user_id)
    return False if response['error_code'] else True


def match_face(login_img, register_img):
    result = client.match([
        {
            'image': login_img,
            'image_type': 'BASE64',
        },
        {
            'image': base64.b64encode(open(register_img, 'rb').read()).decode('utf-8'),
            'image_type': 'BASE64',
        }
    ])
    return result['result']['score']
