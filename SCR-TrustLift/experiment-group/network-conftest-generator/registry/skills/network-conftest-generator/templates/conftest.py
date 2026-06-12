from pytest import fixture
from pytest_atf import *
from pytest_atf.atf_globalvar import globalVar as gl

# --------用户修改区 -------------------

# 执行层及使用拓扑文件名称
level = 3
topo = r'demo.topox'

# 用于声明脚本共用的变量或方法，不能修改类名。
# 变量或方法都要定义为类属性，不要定义为实例属性。
class CVarsAndFuncs:
    pass

# 不能删除setup/teardown的装饰器
@atf_time_stats("ATFSetupTime")
@atf_adornment
def setup():
    pass

@atf_time_stats("ATFTeardownTime")
@atf_adornment
def teardown():
    pass

# ---------END-----------

@fixture(scope="package", autouse=True)
def my_fixture_setup_and_teardown():
    atf_topo_map(topo, level)
    try:
        setup()
        yield
    finally:
        teardown()
        atf_topo_unmap()


@fixture(scope="package")
def VarsAndFuncs():
    return CVarsAndFuncs