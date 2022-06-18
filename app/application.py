import uuid
import re

def generate_key():
    return uuid.uuid4()

def is_key(candidate):
    match = re.match('@leo@.{8}-.{4}-.{4}-.{4}-.{12}', candidate)
    return bool(match)

def match_key(candidate):
    match = re.match('@leo@.{8}-.{4}-.{4}-.{4}-.{12}', candidate)
    return match.string if match else None