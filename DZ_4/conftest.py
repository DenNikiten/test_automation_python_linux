import pytest
from sshcheckers import ssh_checkout, ssh_checkout_negative
import random, string
import yaml
from datetime import datetime
from checkers import checkout, getout


with open('config.yaml') as f:
   data = yaml.safe_load(f)



@pytest.fixture()
def make_folders():
   return ssh_checkout(data["ip"], data["user"], data["passwd"], "mkdir {} {} {} {}".format(data["folder_in"], data["folder_out"], data["folder_ext"], data["folder_ext2"]), "")


@pytest.fixture()
def clear_folders():
   return ssh_checkout(data["ip"], data["user"], data["passwd"], "rm -rf {}/* {}/* {}/* {}/*".format(data["folder_in"], data["folder_out"], data["folder_ext"], data["folder_ext2"]), "")


@pytest.fixture()
def make_files():
   list_of_files = []
   for i in range(data["count"]):
       filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
       if ssh_checkout(data["ip"], data["user"], data["passwd"], "cd {}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["folder_in"], filename), ""):
           list_of_files.append(filename)
   return list_of_files


@pytest.fixture()
def make_subfolder():
   testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
   subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
   if not ssh_checkout(data["ip"], data["user"], data["passwd"], "cd {}; mkdir {}".format(data["folder_in"], subfoldername), ""):
       return None, None
   if not ssh_checkout(data["ip"], data["user"], data["passwd"], "cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["folder_in"],
                                                                                             subfoldername,
                                                                                         testfilename), ""):
       return subfoldername, None
   else:
       return subfoldername, testfilename


@pytest.fixture()
def make_bad_arx():
   ssh_checkout(data["ip"], data["user"], data["passwd"], "cd {}; 7z a {}/arxbad -t{}".format(data["folder_in"],
                                                                               data["folder_out"], data["type"]), "Everything is Ok")
   ssh_checkout(data["ip"], data["user"], data["passwd"], "truncate -s 1 {}/arxbad.{}".format(data["folder_out"],
                                                                               data["type"]), "Everything is Ok")
   yield "arxbad"
   ssh_checkout(data["ip"], data["user"], data["passwd"], "rm -f {}/arxbad.{}".format(data["folder_out"], data["type"]), "")


@pytest.fixture(autouse=True)
def print_time():
   print("Start: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
   yield print("Stop: {}".format(datetime.now().strftime("%H:%M:%S.%f")))


@pytest.fixture()
def start_time():
   return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# @pytest.fixture(autouse=True)
# def stat_log():
#     yield
#     time = datetime.now().strftime("%H:%M:%s.%f")
#     stat = getout('cat /proc/loadavg')
#     checkout(f"echo 'time:{time} count:{COUNT} size;{BS} stat:{stat}' >> stat.txt", '')

# @pytest.fixture(autouse=True)
# def stat_log():
#     yield
#     time = datetime.now().strftime("%H:%M:%s.%f")
#     stat = ssh_checkout_negative(f"{data['ip']}",
#                             f"{data['user']}",
#                             f"{data['password']}",
#                             'cat /proc/loadavg')
#     ssh_checkout(f"{data['ip']}",
#                  f"{data['user']}",
#                  f"{data['password']}",
#                  f"echo 'time:{time} count:{data['count']} size;{data['bs']} stat:{stat}' >> stat.txt",
#                  '')