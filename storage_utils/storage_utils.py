"""Various utils for making file-based data management easier."""

import os


def get_user_ids(storage_path):
    """Returns user ids in the path"""
    existing_ids = os.listdir(storage_path)
    integer_ids = []
    if existing_ids:
        for i in existing_ids:
            try:
                current_id = int(i)
                integer_ids.append(current_id)
            except ValueError:
                pass
        return integer_ids
    return None


def get_next_id(storage_path):
    """Calculate the next available identifier."""
    integer_ids = get_user_ids(storage_path)
    if integer_ids:
        last_id = max(integer_ids)
        return last_id + 1
    return 0


def get_doc_ids(storage_path):
    """Returns document ids in the path"""
    return get_user_ids(storage_path)


def get_proj_ids(storage_path):
    """Returns project ids in the path"""
    return get_user_ids(storage_path)