# name: 顺丰速运
# Author: sicxs
# Date: 2024-11-25
# export sfsy=""
# 换行分割 
# 功能:签到，浏览任务,蜂蜜,会员日
# cron: 20 8 * * *
# new Env('顺丰速运');

import json
import hashlib
import requests,random
import time,re,os,sys
import config
s = requests.session()

def test_getSign(): # headers + 浏览任务sign
        timestamp = str(int(round(time.time() * 1000)))
        data_str = f'token=wwesldfs29aniversaryvdld29&timestamp={timestamp}&sysCode=MCS-MIMP-CORE'
        correct_signature = hashlib.md5(data_str.encode()).hexdigest()
        headers = {
            'Host': 'mcs-mimp-web.sf-express.com',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090551) XWEB/6945 Flue',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'zh-CN,zh',
            'platform': 'MINI_PROGRAM',
            'sysCode': 'MCS-MIMP-CORE',            
            'timestamp': timestamp,
            'signature': correct_signature
        }
        return headers
def test_header():#蜂蜜 heaaders + sign
        timestamp = str(int(round(time.time() * 1000)))
        data_str = f'token=wwesldfs29aniversaryvdld29&timestamp={timestamp}&sysCode=MCS-MIMP-CORE'
        correct_signature = hashlib.md5(data_str.encode()).hexdigest()
        headers = {
            'Host': 'mcs-mimp-web.sf-express.com',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090551) XWEB/6945 Flue',
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json;charset=UTF-8',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'zh-CN,zh',
            'platform': 'MINI_PROGRAM',
            'channel': 'wxwdsj',
            'sysCode': 'MCS-MIMP-CORE',
            'timestamp': timestamp,
            'signature': correct_signature
        }
        
        return headers
def get_deviceId(characters='abcdef0123456789'):# 随机设备
        result = ''
        for char in 'xxxxxxxx-xxxx-xxxx':
            if char == 'x':
                result += random.choice(characters)
            elif char == 'X':
                result += random.choice(characters).upper()
            else:
                result += char
        return result
def random_pause():#随机时间 
    pause_time = random.uniform(20, 25)
    time.sleep(pause_time)
def sf_a():#积分
    url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~integralTaskStrategyService~queryPointTaskAndSignFromES"
    header = test_getSign()
    data = {
            'channelType': '3',
            'deviceId': get_deviceId(),
        }
    response = s.post(url, headers=header,json=data)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    return info['obj']['totalPoint']
def sf_a_a():#积分浏览任务列表
    url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~integralTaskStrategyService~queryPointTaskAndSignFromES"
    header = test_getSign()
    data = {
            'channelType': '1',
            'deviceId': get_deviceId(),
        }
    response = s.post(url, headers=header,json=data)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    return info['obj']['taskTitleLevels']
      
def sf_b():#做任务浏览任务
    # https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberEs~taskRecord~finishTask
    url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonRoutePost/memberEs/taskRecord/finishTask"
    header = test_getSign()
    #浏览任务
    print("开始积分浏览任务")
    taskcode = sf_a_a()
    for code in taskcode:
     data =  {
     "taskCode": code['taskCode']
        }
     response = s.post(url, headers=header,json=data)
     response.encoding = "utf-8"
     strategyId = code['strategyId']
     title = code['title']
     taskId =code['taskId']
     taskCode = code['taskCode']
     awardIntegral = code['awardIntegral']
     status = code['status']
     skip_title = ['用行业模板寄件下单', '去新增一个收件偏好', '参与积分活动','用积分兑任意礼品','领任意生活特权福利','设置你的顺丰ID',]
     if status == 3:
            print(f'{title}-已完成')
            continue
     if title in skip_title:
            print(f'{title}-跳过')
            continue
     info = json.loads(response.text)
     if info['success']:
         print(f"开始{code['title']}任务")
         random_pause()
         sf_b_a(strategyId,title,taskId,taskCode,awardIntegral)
     else:
        print("任务失败")       
def sf_b_a(strategyId,title,taskId,taskCode,awardIntegral):#做任务浏览任务领取奖励
    url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~integralTaskStrategyService~fetchIntegral'
    header = test_getSign()    
    data = {
        "strategyId": strategyId,
        "taskId": taskId,
        "taskCode": taskCode,
        "deviceId": get_deviceId()
        }
    time.sleep(3)
    response = s.post(url,headers=header,json=data)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if info['success']:
        print(f'{title}任务奖励领取成功,奖励:{awardIntegral}积分')
    else:
        print(f'{title}任务失败')
def sf_c():#签到
    url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~integralTaskSignPlusService~automaticSignFetchPackage'
    header = test_getSign()
    data = {"comeFrom": "vioin", "channelFrom": "WEIXIN"}
    response = s.post(url, headers=header,json=data)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if info['success']:
     if "integralTaskSignPackageVOList" in response.text:
        jf =  info["obj"]["integralTaskSignPackageVOList"][0]["packetName"]
        print(f"签到成功，获得{jf}积分")
     else:
        print("您今天已经签到过了")
    else:
        print("签到失败")
def sf_d():#领取惊喜权益 
     url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberManage~memberEquity~commonEquityReceive"
     header = test_getSign()
     data = {"key": "surprise_benefit"}
     response = s.post(url, headers=header,json=data)
     response.encoding = "utf-8"
     info = json.loads(response.text)
     if info['success']:
         print("惊喜权益礼包：领取成功")
     else:
        print("惊喜权益礼包：领取失败")
def sf_hyr_a():#会员日抽奖
    url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~memberDayLotteryService~lottery"
    header = test_getSign()
    data = {}
    response = s.post(url, headers=header,json=data)
    time.sleep(3)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if info['success']:
      cj = info["obj"]["productName"]
      print(f"会员日抽奖成功,获得{cj}")
    else:
      print("会员日抽奖失败")
def sf_hyr_b():#会员日领取合成红包 
    url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~memberDayTaskService~receiveRedPacket"
    header = test_getSign()
    current_time = time.localtime()
    hour = current_time.tm_hour
    if 9 <= hour < 10:
        data = {"receiveHour":9}
        response = s.post(url, headers=header,json=data)
        response.encoding = "utf-8"
        info = json.loads(response.text)
        if info['success']:
         print("领取成功")
        else:
         print("领取失败")
    if 12 <= hour < 13:
        data = {"receiveHour":12}
        response = s.post(url, headers=header,json=data)
        response.encoding = "utf-8"
        info = json.loads(response.text)
        if info['success']:
         print("领取成功")
        else:
         print("领取失败") 
    if 15 <= hour < 16:
        data = {"receiveHour":15}
        response = s.post(url, headers=header,json=data)
        response.encoding = "utf-8"
        info = json.loads(response.text)
        if info['success']:
         print("领取成功")
        else:
         print("领取失败") 
    if 18 <= hour < 19:
        data = {"receiveHour":18}
        response = s.post(url, headers=header,json=data)
        response.encoding = "utf-8"
        info = json.loads(response.text)
        if info['success']:
         print("领取成功")
        else:
         print("领取失败")  
def sf_hyr_c():#会员日查看合成红包列表    
   url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~memberDayPacketService~redPacketStatus"
   header = test_getSign()
   data= ""
   response = s.post(url,headers=header,json=data)
   response.encoding = "utf-8"
   info = json.loads(response.text)    
   if info['success']:
       lv = info["obj"]["packetList"]
       for llv in lv:
           s1 = llv["count"]
           s2 = llv["level"]
           print(f"等级{llv['level']}，红包数量{llv['count']}")
           if s1 == 2 or s1 % 2 == 0:
             sf_hyr_d(s2)  
   else:
       print("您还未有红包")
def sf_hyr_d(lv):#会员日合成红包
    url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~memberDayPacketService~redPacketMerge"
    header = test_getSign()
    data = {
        "level": lv,
        "num": 2
        }
    response = s.post(url, headers=header,json=data)
    random_pause()
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if info['success']:
     print("检测到有同样的红包，执行合成")
    else:
     print("合成失败")
def sf_hyr_e():#会员日浏览任务
   url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberEs~taskRecord~finishTask"
   header = test_getSign()  
   taskcode = [
   "549A0E63C3534EEA9214835D260C8416",
   "1E0C04B2965D4A478595D284D35D396C"
   ]
   for code in taskcode:
    data = {"taskCode": code}   
    response = s.post(url, headers=header,json=data)
    response.encoding = "utf-8"
    random_pause()
    info = json.loads(response.text)
    if info['success']:
     print("任务完成")
    else:
     print("任务失败")
def sf_hyr_f():#会员日领取浏览任务
   url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~activityTaskService~fetchMixTaskReward"
   header = test_getSign()
   taskType = [
      "BROWSE_INTEGRAL_PLANET",
      "BROWSE_VIP_CENTER"
   ]
   for i in taskType:
     data = {
        "taskType": i,
        "activityCode": "MEMBER_DAY",
        "channelType": "MINI_PROGRAM"
        }
     response = requests.post(url=url,json=data,headers=header)
     response.encoding = "utf-8"
     random_pause()
     info = json.loads(response.text)
     if info['success']:
        print("领取成功")
     else:
        print("领取失败")   

def sf_fm_a(): #蜂蜜大冒险
    gameNum = 5
    header = test_header()
    for i in range(1,gameNum):
     data = {"gatherHoney":20}
     if gameNum < 0: break
     print(f'开始第{i}次大冒险')
     url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~receiveExchangeGameService~gameReport'
     response =s.post(url, headers=header,json=data)
     time.sleep(random.uniform(5, 10))
     response.encoding = "utf-8"
     info = json.loads(response.text)
     if info['success']:
        gameNum = info['obj']['gameNum']
        print(f'大冒险成功，剩余次数{gameNum}')
        gameNum -= 1
     elif info["errorMessage"] == '容量不足':
        print(f'需要扩容')
        sf_fm_b()
     else:
        print(f'大冒险失败！【{info["errorMessage"]}】')
        break
def sf_fm_b(): #蜂蜜大冒险扩容
   header = test_header()
   url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~receiveExchangeIndexService~expand'
   data = ""
   response = s.post(url, data=data, headers=header)
   response.encoding = "utf-8"
   info = json.loads(response.text)
   if info['success']: 
    print(f'成功扩容{info["obj"]}容量')
   else: 
    print(f'扩容失败') 
def sf_fm_e1(): #暂留
     header = test_header()
     url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~receiveExchangeGameService~gameStatus"
     data = {}
     response = s.post(url, headers=header, json=data)
     response.encoding = "utf-8"
     info = json.loads(response.text)
     print(info)
def sf_fm_f(): # 蜂蜜任务列表
    header = test_header()
    url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~receiveExchangeIndexService~taskDetail"
    data = {}
    response = s.post(url, headers=header, json=data)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    sf = []
    if info['success']:
        sf_list = info['obj']['list']
        for task in sf_list:
            task_type = task.get('taskType', '')
            status = task.get('status', '')
            task_code = task.get('taskCode', '')
            jumpTo = task.get('jumpTo', '')
            if task_type == 'BROWSER_CENTER_TASK_TYPE' and status == 1:
              sf.append({
                    'task_type': task_type,
                    'status': status,
                    'task_code': task_code,
                    'jumpTo': jumpTo
                })
        return sf
    else:
        print("获取失败")
        return None
def sf_fm_c(): #蜂蜜浏览任务
   header = test_getSign()
   s1 = sf_fm_f()
   for code in s1:
      url = code['jumpTo']
      response = s.get(url, headers=header)
      s2 = response.status_code 
      if s2 == 200:
        time.sleep(random.uniform(15, 18))
        print(f"任务完成")
      else:
        print(f"任务失败")  
def sf_fm_d():#蜂蜜浏览任务领取
   header = test_header()   
   url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~receiveExchangeIndexService~receiveHoney"
   taskType = [
    'BROWSER_CENTER_TASK_TYPE',
    'GATHER_HONEY_INIT_TASK_TYPE',
    'BEES_GAME_TASK_TYPE',
   ]
   for i in taskType:
      data = {
         "taskType": i
    }
      response = s.post(url=url,json=data,headers=header)
      time.sleep(2)
      response.encoding = "utf-8"  
      info = json.loads(response.text)
      if info['success']:
        print(f"领取成功")
      else:
         print("领取失败")
def sf_fm_e():# 蜂蜜积分
   header = test_header()
   url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~receiveExchangeIndexService~detail"
   data = {
        "pageNo": 1,
        "pageSize": 10
        }
   response = s.post(url, json=data, headers=header)
   response.encoding = "utf-8"
   info = json.loads(response.text)
   if info['success']:
     return info['obj']['usableHoney']
   else:
      print(info)

def sf_cs_a():# 财神抽卡
     header = test_getSign()
     sfcs = sf_cs_e()
     filtered_tasks = [task for task in sfcs if task['currency'] in ['WEALTH_CHANCE']]
     print("开始财神抽卡")
     for task in filtered_tasks:
        s1 = task['balance']
        print(f"当前抽卡次数:{s1}")
        for i in range(s1):
            url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~yearEnd2024WealthCardService~fortuneWealth"
            data = { }
            response = s.post(url, json=data, headers=header)
            time.sleep(random.uniform(3, 5))
            response.encoding = "utf-8"
            info = json.loads(response.text)
            print(f"正在抽卡：第{i+1}次")
def sf_cs_b():# 财神任务列表  此处只写两个任务
   header = test_getSign()
   url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~activityTaskService~taskList"
   data = {"activityCode":"YEAREND_2024","channelType":"MINI_PROGRAM"}
   response = s.post(url, json=data, headers=header)
   response.encoding = "utf-8"
   sf = []
   info = json.loads(response.text)
   if info['success']:
     tasks = info['obj']
     filtered_tasks = [task for task in tasks if task['taskType'] in ['BROWSE_VIP_CENTER', 'BROWSE_ANNUAL_REPORT']]
     for task in filtered_tasks:
        sf.append(task)
   else:
      print("获取失败")
   return sf  
def sf_cs_c():# 财神-套财神
   header = test_getSign()
   url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~yearEnd2024GameService~win"
   print("开始套财神15关")
   for levelIndex in range(1, 16):
    data = {
    "levelIndex": levelIndex}
    time.sleep(random.uniform(8, 12))
    response = s.post(url, json=data, headers=header)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if info['success']:
      print(f"第{levelIndex}关成功")
    else:
      print(info)

def sf_cs_d():# 财神-浏览任务奖励
   header = test_getSign()
   sfcs = sf_cs_b()
   print("开始领取财神任务奖励")
   for code in sfcs:
    url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberEs~taskRecord~finishTask"
    data = {"taskCode":code['taskCode']}
    response = s.post(url, json=data, headers=header)
    response.encoding = "utf-8"
    info = json.loads(response.text)
    if info['success']:
      time.sleep(5)
      print(f"任务完成")
    else:
      print(info)

def sf_cs_e():# 财神-信息
   header = test_getSign()
   url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~yearEnd2024TaskService~fetchTasksReward"
   data = {}
   response = s.post(url,json=data, headers=header)
   response.encoding = "utf-8"
   info = json.loads(response.text)
   if info['success']:
    return info['obj']['currentAccountList']  
   else:
    print(info)
def sf_cs_f():# 财神-浏览任务
   header = test_getSign()
   sfcs = sf_cs_b()
   print("开始浏览财神任务")
   for code in sfcs:
    url = code['buttonRedirect']
    response = s.get(url, headers=header)
    s2 = response.status_code 
    if s2 == 200:
        random_pause()
        print(f"任务完成")
    else:
        print(f"任务失败")  

def sf_cs_g():# 财神-领取财神任务奖励
    sfcs = sf_cs_e()
    currency_to_god = {
    'EAST_WEALTH': '东方财神',
    'MIDDLE_WEALTH': '中财神',
    'NORTH_WEALTH': '北方财神',
    'SOUTH_WEALTH': '南方财神',
    'WEST_WEALTH': '西方财神'
}
    balances = {god: 0 for god in currency_to_god.values()}
    for item in sfcs:
     if item['currency'] in currency_to_god:
        balances[currency_to_god[item['currency']]] = item['balance']
    return f"东方财神：{balances['东方财神']} 西方财神：{balances['西方财神']} 中财神：{balances['中财神']} 南方财神：{balances['南方财神']} 北方财神：{balances['北方财神']}"

def index(url):
    try:
     url = url  
     header = {
        "authority": "mcs-mimp-web.sf-express.com",
        "scheme": "https",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        }
     response = s.get(url, headers=header)
     login_mobile = s.cookies.get_dict().get('_login_mobile_', '')
     print(f"登陆成功，用户名: {login_mobile}")
     current_time = time.localtime()
     day = current_time.tm_mday
     time.sleep(random.uniform(3, 5))
     print("******************积分任务********************")
     print(f"账号[{login_mobile}]任务执行前积分：{sf_a()}")
     time.sleep(2)
     sf_c()
     time.sleep(2)
     if day in [1,10,20]:
      sf_d()
     time.sleep(3)
     sf_b()
     time.sleep(2)
     print(f"账号[{login_mobile}]任务执行后积分：{sf_a()}")
     print("******************收件兑奖任务********************")
     print(f"账号[{login_mobile}]任务执行前蜂蜜：{sf_fm_e()}")
     sf_fm_a()
     sf_fm_c()
     sf_fm_d()
     print(f"账号[{login_mobile}]任务执行后蜂蜜：{sf_fm_e()}")
     print("******************财神任务********************")
     print(f"账号[{login_mobile}]任务执行前财神卡：{sf_cs_g()}")
     sf_cs_f()
     sf_cs_d()
     sf_cs_c()
     sf_cs_a()
     print(f"账号[{login_mobile}]任务执行后财神卡：{sf_cs_g()}")
     if day in [26, 27, 28]:
         print("******************会员日任务********************")
         print("开始会员日任务")
         sf_hyr_a()
         sf_hyr_b()
         sf_hyr_c()
         sf_hyr_e()
         sf_hyr_f()
         print("再次检测红包数量")
         sf_hyr_c()
    except Exception as e:
        print(e)
def sicxs():
    # 从系统环境变量获取cookie
    try:
        os.environ
        env_cookie = os.environ.get("sfsy")
        si_cookie = getattr(config, 'sfsy', '') 
        if env_cookie and si_cookie:
            cookies = env_cookie + "\n" + si_cookie
        elif env_cookie:
            cookies = env_cookie
        elif si_cookie:
            cookies = si_cookie
        else:
            print("请设置变量 export sfsy='' 或在 config.py 中设置 sfsy")
            sys.exit()
    except Exception as e:
        print("请设置变量 export sfsy='' 或在 config.py 中设置 sfsy")
        sys.exit()
    list_cookie = re.split(r'\n', cookies)
    total_cookies = len(list_cookie)
    
    for i, list_cookie_i in enumerate(list_cookie):
        print(f'\n----------- 账号【{i + 1}/{total_cookies}】执行 -----------')
        try:
            index(list_cookie_i)
        except Exception as e:
            print(f"执行账号【{i + 1}】时发生错误: {e}")

    print(f'\n-----------  执 行  结 束 -----------')

if __name__ == '__main__':
   sicxs()
