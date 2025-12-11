import uuid

def gen_run_id():
    return str(uuid.uuid4())[:8]
