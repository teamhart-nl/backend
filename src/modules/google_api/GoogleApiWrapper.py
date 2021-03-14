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

    def __init__(self, credentials_path=None):

        cred = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        # no global environment variable for the credentials
        if (cred is None):
            # no path is given manually, so cannot authenticate
            if (credentials_path is None):
                Logger.log_info("GoogleApiWrapper.checkGoogleApiConnection: Currently, no google credentials are set. "
                    "Operations that use the Google API will therefore not work until you set your credentials "
                    "and restart the application. "
                    "Either place the credentials in the //resources// named gcloud_'credentials.json' "
                    "or set global env variable 'GOOGLE_APPLICATION_CREDENTIALS' appropriately.")
                return
            # set the global variable to the credentials in the resources folder
            else:
                self.setCredentials(credentials_path)
        # global environment is set, but the file does not exist
        elif not os.path.isfile(cred):
            # no alternative path is given, so cannot authenticate
            if (credentials_path is None):
                Logger.log_info("GoogleApiWrapper.checkGoogleApiConnection: Currently, no google credentials are set. "
                    "the file " + cred + " was not found. "
                    "Either place the credentials in the //resources// named gcloud_'credentials.json' "
                    "or set global env variable 'GOOGLE_APPLICATION_CREDENTIALS' appropriately.")
                return
            # set the global variable to the credentials in the resources folder
            else:
                self.setCredentials(credentials_path)

        # Check if the Google API can be authenticated
        self.checkGoogleApiConnection()

    def checkGoogleApiConnection(self):
        # Logging general information
        Logger.log_info("GoogleApiWrapper.checkGoogleApiConnection: Checking connection to Google API")
        cred = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        Logger.log_info("GoogleApiWrapper.checkGoogleApiConnection: Currently, "
                        "using credentials: " + cred)
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
        except DefaultCredentialsError as e:
            # Logging information that connection has failed
            Logger.log_warning("GoogleApiWrapper.checkGoogleApiConnection: "
                               "Could not connect to Google API")
            Logger.log_warning(e)
            Logger.log_warning("GoogleApiWrapper.checkGoogleApiConnection: "
                               "Make sure to set you google credentials correctly!")

    def setCredentials(self, credential_path):
        Logger.log_info("GoogleApiWrapper.checkGoogleApiConnection: "
                        "Overwriting global env variable for gcloud credentials to " + credential_path)
        # set environment variable.
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
