import subprocess


def check_out(path_file, file_text):
    res = subprocess.run(path_file, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    out = res.stdout
    if not res.returncode:
        if file_text in out:
            return True
    return False


print(check_out("cat /etc/os-release", 'VERSION_ID="22.04"'))
