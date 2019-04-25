import base64
import os

import tornado.web

from user.models import create_db, User
from utils.conn import session
from utils.faceid import register_face_user, match_face
from utils.settings import IMAGE_DIR


class RegisterHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('register.html')

    def post(self, *args, **kwargs):
        face = self.get_argument('face')
        username = self.get_argument('username')
        if not (face and username):
            self.render('register.html', error='注册信息请填写完整')
        user = session.query(User).filter(User.username == username).first()
        if user:
            self.render('register.html', error='该账号已被使用')
        img = face.split(',')[-1]
        if not register_face_user(img, username):
            self.render('register.html', error='注册失败')
        user = User()
        user.username = username
        session.add(user)
        session.commit()
        file = base64.b64decode(img)
        img_dir = os.path.join(IMAGE_DIR, username + '.jpg')
        with open(img_dir, 'wb') as f:
            f.write(file)
        self.write('注册成功')


class InitDBHandler(tornado.web.RequestHandler):
    def get(self):
        create_db()
        self.write('初始化数据库成功')


class LoginHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('login.html')

    def post(self, *args, **kwargs):
        face = self.get_argument('face')
        username = self.get_argument('username')
        if not (face and username):
            self.render('login.html', error='请填写完整信息')
            return
        user = session.query(User).filter(User.username == username).first()
        if not user:
            self.render('login.html', error='用户没有注册')
            return
        img = face.split(',')[-1]
        file = os.path.join(IMAGE_DIR, username + '.jpg')
        file_exists = os.path.exists(file)
        if not file_exists:
            self.render('login.html', error='该账号没有注册')
            return
        score = match_face(img, file)
        if score < 80:
            self.render('login.html', error='匹配不成功')
            return
        self.set_cookie('username', username)
        self.write('登录成功,人脸匹配度为：{0:.2f}%'.format(score))


