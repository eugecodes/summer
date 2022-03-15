import os

port = int(os.environ.get('PORT', 5000))

# We want to run seamlessly our API both locally and on Heroku, so:
if os.environ.get('PORT'):
    # We're hosted on Heroku! Use the MongoHQ sandbox as our backend.
    MONGO_HOST = '0.0.0.0'
    MONGO_PORT = port
else:
    # Running on local machine. Let's just use the local mongod instance.

    # Please note that MONGO_HOST and MONGO_PORT could very well be left
    # out as they already default to a bare bones local 'mongod' instance.
    MONGO_HOST = 'localhost'
    MONGO_PORT = 5000