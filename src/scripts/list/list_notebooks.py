# Batteries
import os

# External
import evernote.edam.userstore.constants as UserStoreConstants

from evernote.api.client import EvernoteClient


# Step: Authorization
auth_token = os.environ["EVERNOTE_PROD_DEV_TOKEN"]
sandbox = False
china = False

client = EvernoteClient(token=auth_token, sandbox=sandbox, china=china)

user_store = client.get_user_store()

version_ok = user_store.checkVersion(
    "Evernote EDAMTest (Python)",
    UserStoreConstants.EDAM_VERSION_MAJOR,
    UserStoreConstants.EDAM_VERSION_MINOR
)
print("Is my Evernote API version up to date? ", str(version_ok))
print("")
if not version_ok:
    exit(1)

note_store = client.get_note_store()

# Step: List all of the notebooks in the user's account
notebooks = note_store.listNotebooks()
print("Found ", len(notebooks), " notebooks:")
for notebook in notebooks:
    print("  * ", notebook.name)
