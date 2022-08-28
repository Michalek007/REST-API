from views import *
from periodic_tasks import *
from configuration import Config


if __name__ == '__main__':
    app.config.from_object(Config())
    app.run(debug=True)
