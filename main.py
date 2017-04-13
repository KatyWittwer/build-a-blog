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
from google.appengine.ext import db

s = cgi.escape( """& < >""" )

# set up jinja
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class Post(db.Model):
    title = db.StringProperty(required = True)
    body = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

#defaults to the new link with /blog instead of just /
class Mainhandler(webapp2.RequestHandler):
    def get(self):
        self.redirect('/blog')

class MainPage(webapp2.RequestHandler):
    def get(self):
        blog_posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 5")
        t = jinja_env.get_template("mainpage.html")
        content = t.render(posts = blog_posts)
        self.response.write(content)

class NewPost(webapp2.RequestHandler):
    def get(self):
        t = jinja_env.get_template("NewPost.html")
        content = t.render(title = "", body = "")
        self.response.write(content)

    def post(self):
        title = self.request.get("title")
        body = self.request.get("body")
        if title and body:
            p = Post(title = title, body = body)
            key = p.put()
            self.redirect("/blog/%d" % key.id())
        else:
            error = "Please add a Title and a Body."
            t = jinja_env.get_template("NewPost.html")
            content = t.render(title = title, body = body, error = error)
            self.response.write(content)

class ViewPost(webapp2.RequestHandler):
    def get(self, post_id):
        blog_post = Post.get_by_id(int(post_id))
        t = jinja_env.get_template("ViewPost.html")
        content = t.render(post = blog_post)
        self.response.write(content)

        if not blog_post:
            self.response.write("error 404")

app = webapp2.WSGIApplication([
    ('/', Mainhandler),
    ('/blog', MainPage),
    ('/blog/newpost', NewPost),
    webapp2.Route('/blog/<post_id:\d+>', ViewPost),
], debug=True)
