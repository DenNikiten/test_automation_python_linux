from checkers import checkout
from checkers import checkout_negative
import yaml

with open('config.yaml') as f:
    data = yaml.safe_load(f)

FOLDER_TST = data['FOLDER_TST']
FOLDER_OUT = data['FOLDER_OUT']
FOLDER_1 = data['FOLDER_OUT']
FOLDER_2 = data['FOLDER_OUT']
ARC_TYPE = data['ARC_TYPE']


class TestPositive:

    def test_step1(self, make_folders, clear_folders, make_files):
        result1 = checkout(f"cd {FOLDER_TST}; 7z a -t{ARC_TYPE} {FOLDER_OUT}/arx2",
                           "Everything is Ok")
        result2 = checkout(f"cd {FOLDER_OUT}; ls", f"arx2.{ARC_TYPE}")
        assert result1 and result2, "test1 FAIL"

    def test_step2(self, clear_folders, make_files):
        result1 = checkout(f"cd {FOLDER_TST}; 7z a -t{ARC_TYPE} {FOLDER_OUT}/arx2",
                           "Everything is Ok")
        result2 = checkout(f"cd {FOLDER_OUT}; 7z e arx2.{ARC_TYPE} -o{FOLDER_1} -y",
                           "Everything is Ok")
        result3 = checkout(f"cd {FOLDER_1}; ls", make_files[0])
        assert result1 and result2 and result3, "test2 FAIL"

    def test_step3(self, clear_folders, make_files):
        result2 = checkout(f"cd {FOLDER_TST}; 7z a -t{ARC_TYPE} {FOLDER_OUT}/arx2",
                           "Everything is Ok")
        result1 = checkout(f"cd {FOLDER_OUT}; 7z x arx2.{ARC_TYPE} -o{FOLDER_2}",
                           "Everything is Ok")
        assert result1 and result2, "test3 FAIL"

    def test_step4(self, clear_folders, make_files):
        result1 = checkout(f"cd {FOLDER_TST}; 7z a -t{ARC_TYPE} {FOLDER_OUT}/arx2",
                           "Everything is Ok")
        result2 = checkout(f"cd {FOLDER_OUT}; 7z l arx2.{ARC_TYPE}", make_files[0])
        assert result1 and result2, "test4 FAIL"

    def test_step5(self, clear_folders, make_files):
        result2 = checkout(f"cd {FOLDER_TST}; 7z a -t{ARC_TYPE} {FOLDER_OUT}/arx2",
                           "Everything is Ok")
        result1 = checkout(f"cd {FOLDER_OUT}; 7z t arx2.{ARC_TYPE}",
                           "Everything is Ok")
        assert result1 and result2, "test5 FAIL"

    def test_step6(self):
        assert checkout(f"cd {FOLDER_TST}; 7z u {FOLDER_OUT}/arx2.{ARC_TYPE}",
                        "Everything is Ok"), "test6 FAIL"

    def test_step7(self, make_files, make_sub_folder):
        result2 = checkout(f"cd {FOLDER_TST}; 7z a -t{ARC_TYPE} {FOLDER_OUT}/arx2",
                           "Everything is Ok")
        result1 = checkout(f"cd {FOLDER_OUT}; 7z d arx2.{ARC_TYPE}",
                           "Everything is Ok")
        assert result1 and result2, "test7 FAIL"


class TestNegative:

    def test_step1(self, make_files, make_folders, clear_folders, make_bad_arx):
        result1 = checkout_negative(f"cd {FOLDER_OUT};"
                                    f" 7z e bad_arx.{ARC_TYPE} -o{FOLDER_1} -y", "ERRORS")
        assert result1, "test1 FAIL"

    def test_step2(self, make_folders, clear_folders, make_files, make_bad_arx):
        assert checkout_negative(f"cd {FOLDER_OUT}; 7z t bad_arx.{ARC_TYPE} ", "ERRORS"), \
            "test2 FAIL"
