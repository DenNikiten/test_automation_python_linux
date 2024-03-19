import subprocess

folder_in = "/home/dan/tst"
folder_out = "/home/dan/out"
folder_ext = "/home/dan/folder1"
folder_ext2 = "/home/dan/folder2"


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    print(result.stdout)
    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False


def test_step1():
    result1 = checkout("cd {}; 7z l arx2.7z".format(folder_out), "one")
    result2 = checkout("cd {}; 7z l arx2.7z".format(folder_out), "two")
    assert result1 and result2, "test1 FAIL"


def test_step2():
    result1 = checkout("cd {}; 7z x arx2.7z -o{} -y".format(folder_out, folder_ext2), "Everything is Ok")
    result2 = checkout("ls {}".format(folder_ext2), "two")
    result3 = checkout("ls {}".format(folder_ext2), "three")
    assert result1 and result2 and result3, "test2 FAIL"