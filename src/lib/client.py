# Batteries
import os

# External
import evernote.edam.userstore.constants as UserStoreConstants

from evernote.api.client import EvernoteClient


def new_client() -> EvernoteClient:
    auth_token = os.environ['EVERNOTE_PROD_DEV_TOKEN']
    sandbox = False
    china = False

    client = EvernoteClient(token=auth_token, sandbox=sandbox, china=china)

    user_store = client.get_user_store()

    version_ok = user_store.checkVersion(
        'Ilirium Bunch of Scripts (Python v3)',
        UserStoreConstants.EDAM_VERSION_MAJOR,
        UserStoreConstants.EDAM_VERSION_MINOR
    )

    if not version_ok:
        raise Exception('It is not compatible version of EDAM and Evernote SDK')

    return client
