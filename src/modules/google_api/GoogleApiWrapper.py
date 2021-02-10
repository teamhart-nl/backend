import os

from google.auth.exceptions import DefaultCredentialsError
from google.cloud import storage

from src.helpers.Logger import Logger
from src.helpers.SingletonHelper import Singleton


class GoogleApiWrapper(metaclass=Singleton):
    """
    Wrapper for authenticating with the Google API.
    Does not check for whether the Google API is installed.
    Only checks for whether it can authenticate.
    TODO be able to (cross-os) check whether Google API is installed
    """

    # Stores whether the Google API is authenticated correctly
    authenticated: bool = False

    def __init__(self):
        # Check if the Google API is set up correctly
        self.checkGoogleApiConnection()

    def checkGoogleApiConnection(self):
        # Logging general information
        Logger.log_info("GoogleApiWrapper.checkGoogleApiConnection: Checking connection to Google API")
        Logger.log_info("GoogleApiWrapper.checkGoogleApiConnection: Currently, "
                        "the path to your credentials file is set to: " +
                        os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'))

        try:
            # If you don't specify credentials when constructing the client, the
            # client library will look for credentials in the environment.
            storage_client = storage.Client()

            # Make an authenticated API request
            buckets = list(storage_client.list_buckets())

            # Setting authentication to true
            self.authenticated = True

            # Logging info that connection has succeeded
            Logger.log_info("GoogleApiWrapper.checkGoogleApiConnection: "
                            "Google API credentials accepted, connection succeeded!")
        except DefaultCredentialsError:
            # Logging information that connection has failed
            Logger.log_warning("GoogleApiWrapper.checkGoogleApiConnection: "
                               "Could not connect to Google API")
            Logger.log_warning("GoogleApiWrapper.checkGoogleApiConnection: "
                               "Make sure to set you google credentials correctly!")

    def setCredentials(self, credential_path):
        # set environment variable.
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

        # check connection to google api again.
        self.checkGoogleApiConnection()
