def fromFile(path):
    extraction = []
    for line in parse(path):
        extraction.append((float(line[0]), float(line[1])))
    return extraction

def parse(path):
    ret = []
    f = open(path, 'r')
    for line in f.read().split('\n'):
        ret.append(line.split(' '))
    del ret[-1]
    return ret
