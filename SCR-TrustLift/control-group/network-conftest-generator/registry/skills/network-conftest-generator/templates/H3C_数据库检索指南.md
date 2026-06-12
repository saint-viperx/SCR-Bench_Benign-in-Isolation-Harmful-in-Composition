# H3C设备知识库检索系统使用指南

## 1. 系统概述

H3C设备知识库检索系统是一个基于Elasticsearch的智能搜索系统，集成了6个专业领域的知识库，涵盖H3C网络设备的配置示例、测试用例、命令参考等内容。系统采用混合搜索技术（关键词+向量），提供高精度的智能检索服务。

### 1.1 技术架构
- **搜索引擎**: Elasticsearch 9200端口
- **搜索方式**: 混合搜索（关键词匹配 + 向量相似度）
- **向量模型**: embedding-3 (http://10.144.41.149:4000/v1/embeddings)
- **检索权重**: 关键词权重0.5 + 向量权重0.5

### 1.2 支持的数据库
系统共支持6个专业数据库，每个数据库针对特定的应用场景：

1. **v9_press_example** - V9文档配置示例
2. **background_ke**    - 测试背景知识库
3. **example_ke**       - 测试用例示例库
4. **testcenter_ke**    - 测试仪知识库
5. **cmd_ke**           - 命令配置知识库
6. **press_config_des** - 配置描述知识库

## 2. 数据库详细介绍

### 2.1 v9_press_example - V9文档配置示例

#### 数据库简介
存储H3C V9系列设备的完整配置示例文档，包含详细的组网需求、配置步骤和验证方法。

#### 数据结构
```json
{
    "content": "配置内容（包含组网需求、配置步骤、验证配置等详细说明）",
    "title_2": "二级标题（如'IP地址配置举例（交换应用）'）",
    "path": "文档路径（本地Markdown文件路径）"
}
```

#### 适用场景
- 网络设备配置参考
- 工程实施指导
- 配置问题排查

#### 检索建议
- **关键词**: 具体功能名称，如"IP地址配置"、"静态路由"、"VLAN"等
- **描述**: 配置需求描述，如"交换机多网段配置"、"路由器间静态路由"等
- **返回数量**: 默认5条结果

#### 示例检索
```bash
# 查询交换机配置相关内容
python {当前skill路径}/script/data_search_h3c_example.py --description "交换机多网段配置" --indexname "v9_press_example"

# 查询路由配置
python {当前skill路径}/script/data_search_h3c_example.py --description "静态路由配置" --indexname "v9_press_example"
```

#### 检索结果示例

**示例1：查询交换机配置**
```bash
python {当前skill路径}/script/data_search_h3c_example.py --description "交换机配置" --indexname "v9_press_example"
```

**返回结果：**
```json
[
    {
        "content": "#### 组网需求\nSwitch的端口（属于VLAN 1）连接一个局域网，局域网中的计算机分别属于2个网段：172.16.1.0/24和172.16.2.0/24。要求这两个网段的主机都可以通过Switch与外部网络通信，且这两个网段中的主机能够互通...\n#### 配置步骤\n针对上述的需求，如果在Switch的VLAN接口1上只配置一个IP地址，则只有一部分主机能够通过Switch与外部网络通信。为了使局域网内的所有主机都能够通过Switch访问外部网络，需要配置VLAN接口1的从IP地址...",
        "title_2": "IP地址配置举例（交换应用）",
        "path": "D:\\Documents\\press文档\\V9B88_MD\\08-三层技术-IP业务\\02-IP地址\\IP地址配置.md"
    },
    {
        "content": "#### 组网需求\n交换机各接口及主机的IP地址和掩码如图所示。要求采用静态路由，使图中任意两台主机之间都能互通。\n#### 配置步骤\n(1) 配置静态路由\n\\# 在Switch A上配置缺省路由。\n\\<SwitchA\\> system-view\n\\[SwitchA\\] ip route-static 0.0.0.0 0.0.0.0 1.1.4.2\n\\# 在Switch B上配置两条静态路由...",
        "title_2": "静态路由配置举例（交换应用）",
        "path": "D:\\Documents\\press文档\\V9B88_MD\\09-三层技术-IP路由\\02-静态路由\\静态路由配置.md"
    }
]
```

**示例2：查询WLAN配置**
```bash
python {当前skill路径}/script/data_search_h3c_example.py --description "无线网络配置" --indexname "v9_press_example"
```

**返回结果：**
```json
[
    {
        "content": "#### 组网需求\nAC和AP通过交换机连接，通过将客户端的MAC地址0000-000f-1211加入到白名单中，仅允许该客户端接入无线网络，拒绝其它客户端接入无线网络。\n#### 配置步骤\n\\# 将客户端的MAC地址0000-000f-1211添加到白名单。\n\\<AC\\> system-view\n\\[AC\\] wlan whitelist mac-address 0000-000f-1211\n#### 验证配置\n配置完成后，在AC上执行**display wlan whitelist**命令...",
        "title_2": "WLAN接入配置举例",
        "path": "D:\\Documents\\press文档\\V9B88_MD\\22-WLAN\\04-WLAN接入\\WLAN接入配置.md"
    }
]
```

#### 典型内容
- IP地址配置举例（交换应用）
- 静态路由配置举例（交换应用）
- BOOTP客户端配置举例（交换应用）
- WLAN接入配置举例

---

### 2.2 background_ke - 测试背景知识库

#### 数据库简介
存储自动化测试的背景配置信息，包含测试环境初始化、设备配置、拓扑映射等关键信息。

#### 数据结构
```json
{
    "title": "测试项目标题（如'SEC\\DPI\\DPI-1_1_0_3-AV业务测试'）",
    "conftest": "pytest框架的conftest.py内容（包含setup、teardown函数）",
    "resource_file": "资源文件集合（包含多个辅助Python文件）"
}
```

#### 适用场景
- 自动化测试框架搭建
- 测试环境初始化
- 设备连通性检查
- 测试资源管理

#### 检索建议
- **关键词**: 测试模块名称，如"DPI"、"安全策略"、"防火墙"等
- **描述**: 测试场景描述，如"病毒防护测试"、"入侵检测"等
- **返回数量**: 默认2条结果

#### 示例检索
```bash
# 查询DPI相关测试背景
python {当前skill路径}/script/data_search_h3c_example.py --description "DPI安全测试" --indexname "background_ke"

# 查询安全策略测试
python {当前skill路径}/script/data_search_h3c_example.py --description "防火墙策略测试" --indexname "background_ke"
```

#### 检索结果示例

**示例：查询测试背景配置**
```bash
python {当前skill路径}/script/data_search_h3c_example.py --description "测试背景" --indexname "background_ke"
```

**返回结果：**
```json
[
    {
        "title": "SEC\\DPI\\DPI-1_1_0_3-AV业务测试",
        "conftest": "from pytest import fixture\nfrom pytest_atf import *\nfrom pytest_atf.atf_globalvar import globalVar as gl\nimport time\nimport datetime\nimport inspect\nimport os\nimport pytest_check\nimport sys\nlevel = 3\ntopo = r'T_1_1_0_3.topox'\n...\n@atf_time_stats(\"ATFSetupTime\")\n@atf_adornment\ndef setup():\n    '''\n    脚本初始配置\n    '''\n\tcomconfig.Linuxconfig()\n    cmd = f\"\"\"\n        ctrl+z\n        system-view\n        anti-virus policy AVpolicy\n        qu\n\n        app-profile appProfile\n        anti-virus apply policy AVpolicy mode protect\n        qu\n\n        security-policy ip\n        rule 0 name sec_policy_ipv4_default\n        profile appProfile \n        qu\n\n        qu\n\n        inspect activate\n        customlog format dpi ips \n        customlog host {gl.GeneralServer.PORT1.ip} export  dpi ips \n        \"\"\"\n    gl.DUT.send(cmd,timeout=60)",
        "resource_file": "{'file_name': 'resource\\\\comconfig.py', 'resource_content': 'from pytest import fixture\\nfrom pytest_atf import *\\n...'}"
    }
]
```

#### 典型内容
- SEC\DPI\DPI-1_1_0_3-AV业务测试
- SEC\SECP\Security-Policy_4_12_0_1-SECP基础业务
- 测试环境配置脚本
- 设备连通性检查代码

---

### 2.3 example_ke - 测试用例示例库

#### 数据库简介
存储具体的测试用例实现代码，提供完整的测试函数、初始化和清理配置。

#### 数据结构
```json
{
    "file_name": "测试文件名（按功能模块分类）",
    "setup": "测试初始化配置（DUT设备配置）",
    "teardown": "测试清理配置",
    "fun_content": "测试函数内容"
}
```

#### 适用场景
- 测试用例开发参考
- 测试代码复用
- 测试脚本模板
- 功能测试实现

#### 检索建议
- **关键词**: 功能模块名称，如"DHCP"、"SSLVPN"、"接口测试"等
- **描述**: 测试功能描述，如"DHCP中继功能测试"、"VPN网关测试"等
- **返回数量**: 默认5条结果

#### 示例检索
```bash
# 查询DHCP相关测试用例
python {当前skill路径}/script/data_search_h3c_example.py --description "DHCP中继测试" --indexname "example_ke"

# 查询SSLVPN测试用例
python {当前skill路径}/script/data_search_h3c_example.py --description "SSLVPN网关登录测试" --indexname "example_ke"
```

#### 检索结果示例

**示例：查询测试用例**
```bash
python {当前skill路径}/script/data_search_h3c_example.py --description "测试示例" --indexname "example_ke"
```

**返回结果：**
```json
[
    {
        "file_name": "DHCP_Relay,DHCP_Relay_选项功能,test_dhcp_relay_30_1_7_14_T85_P30651_1_1_1.py",
        "setup": "def setup_class(cls):\n        '''\n        组网初始配置\n        '''\n        # 设置发包接口名称\n        dhcp.Set_ifname(gl.PC.PORT1.ip)\n        \n        gl.DUT1.send(f'''\n            ctrl+z\n            system-view\n            ip route-static 111.1.1.0 24 100.1.1.2\n            dhcp enable\n            ip pool a\n            network 111.1.1.0 24\n            forbidden-ip 111.1.1.1\n            interface {gl.DUT1.PORT1.intf}\n            undo ip address\n            undo ipv6 address\n            undo shutdown\n            ip address 100.1.1.1 24",
        "teardown": "def teardown_class(cls):\n        '''\n        清除脚本初始配置\n        '''\n        gl.DUT1.send(f'''\n            ctrl+z\n            undo debugging all\n            undo t m\n            undo t d\n            reset dhcp server ip-in-use\n            y\n            system-view\n            undo dhcp enable",
        "fun_content": "def test_step_2(self):\n        '''\n        用例描述\n        '''\n        pass"
    }
]
```

#### 典型内容
- DHCP_Relay,DHCP_Relay_选项功能,test_dhcp_relay_30_1_7_14_T85_P30651_1_1_1.py
- SSLVPN,SSLVPN_网关,resource,loginPage.py
- DHCP_Server,DHCP_Server_租约固化功能,test_dhcp_1_11_1_1.py

---

### 2.4 testcenter_ke - 测试中心知识库

#### 数据库简介
存储测试仪流量配置示例和网络拓扑信息，专门用于网络性能和功能测试的流量生成。

#### 数据结构
```json
{
    "file_name": "测试场景名称",
    "content": "测试脚本片段和组网说明"
}
```

#### 适用场景
- 测试仪配置参考
- 流量测试脚本开发
- 网络拓扑设计
- 性能测试实现

#### 检索建议
- **关键词**: 测试类型，如"组播"、"路由测试"、"流量生成"等
- **描述**: 测试场景描述，如"IPv4组播测试"、"路由匹配流量"等
- **返回数量**: 默认5条结果

#### 示例检索
```bash
# 查询组播测试相关内容
python {当前skill路径}/script/data_search_h3c_example.py --description "组播流量测试" --indexname "testcenter_ke"

# 查询路由测试
python {当前skill路径}/script/data_search_h3c_example.py --description "路由匹配数据流量" --indexname "testcenter_ke"
```

#### 检索结果示例

**示例：查询测试中心配置**
```bash
python {当前skill路径}/script/data_search_h3c_example.py --description "测试中心" --indexname "testcenter_ke"
```

**返回结果：**
```json
[
    {
        "file_name": "测试仪口打入IPV4组播数据报文",
        "content": "2.2.1 **脚本片段测试组网（设备+连接）**\n```\n设备组网连线模拟示意图：\n         topo为：SMB port1----DUT1--------DUT2----SMB port2\n\ndevices：\n    DUT1,SMB                                      #待测设备\nports：                                           #待测设备的接口\n    DUT1 [PORT1]\n    SMB [PORT1] \nlinks:                                            #设备间的接口连线\n    link1：DUT1.PORT1 to SMB.PORT1\n```  \n**2.2.2 脚本片段示例**\n```python\n        gl.SMB.PORT1.CreateUDPStream(Name='L6Z-PIS-PIS', \n        FrameLen =[128],  \t\t\t\t\t# IP数据流的帧长(不含CRC)\n        FrameRate=100, \t\t\t\t\t# 流的速率（pps）\n        TxMode='L3_CONTINUOUS_MODE', \n        DesMac='0100-5e10-1101', \t\t\t# 修改组播目的起始mac\n        SrcMac='1-1-1', \n        VlanID= 2083, \t\t\t\t\t\t# 流量入接口对应的vlan ID\n        DesIP='239.16.17.1', \t\t\t\t# 修改组播目的起始 IP\n        SrcIP='10.148.24.23', \t\t\t\t# 修改组播源IP，与网关同一网段"
    }
]
```

#### 典型内容
- 测试仪口打入IPV4组播数据报文
- 模拟匹配路由数据的流量
- 检查测试仪口IPV6组播流量收包速率
- 检查测试仪口接收的IPV4组播数据报文流量速率

---

### 2.5 cmd_ke - 命令配置知识库

#### 数据库简介
存储H3C设备的命令行配置参考，包含完整的命令语法、参数说明和使用指导。

#### 数据结构
```json
{
    "title_2": "命令分类标题（如'下发目标配置命令'）",
    "cmd": "具体命令名称（如'commit'）",
    "content": "命令详细说明（语法、参数、示例等）"
}
```

#### 适用场景
- 命令行配置参考
- 设备操作指导
- 命令语法查询
- 运维工作支持

#### 检索建议
- **关键词**: 具体命令名称，如"commit"、"display"、"interface"等
- **描述**: 配置需求描述，如"保存配置"、"查看配置"、"安全策略"等
- **返回数量**: 默认5条结果

#### 示例检索
```bash
# 查询配置提交命令
python {当前skill路径}/script/data_search_h3c_example.py --description "提交配置命令" --indexname "cmd_ke"

# 查询显示配置命令
python {当前skill路径}/script/data_search_h3c_example.py --description "查看当前配置" --indexname "cmd_ke"
```

#### 检索结果示例

**示例：查询命令配置**
```bash
python {当前skill路径}/script/data_search_h3c_example.py --description "命令配置" --indexname "cmd_ke"
```

**返回结果：**
```json
[
    {
        "title_2": "下发目标配置命令",
        "cmd": "commit",
        "content": "**commit**命令用来下发目标配置。\n【命令】\n**commit** \\[ **best-effort** \\] \\[ **force** \\] \\[ **label**\n*labelname* \\] \\[ **save-running** *filename* \\] \\[ **confirmed** \\[\n*seconds* \\| **minutes** *minutes* \\] \\] \\[ **show-error** \\] \\[\n**clear-error** \\] \\[ **description** *text* \\]\n【视图】\n私有模式下的任意视图\n独占模式下的任意视图\n【缺省用户角色】\nnetwork-admin\nnetwork-operator\nmdc-admin\nmdc-operator\n【参数】\n**best-effort**：表示目标配置中包含错误命令行时，设备将忽略错误命令行下发目标配置。如果不指定该参数，目标配置中包含错误命令行时，目标配置下发操作失败，系统继续使用下发目标配置操作以前的配置运行。\n**force**：下发目标配置时不检查内存。如果不指定该参数，设备下发目标配置前，首先查看内存状态是否处于正常状态，若内存异常则目标配置下发操作失败，系统继续使用下发目标配置操作以前的配置运行。"
    }
]
```

#### 典型内容
- commit: 下发目标配置命令
- display this: 显示当前视图下生效的配置
- display current-configuration: 显示设备生效的配置
- action: 配置安全策略规则动作

---

### 2.6 press_config_des - 配置描述知识库

#### 数据库简介
存储标准化的配置步骤说明，提供详细的配置流程和参数说明。

#### 数据结构
```json
{
    "title": "配置功能标题（如'时间段/配置时间段'）",
    "content": "详细配置步骤说明"
}
```

#### 适用场景
- 标准化配置流程
- 配置步骤参考
- 功能配置指导
- 参数配置说明

#### 检索建议
- **关键词**: 配置功能名称，如"时间段"、"预配置"、"应用组"等
- **描述**: 配置需求描述，如"时间控制"、"模块预配置"、"应用识别"等
- **返回数量**: 默认5条结果

#### 示例检索
```bash
# 查询时间段配置
python {当前skill路径}/script/data_search_h3c_example.py --description "时间段配置" --indexname "press_config_des"

# 查询预配置功能
python {当前skill路径}/script/data_search_h3c_example.py --description "模块预配置" --indexname "press_config_des"
```

#### 检索结果示例

**示例：查询配置描述**
```bash
python {当前skill路径}/script/data_search_h3c_example.py --description "配置描述" --indexname "press_config_des"
```

**返回结果：**
```json
[
    {
        "title": "时间段/配置时间段",
        "content": "(1) 进入系统视图。\n**system-view**\n(2) 创建时间段。\n**time-range** *time-range-name* { { **monthly** \\| **weekly** }\n*start-day* *start-time* **to** *end-day end-time* \\[ **from** *time1\ndate1* \\] \\[ **to** *time2 date2* \\] \\| *start-time* **to** *end-time*\n*days* \\[ **from** *time1 date1* \\] \\[ **to** *time2 date2* \\] \\|\n**from** *time1 date1* \\[ **to** *time2 date2* \\] \\| **to** *time2\ndate2* }\n如果指定的时间段已经创建，则本命令可以修改时间段的时间范围。\n(3) （可选）配置时间段的描述信息。\n**time-range** *time-range-name* **description** *text*\n缺省情况下，时间段未配置描述信息。"
    }
]
```

#### 典型内容
- 时间段/配置时间段
- 预配置/开启预配置功能
- APR配置/配置应用组
- APR配置/配置PBAR
- 设备基本配置/配置系统时间/配置时区

## 3. 使用方法

### 3.1 基本语法
```bash
python {当前skill路径}/script/data_search_h3c_example.py --description "检索描述" --indexname "数据库名称"
```

### 3.2 参数说明
- `--description`: 必选参数，检索的关键词或需求描述
- `--indexname`: 必选参数，目标数据库名称

### 3.3 支持的数据库名称
- `v9_press_example`: V9文档配置示例
- `background_ke`: 测试背景知识库
- `example_ke`: 测试用例示例库
- `testcenter_ke`: 测试中心知识库
- `cmd_ke`: 命令配置知识库
- `press_config_des`: 配置描述知识库

### 3.4 返回结果格式
每个数据库返回的结果都是JSON格式的列表，包含该数据库特定的字段结构。

## 4. 检索策略建议

### 4.1 数据库选择指南

| 需求类型 | 推荐数据库 | 检索关键词示例 |
|---------|-----------|---------------|
| 配置示例参考 | v9_press_example | "IP配置"、"路由配置"、"VLAN配置" |
| 测试环境搭建 | background_ke | "DPI测试"、"安全测试"、"连通性检查" |
| 测试代码开发 | example_ke | "DHCP测试"、"VPN测试"、"功能测试" |
| 流量测试配置 | testcenter_ke | "组播测试"、"流量生成"、"路由测试" |
| 命令行参考 | cmd_ke | "commit命令"、"display命令"、"配置命令" |
| 配置流程指导 | press_config_des | "时间段配置"、"预配置"、"应用组配置" |


## 7. 常见检索场景示例


**场景**: 需要配置交换机实现多网段互通
```bash
python {当前skill路径}/script/data_search_h3c_example.py --description "交换机多网段配置" --indexname "v9_press_example"
```

**场景**: 需要配置防火墙安全策略
```bash
python {当前skill路径}/script/data_search_h3c_example.py --description "安全策略配置" --indexname "cmd_ke"
```


**场景**: 需要搭建DPI功能测试环境
```bash
python {当前skill路径}/script/data_search_h3c_example.py --description "DPI安全测试" --indexname "background_ke"
```

**场景**: 需要编写DHCP中继测试用例
```bash
python {当前skill路径}/script/data_search_h3c_example.py --description "DHCP中继测试" --indexname "example_ke"
```

**场景**: 需要查看设备当前配置
```bash
python {当前skill路径}/script/data_search_h3c_example.py --description "查看当前配置" --indexname "cmd_ke"
```

**场景**: 需要配置时间段策略
```bash
python {当前skill路径}/script/data_search_h3c_example.py --description "时间段配置" --indexname "press_config_des"
```