#coding = utf-8
import os
from flask_migrate import MigrateCommand, Migrate
from flask_script import Manager
from smalldragonsblog.models import db , User , Role , Post , Comment , users_roles , Tag
from smalldragonsblog import create_app
from flask_script import Server

env = os.environ.get('WEBAPP_ENV' , 'dev')
app = create_app('smalldragonsblog.config.%sConfig' % env.capitalize())

manager = Manager(app)
migrate = Migrate(app , db)
manager.add_command('db' , MigrateCommand)
manager.add_command('server' , Server())

@manager.shell
def make_shell_context():

    return dict(app=app,
                db=db,
                User=User,
                Post=Post,
                Role=Role,
                Server=Server,
                Comment=Comment,
                Tag=Tag)

if __name__ == '__main__':
    manager.run()