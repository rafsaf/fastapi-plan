__version__ = "0.1.0"

from fastapi_template.greet_command import GreetCommand
from cleo import Application

application = Application()
application.add(GreetCommand())


def start():
    application.run()
