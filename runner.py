# -*- coding: utf-8 -*-
from framework.core.lib.ConfigManager import ConfigManager
from subprocess import Popen, PIPE
import os, sys, getopt
import pytest

def get_testlist(filename):
    test_dir = "framework/testcases/tests/"
    cfg = ConfigManager()
    data = cfg.config_load(filename=filename)
    data = data["tests"].values()
    for item in range(len(data)):
        data[item] = test_dir + data[item]
    return data

def generate_report(xmldir, reportdir, alluredir, _open):
    cur_dir = os.getcwd()
    allure_path = os.path.join(cur_dir, alluredir, "bin\\allure")
    xmldir = os.path.join(cur_dir, xmldir)
    reportdir = os.path.join(cur_dir, reportdir)
    cmd = "%s generate %s -o %s" % (allure_path, xmldir, reportdir)
    proc = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    proc.wait()    # дождаться выполнения
    res = proc.communicate()  # получить tuple('stdout res', 'stderr res')
    if proc.returncode:
        print res[1]
    print 'result:', res[0]
    if _open:
        cmd = "%s report open  --report-path %s" % (allure_path, reportdir)
        proc = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        proc.wait()    # дождаться выполнения
        res = proc.communicate()  # получить tuple('stdout res', 'stderr res')
        if proc.returncode:
            print res[1]
        print 'result:', res[0]


def main(argv):
    _xmldir    = "env/output"
    _reportdir = "report"
    _alluredir = "env/allure"
    _filecfg = "framework/testcases/config/test.yaml"
    _open = None

    try:
        opts, args = getopt.getopt(argv, "hf:d:r:a:o:", ["help", "filecfg", "xmldir=", "reportdir=", "alluredir=", "open="])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt in("-h", "--help"):
            usage()
            sys.exit()
        elif opt in("-d", "--xmldir"):
            _xmldir = arg
        elif opt in("-f", "--filecfg"):
            _xmldir = arg
        elif opt in("-r", "--reportdir"):
            _reportdir = arg
        elif opt in("-a", "--alluredir"):
            _alluredir = arg
        elif opt in("-o", "--open"):
            _open = arg
    params = get_testlist(filename=_filecfg)
    params.append("--alluredir=%s/" % _alluredir)
    pytest.main(args=params)
    generate_report(xmldir=_xmldir, reportdir=_reportdir, alluredir=_alluredir, _open=_open)

def usage():
    print u"""
             -f path , --filecfg path, где path путь к *.yaml файлу с тестами
              По умолчанию --filecfg="testcases/config/test.yaml""/\n
             -d path, --xmldir path, где path путь к директории с xml файлами  По умолчанию --xmldir=env/output/\n
             -r path,  --reportdir path, где path путь к директории куда будет сгенерирован отчёт.
              По умолчанию reportdir=report\n
             -a path, --alluredir path, где path путь к папке allure-cli. По умолчанию alluredir = env/allure/
             -h, --help  выводит справку об использовании приложения\n
          """

if __name__ == '__main__':
    main(sys.argv[1:])

