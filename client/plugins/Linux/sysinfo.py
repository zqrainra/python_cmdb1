#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Bob'

import commands,re,os

def collect():
    filter_list = ['Manufacturer','Serial Number','Product Name','UUID','Wake-up Type']
    raw_data = {}

    for key in filter_list:
        try:
            res = commands.getoutput('sudo dmidecode -t system|grep "%s"' % (key))
            if res :
                raw_data[key] = res.split(':')[-1]
            else:
                raw_data[key] = -1
        except Exception,e:
            print(e)

    asset_data = {}
    server_data = {}
    server_data['Manufacturer'] = raw_data['Manufacturer']
    server_data['Serial Number'] = raw_data['Serial Number']
    server_data['Product Name'] = raw_data['Product Name']
    server_data['UUID'] = raw_data['UUID']
    server_data['Wake-up Type'] = raw_data['Wake-up Type']
    asset_data['server_info']=server_data
    collect_nic = Collect_nic()
    asset_data['nic_info'] = collect_nic.nicinfo()
    asset_data['ram_info'] = ram_info()
    asset_data['os_info'] = osinfo()
    asset_data['cpu_info'] = cpuinfo()
    asset_data['disk_info'] = diskinfo()

    return asset_data

#收集CPU信息
def cpuinfo():
    base_cmd = 'cat /proc/cpuinfo'
    cmd_dic = {
        'cpu_type':'%s|grep "model name"|head -1' % base_cmd,
        'cpu_count':'%s|grep "model name"|wc -l' % base_cmd,
        'cpu_core_count':"%s|grep 'cpu cores'|awk -F ': ' '{S=S+$2}END{print S}'" % base_cmd,
    }
    data_dic = {
        'cpu_type':commands.getoutput(cmd_dic['cpu_type']).split(':')[1].strip(),
        'cpu_count':commands.getoutput(cmd_dic['cpu_count']),
        'cpu_core_count':commands.getoutput(cmd_dic['cpu_core_count']),
    }
    return data_dic

#操作系统信息
def osinfo():
    os_distribution  = commands.getoutput('uname -o')
    os_release = commands.getoutput('cat /etc/redhat-release')
    os_type = 'linux'
    os_info = {}
    os_info['os_distribution'] =os_distribution
    os_info['os_release'] = os_release
    os_info['os_type'] = os_type
    return os_info



class Collect_nic(object):#收集网卡信息
    def __init__(self):
        self.nic_name = ''
        self.mac_addr = ''
        self.ip_addr = ''
        self.bording = 0
        self.Bcast = ''
        self.Mask = ''

    def add_dic_data(self):
        ip_dic = {
            'nic_name': self.nic_name,
            'mac_addr': self.mac_addr,
            'ip_addr': self.ip_addr,
            'bording': self.bording,  # 是否绑定
            'Bcast': self.Bcast,
            'Mask': self.Mask
        }
        return  ip_dic

    def nicinfo(self):
        tmp = commands.getoutput('sudo ifconfig -a').split('\n')
        self.raw_data = []
        next_ip_line = False
        ip_dic = {}

        for line in tmp:
            if 'HWaddr' in line:#判断所在行是否有mac地址
                self.nic_name = line.split()[0]
                self.mac_addr = line.split('HWaddr ')[-1].strip()
                next_ip_line = True
            if 'inet addr:' in line and next_ip_line:#是否在mac地址的下一行
                next_ip_line = False
                split_list = re.split(':| ',line)
                # print(split_list)
                self.ip_addr = split_list[split_list.index('addr') + 1]
                self.Bcast = split_list[split_list.index('Bcast') + 1]
                self.Mask = split_list[split_list.index('Mask') + 1]
                if len(self.raw_data) > 0:
                    for data_dic in self.raw_data:
                        if self.mac_addr in data_dic.values():#判断mac地址是否已经存在列表中，如果存在表示这个ip为vip
                            self.bording = 1
                ip_dic = self.add_dic_data()
                self.raw_data.append(ip_dic)
                ip_dic = {}
        return self.raw_data


#硬盘信息
def diskinfo():
    obj = DiskPlugin()
    return obj.linux()

#内存信息
def ram_info():
    tmp_list = commands.getoutput('sudo dmidecode -t 17').split('\n')
    res_list = []
    next_text = False
    content_dic = {}
    for line in tmp_list:
        data_list = line.split(':')
        if data_list[0].strip() == 'Size':
            if data_list[1].strip() == 'No Module Installed':
                continue
            else:
                content_dic['size'] = data_list[1].strip()
                next_text = True
        if data_list[0].strip() == 'Locator'and next_text:
            content_dic['solt'] = data_list[1].strip()
        if data_list[0].strip() == 'Type' and next_text:
            content_dic['type'] = data_list[1].strip()
        if data_list[0].strip() == 'Manufacturer' and next_text:
            content_dic['manufacturer'] = data_list[1].strip()
        if data_list[0].strip() == 'Serial Number' and next_text:
            content_dic['sn'] = data_list[1].strip()
        if data_list[0].strip() == 'Asset Tag' and next_text:
            content_dic['asset_tag'] = data_list[1].strip()
            if len(content_dic) and next_text> 0:
                res_list.append(content_dic)
                content_dic = {}
                next_text = False
    return res_list

class DiskPlugin(object):

    def linux(self):
        result = {'physical_disk_driver':[]}

        try:
            script_path = os.path.dirname(os.path.abspath(__file__))
            shell_command = "sudo %s/MegaCli  -PDList -aALL" % script_path
            output = commands.getstatusoutput(shell_command)
            result['physical_disk_driver'] = self.parse(output[1])
        except Exception,e:
            result['error'] = e
        return result

    def parse(self,content):
        '''
        解析shell命令返回结果
        :param content: shell 命令结果
        :return:解析后的结果
        '''
        response = []
        result = []
        for row_line in content.split("\n\n\n\n"):
            result.append(row_line)
        for item in result:
            temp_dict = {}
            for row in item.split('\n'):
                if not row.strip():
                    continue
                if len(row.split(':')) != 2:
                    continue
                key,value = row.split(':')
                name =self.mega_patter_match(key);
                if name:
                    if key == 'Raw Size':
                        raw_size = re.search('(\d+\.\d+)',value.strip())
                        if raw_size:

                            temp_dict[name] = raw_size.group()
                        else:
                            raw_size = '0'
                    else:
                        temp_dict[name] = value.strip()

            if temp_dict:
                response.append(temp_dict)
        return response

    def mega_patter_match(self,needle):
        grep_pattern = {'Slot':'slot', 'Raw Size':'capacity', 'Inquiry':'model', 'PD Type':'iface_type'}
        for key,value in grep_pattern.items():
            if needle.startswith(key):
                return value
        return False






