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

class DBHandler(tornado.web.RequestHandler):
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
        # self.write('{{"data": {}}}'.format([x.strip().strip(',') for x in data]))
        #self.write('{{"data": [{},{}]}}'.format(data[0].strip().strip(','),
        #                                        data[1].strip().strip(',')))
        #self.write('[{}]'.format(json.dumps(data[0].strip().strip(','))))
        #self.write('[{"id":"99", "name":"Oli Bob", "progress":12, "gender":"male", "rating":1, "col":"red", "dob":"19/02/1984", "car":1, "lucky_no":5, "activity":[1, 20, 5, 3, 10, 13, 17, 15, 9, 11, 10, 12, 14, 16, 13, 9, 7, 11, 10, 13]}]')
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
            tornado.web.url(r'/update_record/.*', DBHandler, name="dbhandler"),
        ], **settings)

if __name__ == "__main__":
    parse_command_line()
    Application().listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
