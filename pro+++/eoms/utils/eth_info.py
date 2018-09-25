# encoding: utf-8
"""
Create on: 2018-09-25 上午12:25
author: sato
mail: ysudqfs@163.com
life is short, you need python
"""

# 获取服务器ip地址信息
import netifaces as netifaces
import subprocess

import psutil

serverip = {
	"isOuter": False,
	"inner":   {
		"ip":      "",
		"netMask": "",
		"gateway": "",
		"dns":     ""
	},
	"outer":   {
		"ip":      "",
		"netMask": "",
		"gateway": "",
		"dns":     ""
	},
	"url":     ""
}


def get_server_info():
	# inip, outip, eurl = get_ldd_info()
	# eth_info = get_eth_info()
	# if eth_info.get(inip):
	# 	md_net_card(eth_info.get(inip), 0, check=True)
	# serverip['url'] = eurl
	with open("/etc/resolv.conf", "r") as f:
		data = f.readlines()
	dns = ""
	for foo in data[1:]:
		dns += foo.split(" ")[1].strip()
		dns += "  "
	info = get_eth_info()[0]
	serverip['inner']['ip'] = info.get("ip")
	serverip['inner']['gateway'] = info.get("gateway")
	serverip['inner']['netMask'] = info.get("netmask")
	serverip['inner']['dns'] = dns
	serverip["outer"]["ip"] = (subprocess.getstatusoutput("curl ifconfig.me")[1]).split("\n")[-1]
	return serverip


# 获取网卡信息
def get_eth_info():
	netcard_info = []
	info = psutil.net_if_addrs()
	for k, v in info.items():
		for item in v:
			if item[0] == 2 and not item[1] == '127.0.0.1':
				netcard_info.append({
					"name": k, "ip": item[1],
					"netmask": item[2],
					"broadcast": item[3]
					})
	gateway = netifaces.gateways()['default'][netifaces.AF_INET][0]
	netcard_info[0]["gateway"] = gateway
	return netcard_info
	

if __name__ == '__main__':
	print(get_eth_info())
