#coding:utf-8
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
# Create your models here.
from myauth import UserProfile

@python_2_unicode_compatible
class Asset(models.Model):
    asset_type_choice = (
        ('server',u'服务器'),
        ('switch',u'交换机'),
        ('router',u'路由器'),
        ('firewall',u'防火墙'),
        ('storage',u'存储设备'),
        ('NLB',u'NetScaler'),
        ('wireless',u'无线AP'),
        ('software',u'软件资产'),
        ('others',u'其他资产'),
    )

    asset_type = models.CharField(choices=asset_type_choice,max_length=64,default='server')
    asset_name = models.CharField(max_length=64,unique=True)
    sn = models.CharField(u'资产号',max_length=128,unique=True)
    manufacturer = models.ForeignKey('Manufacturer',verbose_name=u'生产厂商',null=True,blank=True)
    management_ip = models.GenericIPAddressField(u'管理IP',null=True,blank=True)
    contract = models.ForeignKey('Contract',verbose_name=u'合同',null=True,blank=True)
    trade_date = models.DateField(u'购买时间',null=True,blank=True)
    expire_date = models.DateField(u'过保时间',null=True,blank=True)
    business_unit = models.ForeignKey('Business_unit',verbose_name=u'所属业务线',null=True,blank=True)
    tags = models.ManyToManyField('Tags',verbose_name='tags',blank=True)
    admin = models.ForeignKey('UserProfile',verbose_name=u'管理员',null=True,blank=True)
    idc = models.ForeignKey('IDC',verbose_name=u'所属IDC',null=True,blank=True)
    memo = models.TextField(u'备注',null=True,blank=True)
    create_date = models.DateTimeField(u'创建时间',auto_now_add=True)
    update_date  = models.DateTimeField(u'修改时间',auto_now=True)

    class Meta:
        verbose_name = u'资产总表'
        verbose_name_plural = u'资产总表'

    def __str__(self):
        return self.asset_name

@python_2_unicode_compatible
class Server(models.Model):
    asset = models.OneToOneField('Asset')
    create_choice = (
        ('auto','Auto'),
        ('manual','Manual'),
    )
    create_type = models.CharField(u'创建方式',choices=create_choice,max_length=64)
    hosted_on = models.ForeignKey('self',related_name='host_on_server',null=True,blank=True)#虚拟机用
    cpu_model = models.CharField(u'型号',max_length=128,null=True,blank=True)
    raid_type = models.CharField(u'RAID类型',max_length=512,null=True,blank=True)
    os_type = models.CharField(u'操作系统类型',max_length=64,null=True,blank=True)
    od_distribution = models.CharField(u'发行版本',max_length=64,null=True,blank=True)
    od_release = models.CharField(u'系统版本',max_length=64,null=True,blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = '服务器'

    def __str__(self):
        return self.cpu_model

@python_2_unicode_compatible
class NetworkDevice(models.Model):
    asset = models.OneToOneField('Asset')
    vlan_ip = models.GenericIPAddressField(u'VlanIP',null=True,blank=True)
    lan_ip = models.GenericIPAddressField(u'内网IP',null=True,blank=True)
    sn = models.CharField(u'SN型号',max_length=128,unique=True)
    model = models.CharField(u'型号',max_length=64,null=True,blank=True)
    port_num = models.IntegerField(u'端口个数',null=True,blank=True)
    device_detail = models.TextField(u'设置详细配置',null=True,blank=True)
    firmware = models.ForeignKey('Software',verbose_name=u'软件')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u'网络设备'
        verbose_name_plural = u'网络设备'

    def __str__(self):
        return self.sn

@python_2_unicode_compatible
class Software(models.Model):
    os_type_choice = (
        ('linux','Linux'),
        ('windows','Windows'),
        ('software','Software'),
    )
    os_distribution_choice = (
        ('windows','Windows'),
        ('centos','Centos'),
        ('ubantu','Ubantu')
    )
    language_choice = (('cn','cn'),('en','en'))
    os_type = models.CharField(choices=os_type_choice,max_length=64,help_text='eg. Gnu/Linux',default='Linux')
    os_distribution = models.CharField(choices=os_distribution_choice,max_length=64,default='centos')
    version = models.CharField(u'软件/系统版本',max_length=64)
    language = models.CharField(choices=language_choice,max_length=32,default='cn')

    class Meta:
        verbose_name = u'软件/系统'
        verbose_name_plural = u'软件/系统'

    def __str__(self):
        return self.sn

@python_2_unicode_compatible
class CPU(models.Model):
    asset = models.OneToOneField('Asset')
    cpu_model = models.CharField(u'CPU型号',max_length=64)
    cpu_count = models.IntegerField(u'CPU个数')
    cpu_core_count = models.IntegerField(u'CPU核数')
    memo = models.TextField(u'备注',null=True,blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u'CPU'
        verbose_name_plural = u'CPU'

    def __str__(self):
        return self.cpu_model


@python_2_unicode_compatible
class RAM(models.Model):
    asset = models.ForeignKey('Asset')
    sn = models.CharField(u'sn号',max_length=128)
    model = models.CharField(u'内存型号',max_length=64)
    slot = models.CharField(u'插槽',max_length=64)
    capacity = models.IntegerField(u'容量')
    memo = models.TextField(u'备注', null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u'内存'
        verbose_name_plural = u'内存'
        unique_together = ('asset','slot')

    def __str__(self):
        return self.sn

@python_2_unicode_compatible
class Disk(models.Model):
    asset = models.ForeignKey('Asset')
    sn = models.CharField(u'sn号', max_length=128)
    slot = models.CharField(u'插槽', max_length=64)
    capacity = models.IntegerField(u'容量')
    manufacturer = models.ForeignKey('Manufacturer', verbose_name=u'生产厂商', null=True, blank=True)
    disk_interface_choice = (
        ('SATA', 'SATA'),
        ('SAS', 'SAS'),
        ('SCSI', 'SCSI'),
        ('SSD', 'SSD'),
    )
    disk_interface = models.CharField(choices=disk_interface_choice,max_length=64)
    memo = models.TextField(u'备注', null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u'硬盘'
        verbose_name_plural = u'硬盘'
        unique_together = ('asset', 'slot')

    def __str__(self):
        return self.sn

@python_2_unicode_compatible
class NIC(models.Model):
    asset = models.ForeignKey('Asset')
    sn = models.CharField(u'sn号', max_length=128)
    vlan_ip = models.GenericIPAddressField(u'VlanIP', null=True, blank=True)
    ip_addr = models.GenericIPAddressField(u'IP地址', null=True, blank=True)
    mac_addr = models.CharField(u'MAC地址',max_length=64,unique=True)
    memo = models.TextField(u'备注', null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u'网卡'
        verbose_name_plural = u'网卡'

    def __str__(self):
        return self.ip

@python_2_unicode_compatible
class RaidAdaptor(models.Model):
    asset = models.ForeignKey('Asset')
    sn = models.CharField(u'sn号', max_length=128)
    slot = models.CharField(u'插槽', max_length=64)
    model = models.CharField(u'型号', max_length=64)
    memo = models.TextField(u'备注', null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u'RAID卡'
        verbose_name_plural = u'RAID卡'
        unique_together = ('asset', 'slot')

    def __str__(self):
        return self.sn

@python_2_unicode_compatible
class Manufacturer(models.Model):
    name = models.CharField(u'生产厂商',max_length=128)
    contract = models.CharField(u'联系方式',max_length=256)
    memo = models.TextField(u'备注', null=True, blank=True)

    class Meta:
        verbose_name = u'厂商'
        verbose_name_plural = u'厂商'

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Contract(models.Model):
    name = models.CharField(u'合同名',max_length=128)
    date = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField(u'总价')
    memo = models.TextField(u'备注', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'合同'
        verbose_name_plural = u'合同'


@python_2_unicode_compatible
class Business_unit(models.Model):
    name = models.CharField(u'业务线名称', max_length=128)
    memo = models.TextField(u'备注', null=True, blank=True)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Tags(models.Model):
    name = models.CharField('Tag_name', max_length=64,unique=True)
    creator = models.ForeignKey('UserProfile',related_name='creator')
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class IDC(models.Model):
    name = models.CharField(u'IDC名称', max_length=128)
    memo = models.TextField(u'备注', null=True, blank=True)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class EventLog(models.Model):
    event_type_choice = (
        (1, u'硬件变更'),
        (2, u'新增配件'),
        (3, u'设备下线'),
        (4, u'设备上线'),
        (5, u'定期维护'),
        (6, u'业务上线\更新\变更'),
        (7, u'其它'),
    )
    event_type = models.CharField(choices=event_type_choice,max_length=64)
    asset = models.ForeignKey('Asset')
    component = models.CharField(u'事件子项',max_length=128)
    detail = models.TextField(u'时间详情')
    date = models.DateTimeField(u'时间',auto_now_add=True)
    user = models.ForeignKey('UserProfile',verbose_name=u'事件源')
    memo = models.TextField(u'备注', null=True, blank=True)

    def __str__(self):
        return self.event_type

@python_2_unicode_compatible
class NewAssetApprpval(models.Model):
    sn = models.CharField(u'资产编号',max_length=128,unique=True)
    asset_type_choice = (
        ('server', u'服务器'),
        ('switch', u'交换机'),
        ('router', u'路由器'),
        ('firewall', u'防火墙'),
        ('storage', u'存储设备'),
        ('NLB', u'NetScaler'),
        ('wireless', u'无线AP'),
        ('software', u'软件资产'),
        ('others', u'其他资产'),
    )

    asset_type  = models.CharField(u'资产类型',choices=asset_type_choice,max_length=128)
    manufactory = models.CharField(max_length=64,null=True,blank=True)
    model = models.CharField(max_length=128,null=True,blank=True)
    ram_size = models.IntegerField(null=True,blank=True)
    cpu_model = models.CharField(max_length=128, null=True, blank=True)
    cpu_count = models.IntegerField(null=True, blank=True)
    cpu_core_count = models.IntegerField(null=True, blank=True)
    os_distribution = models.CharField(max_length=128, null=True, blank=True)
    os_type = models.CharField(max_length=128, null=True, blank=True)
    os_release = models.CharField(max_length=128, null=True, blank=True)
    data = models.TextField(u'资产数据')
    date = models.DateTimeField(u'录入日期',auto_now_add=True)
    approved = models.BooleanField(u'已批准',default=False)
    approved_by = models.ForeignKey('UserProfile',verbose_name='批准人',blank=True,null=True)
    approved_date = models.DateTimeField(u'批准日期',null=True,blank=True)

    def __str__(self):
        return '%s:%s' % (self.asset_type,self.sn)

    class Meta:
        verbose_name = u'待批准资产'
        verbose_name_plural = u'待批准资产'
