def commit_callback(commit):
    if commit.original_id == b"68d5ba7848555f7ac143eb57abfb1147b443f95a":
        commit.skip()
