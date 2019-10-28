from flask_admin.contrib.sqla import ModelView
import sqlite3 as sql
class User():
    pass

class MicroBlogModelView(ModelView):
    can_delete = False  # disable model deletion
    page_size = 50  # the number of entries to display on the list view

admin.add_view(MicroBlogModelView(User, db.session))
admin.add_view(MicroBlogModelView(Post, db.session))