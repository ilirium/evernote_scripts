# Batteries
import os
import math
import time

from pathlib import Path
from typing import List

# External
import pandas as pd
import regex

import evernote.edam.error as Errors
from evernote.api.client import EvernoteClient
from evernote.edam.notestore import NoteStore
from evernote.edam.type.ttypes import Tag

from tqdm import tqdm

# Lib
from src.lib.client import new_client


def sort(client: EvernoteClient, tags_lst: List[Tag], tag_rus: Tag, tag_eng: Tag):
    note_store = client.get_note_store()

    for tag in tqdm(tags_lst):
        if tag.name[0] == '#':
            pass
        elif tag.parentGuid is None:
            retrieved_tag = note_store.getTag(token, tag.guid)
            print(f'\nold = {retrieved_tag}')

            if regex.search(r'\p{IsCyrillic}', tag.name) is None:
                tag = Tag(guid=tag.guid, name=tag.name, parentGuid=tag_eng.guid)
                # print('new = eng')
            else:
                tag = Tag(guid=tag.guid, name=tag.name, parentGuid=tag_rus.guid)
                # print('new = rus')

            update_sequence_number = note_store.updateTag(token, tag)
            retrieved_tag = note_store.getTag(token, tag.guid)
            print(f'new = {retrieved_tag}')
            print()


def get_all_tags(client: EvernoteClient) -> List[Tag]:
    note_store = client.get_note_store()
    tags = note_store.listTags()
    return tags


def get_tag_by_name(tags_lst: List[Tag], tag_name: str):
    for tag in tags_lst:
        if tag.name == tag_name:
            return tag

    return None


if __name__ == '__main__':
    # Step: Init
    token = os.environ['EVERNOTE_PROD_DEV_TOKEN']
    client = new_client()

    # Step: Tags
    tags_lst = get_all_tags(client)
    tag_rus = get_tag_by_name(tags_lst, '#RUS')
    tag_eng = get_tag_by_name(tags_lst, '#ENG')

    # Step: Sort
    sort(client, tags_lst, tag_rus, tag_eng)
