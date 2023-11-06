
from jinja2 import Template
import datetime
from flask import Flask

app = Flask(__name__)


app.config.from_object(Config)



def create_app(config_class=Config):
    app.jinja_loader = Template("{% extends 'template_folder' %}")

    

# Creating blueprint configuration for app
    from ._web_utils.api import web_tool


# registering packages to blueprint
    app.register_blueprint(web_tool)

    return app