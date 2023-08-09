# -*- coding: utf8 -*-
'''配置处理'''



import os
import configparser as ConfigParser
import common.KT_Data_PRS as Data_PRS
import yaml


class MyConfigParser(ConfigParser.ConfigParser):
    def __init__(self, defaults=None):
        ConfigParser.ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        return optionstr
""" 
conf = MyConfigParser()
conf.read("************") 
"""


class Config_yaml:
	"""config yaml"""
	def __init__(self):
		super(Config_yaml,self).__init__()
	
	def config_yaml(self,yaml_file):
		file=open(yaml_file,'r', encoding="utf-8")
		file_data=file.read()
		file.close()
		yaml_data=yaml.safe_load(file_data)
		return yaml_data



class Project(object):
	"""Project operate"""
	def __init__(self):
		super(Project, self).__init__()
		self.conf = MyConfigParser()

	def project(self,file):
		"""读取配置文件中所有项目"""
		self.conf.read(file)
		sections = self.conf.sections()
		return sections

	def Useproject(self,file,section):
		''' 获取项目及相应配置'''
		self.conf.read(file)
		Cdata=Data_PRS.Pdata()
		conf_data=Cdata.CreateTwoDict(section,self.conf.items(section))
		return conf_data

	def RD_listconfig(self,file,section,Items):
		#根据配置项查找配置值,返回list内容值
		values=[]
		if os.path.exists(file):
			self.conf.read(file) 
			for n in range(len(Items)):
				values.append(self.conf.get(section,Items[n]))
			return (values)
		else:
			return False

	def RD_dictconfig(self,file,section,Items):
		#根据配置项查找配置值,字典形式返回
		values={}
		if os.path.exists(file):
			self.conf.read(file) 
			for n in range(len(Items)):
				values[Items[n]]=self.conf.get(section,Items[n])
			return (values)
		else:
			return False

class ProJconfig(object):
	"""docstring for ProJconfig"""
	def __init__(self):
		super(ProJconfig, self).__init__()
		self.conf = MyConfigParser()

	def New_config(self,file,conf_data):
		#新建模式写入配置文件
		for section in conf_data.keys():
			cfg=open(file, "w")
			print (u'添加项目名称：'+section)
			self.conf.add_section(section)
			for item in conf_data[section].keys():
				print (u'添加配置项：'+item+' = '+conf_data[section][item])
				self.conf.set(section,item,conf_data[section][item])
			self.conf.write(cfg)
			cfg.close()
		return True

	def Edit_config(self,file,conf_data):
		#追加模式写入配置文件
		print (u'新加配置相关内容如下:')
		print (conf_data)
		for section in conf_data.keys():
			print (u'添加项目名称：'+section)
			self.Del_config(file,section)
			#写入项目配置项信息
			self.conf.add_section(section)
			for item in conf_data[section].keys():
				print (u'添加配置项：'+item+' = '+conf_data[section][item])
				self.conf.set(section,item,conf_data[section][item])
			self.conf.write(open(file, "a"))
			open(file, "a").close()
		return True

	def Del_config(self,file,section):
		#删除配置项目信息
		self.conf.read(file)
		if self.conf.has_section(section):
			self.conf.remove_section(section)
		self.conf.write(open(file, "w"))
		open(file, "w").close()
		return True


if __name__ == '__main__':
	'''	a={'Oraclektv4':[('a1','b1'),('a2','b2')],'e':[('a1','b1'),('a2','b2')]}
	b=Data_PRS.Pdata()
	c=b.DL_To_Dict(a)#
	file='..//..//data//db_config//AllDbconfig.cfg'
	d=ProJconfig()
	e=d.WT_allconfig(file,c)
	print (e)
	'''

	ALLDbconfig='..//..//config//db_config//AllDbconfig.cfg'
	a=Project()
	b=a.project(ALLDbconfig)
	print (b)
