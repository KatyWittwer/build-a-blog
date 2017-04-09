#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import jinja2
import os
#set up google db
from google.appengine.ext import db

s = cgi.escape( """& < >""" )

# set up jinja
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Posts(db.Model):
    title = db.StringProperty(required = True)
    body = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

    #def render(self):
class Mainhandler(Handler):
    def get(self):
        self.redirect('/blog')

class MainPage(Handler):
        def get(self):
            p = db.GqlQuery("SELECT * FROM Posts LIMIT 5")
            self.render("mainpage.html", p = p)

class ViewPost(Handler):
    def get(self, id):
        blog_post = Posts.get_by_id(int(id))
        self.render("viewpost.html", blog_post = blog_post)

        if not blog_post:
            error = "No post found by that id number"
            self.render(error)

class NewPost(Handler):
    def get(self):
        self.render("newpost.html")

    def post(self):
        title = self.request.get("title")
        body = self.request.get("body")

        if title and body:
            p = Posts(title = title, body = body)
            p.put()
            self.redirect('/')
        else:
            error = "Submit a post with a title and body, please!"
            self.render("newpost.html", title = title, content = content, error = error)

app = webapp2.WSGIApplication([
    ('/', Mainhandler),
    ('/blog', MainPage),
    ('/blog/newpost', NewPost),
    webapp2.Route('/blog/<id:\d+>', ViewPost),
], debug=True)
