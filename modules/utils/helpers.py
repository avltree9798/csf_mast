from plistlib import load as load_plist


def plist_parse(file: str) -> {}:
    plist = {}
    with open(file, 'rb') as fp:
        plist = load_plist(fp)
        fp.close()
    return plist
