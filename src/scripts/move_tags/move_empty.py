# Batteries
import os

# External
from evernote.edam.notestore import NoteStore
from evernote.api.client import EvernoteClient

from tqdm import tqdm

# Lib
from src.lib.client import new_client


def count_notes_in_tags(client: EvernoteClient, token: str):
    note_store = client.get_note_store()
    tags = note_store.listTags()

    empty_tags_lst = []
    tags_dct = {}

    for tag in tqdm(tags):
        filter = NoteStore.NoteFilter()
        filter.tagGuids = [tag.guid, ]
        spec = NoteStore.NotesMetadataResultSpec()
        note_list = note_store.findNotesMetadata(token, filter, 0, 100, spec)
        if note_list.totalNotes == 0:
            empty_tags_lst.append(tag)
        else:
            tags_dct[tag] = note_list.totalNotes

    return tags_dct, empty_tags_lst


if __name__ == '__main__':
    token = os.environ['EVERNOTE_PROD_DEV_TOKEN']
    client = new_client()

    tags_dct, empty_tags_lst = count_notes_in_tags(client, token)
    print(empty_tags_lst)
