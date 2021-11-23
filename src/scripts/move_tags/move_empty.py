# Batteries
import os
import math
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


def load_tags(path_file: Path):
    df = pd.read_csv(path_file)
    return df


def move_empty(empty_parent_guid: str, client: EvernoteClient, token: str, tags_df: pd.DataFrame):
    note_store = client.get_note_store()

    empty_df = tags_df.query('assigned_notes == 0')

    for idx in range(empty_df.shape[0]):
        name = empty_df.iloc[idx]['name']
        guid = empty_df.iloc[idx]['guid']
        if name[0] != '#':
            print(name)
            retrieved_tag = note_store.getTag(token, guid)
            print(f'old = {retrieved_tag}')
            parent_guid = retrieved_tag.parentGuid
            if math.isnan(parent_guid):
                tag = Tag(guid=guid, parentGuid=empty_parent_guid, name=name)
                update_sequence_number = note_store.updateTag(token, tag)
                retrieved_tag = note_store.getTag(token, guid)
                print(f'new = {retrieved_tag}')
                print()

def get_tag_by_name(client: EvernoteClient, token: str, tag_name: str):
    note_store = client.get_note_store()
    tags = note_store.listTags()
    for tag in tags:
        if tag.name == tag_name:
            return tag

    return None

if __name__ == '__main__':
    token = os.environ['EVERNOTE_PROD_DEV_TOKEN']
    client = new_client()

    path_csv_tags = Path('.') / 'tags_list_2021-11-22.csv'
    tags_df = load_tags(path_csv_tags)

    tag_parent_for_empty_name = '#EMPTY'

    tag_parent_for_empty = get_tag_by_name(client, token, tag_parent_for_empty_name)
    print(f'*** Empty tag = {tag_parent_for_empty}\n')
    tag_parent_for_empty_guid = tag_parent_for_empty.guid

    move_empty(tag_parent_for_empty_guid, client, token, tags_df)
