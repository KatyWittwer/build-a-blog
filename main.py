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
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

#Displays the five most recent posts (use filtering)

class blogposts(db.Model):
    title = db.StringProperty(required = True)
    body = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

    #def render(self):

class MainPage(webapp2.RequestHandler):
        def get(self):
            blogposts = db.GqlQuery("SELECT * FROM blogposts LIMIT 5")
            t = jinja_env.get_template("mainpage.html")
            content = t.render(blogposts = blogposts)
            self.response.write(content)

class ViewPost(webapp2.RequestHandler):
    def get(self, id):
        blogposts = (blogposts.get_by_id)

    #if not post:
    #    error = "No post found"
    #    self.write(error)

class NewPost(webapp2.RequestHandler):
    def get(self):
        t = jinja_env.get_template("newpost.html")
        content = t.render()
        self.response.write(content)
    def post(self):
        title = self.request.get("title")
        body = self.request.get("body")

        if title and body:
            b = blogposts(title = title, body = body)
            b.put()
            self.redirect('/blog')
        else:
            self.renderError(400)
            return

            self.render("newpost.html", title = title, content = content, error = error)

app = webapp2.WSGIApplication([
    ('/blog', MainPage),
    ('/blog/newpost', NewPost),
    ('/blog/<id:\d+>', ViewPost)
], debug=True)
