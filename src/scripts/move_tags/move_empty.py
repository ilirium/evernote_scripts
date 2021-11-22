# Batteries
import os
import time

from pathlib import Path
from typing import Dict

# External
import pandas as pd

import evernote.edam.error as Errors
from evernote.api.client import EvernoteClient
from evernote.edam.notestore import NoteStore
from evernote.edam.type.ttypes import Tag


from tqdm import tqdm

# Lib
from src.lib.client import new_client


def count_notes_in_tags(client: EvernoteClient, token: str):
    note_store = client.get_note_store()
    tags = note_store.listTags()

    tags_dct = {}

    i = 0
    for tag in tqdm(tags):
        # print(tag)
        # Tag(guid='681d674e-2085-41f6-ad14-d0a9aa3eb51d', name='classification', parentGuid=None, updateSequenceNum=17)
        filter = NoteStore.NoteFilter()
        filter.tagGuids = [tag.guid, ]
        spec = NoteStore.NotesMetadataResultSpec()
        try:
            note_list = note_store.findNotesMetadata(token, filter, 0, 100, spec)
        except Errors.EDAMSystemException as e:
            if e.errorCode == Errors.EDAMErrorCode.RATE_LIMIT_REACHED:
                print('\n*** rate limit reached\n')
                print('\n*** retry your request in %d seconds\n' % e.rateLimitDuration)
                time.sleep(e.rateLimitDuration)
        else:
            tags_dct[tag] = note_list.totalNotes

        i += 1
        if i == 50:
            save_tags(tags_dct)
            print("\n*** saved\n")
            i = 0

    save_tags(tags_dct)
    return tags_dct


def save_tags(tags_dct: Dict[Tag, int]):
    lst = []

    for tag in tags_dct.keys():
        one = {'name': tag.name, 'assigned_notes': tags_dct[tag],
               'guid': tag.guid, 'parentGuid': tag.parentGuid, 'updateSequenceNum': tag.updateSequenceNum}
        lst.append(one)

    df = pd.DataFrame(lst)
    dt = time.strftime('%Y-%m-%d_%H:%M:%S', time.gmtime())
    path = Path('.') / f'tags_list_{dt}.csv'
    df.to_csv(path)



if __name__ == '__main__':
    token = os.environ['EVERNOTE_PROD_DEV_TOKEN']
    client = new_client()

    tags_dct = count_notes_in_tags(client, token)
