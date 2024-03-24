import pytest
from checkers import checkout, getout
import random, string
import yaml
from datetime import datetime

with open('config.yaml') as f:
    data = yaml.safe_load(f)

FOLDER_TST = data['FOLDER_TST']
FOLDER_OUT = data['FOLDER_OUT']
FOLDER_1 = data['FOLDER_OUT']
FOLDER_2 = data['FOLDER_OUT']
ARC_TYPE = data['ARC_TYPE']
COUNT = data['COUNT']
BS = data['BS']


@pytest.fixture()
def make_folders():
    return checkout(
        f"mkdir -p {FOLDER_TST} {FOLDER_OUT} {FOLDER_1} {FOLDER_1}",
        "")


@pytest.fixture()
def make_files():
    list_of_files = []
    for i in range(COUNT):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout(f"cd {FOLDER_TST}; "
                    f"dd if=/dev/urandom of={filename} bs={BS} count=1 iflag=fullblock", ''):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def clear_folders():
    return checkout(
        f"rm -rf {FOLDER_TST}/* {FOLDER_OUT}/* {FOLDER_1}/* {FOLDER_2}/*",
        "")


@pytest.fixture()
def make_sub_folder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not checkout(f"cd {FOLDER_TST}; mkdir {subfoldername} ", ''):
        return None, None
    if not checkout(f"cd {FOLDER_TST}/{subfoldername};"
                    f" dd if=/dev/urandom of={testfilename} bs={BS} count=1 iflag=fullblock", ''):
        return subfoldername, None
    return subfoldername, testfilename


@pytest.fixture()
def make_bad_arx():
    checkout(f"cd {FOLDER_TST}; 7z a -t{ARC_TYPE}{FOLDER_OUT}/bad_arx",
             "Everything is Ok")
    checkout(f"truncate -s 1 {FOLDER_OUT}/bad_arx.{ARC_TYPE}", "")


@pytest.fixture(autouse=True)
def print_time():
    print(f'Start: {datetime.now().strftime("%H:%M:%s.%f")}')
    yield
    print(f'\nFinish: {datetime.now().strftime("%H:%M:%s.%f")}')


@pytest.fixture(autouse=True)
def stat_log():
    yield
    time = datetime.now().strftime("%H:%M:%s.%f")
    stat = getout('cat /proc/loadavg')
    checkout(f"echo 'time:{time} count:{COUNT} size;{BS} stat:{stat}' >> stat.txt", '')
