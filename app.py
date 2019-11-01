#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import json
import tornado
import tornado.web
import tornado.ioloop
import tornado.httpserver
from tornado.log import app_log as log
from tornado.options import define, options, parse_command_line

define("port", default=8080, help="run on the given port", type=int)

class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        return self.get_secure_cookie("username")


class DashHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self):
        self.render('index.html')

    @tornado.gen.coroutine
    def post(self):
        log.warn("I shouldn't be getting post requests")

class PhotoHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        log.info('got request for photohandler')
        self.render('photoviewer.html')

    @tornado.gen.coroutine
    def post(self):
        log.warn("I shouldn't be getting post requests for photohandler")


class InvitationHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self):
        log.info("got request for InvitationHandler")
        self.render('invitation.html')

    @tornado.gen.coroutine
    def post(self):
        log.warn("I shouldn't be receiving post requests for invitationhandler")
        
class UserTableHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self):
        log.info('get request for UserTableHandler')
        self.render('tables.html')

    @tornado.gen.coroutine
    def post(self):
        log.warn("I shouldn't be gettng post requests")

class DBHandler(BaseHandler):

    def set_default_headers(self):
        log.info("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET')

    def options(self):
        # no body
        #self.set_status(204)
        self.finish()

    @tornado.gen.coroutine
    def get(self):
        with open("test/test_invites.txt", 'r') as fh:
            #data = fh.readlines()
            data = json.load(fh)
        self.write('{{"data": {}}}'.format(json.dumps(data)))
        self.finish()

    @tornado.gen.coroutine
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        log.info("Data received in POST: {}".format(data))
        return "{'response': 'OK'}"

class Application(tornado.web.Application):
    def __init__(self):
        base_dir = os.path.dirname(__file__)
        settings = {
            "cookie_secret": "123", # Change this in prod
            "login_url": "/auth/login",
            'template_path': os.path.join(base_dir, "templates"),
            'static_path': os.path.join(base_dir, "static"),
            'debug':True,
            "xsrf_cookies": False,
        }
        tornado.web.Application.__init__(self, [
            tornado.web.url(r'/invitation/.*', InvitationHandler, name='invitationhandler'),
            # Testing photoviewer
            tornado.web.url(r'/photoviewer/.*', PhotoHandler, name='photohandler'),
            tornado.web.url(r'/dashboard/.*', DashHandler, name="dashhandler"),
            tornado.web.url(r'/tables/.*', UserTableHandler, name="usertablehandler"),
            tornado.web.url(r'/update_record/.*', DBHandler, name="dbhandler"),
        ], **settings)

if __name__ == "__main__":
    parse_command_line()
    Application().listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
