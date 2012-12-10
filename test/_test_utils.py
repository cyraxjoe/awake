import tempfile

def create_sample_file(*lines):
    _, path = tempfile.mkstemp('.awaketest')
    try:
        file_ = open(path, 'w')
        for line in lines:
            file_.write('%s\n' % line)
    finally:
        file_.close()
    return path
