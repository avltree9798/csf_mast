from modules.utils.constant import (
    ROOT_DIR,
    JADX_PATH
)
import os
import zipfile


def extract_ipa(filename: str, scan_id):
    output = f'/tmp/mast-output/{scan_id}/{filename}-output'
    try:
        with zipfile.ZipFile(f'{filename}') as z:
            z.extractall(output)
            z.close()
    except Exception as e:
        raise Exception(f"Error during extraction {e}")
    finally:
        return output


def extract_apk(filename: str, scan_id: str):
    output = f'/tmp/mast-output/{scan_id}/{filename}-output'
    os.makedirs(output)
    command = f"{jadx_path} -d {output} {CURR_DIR}/input/{file_name}"
    os.system(command)
    return output


PREPROCESSOR = {
    'ios': extract_ipa,
    'android': extract_apk
}
