# -*- coding: utf8 -*-
'''数据格式进行处理'''
import sys,os
class Pdata(object):
	"""docstring for Pdata"""
	def __init__(self):
		super(Pdata, self).__init__()

	def Tlist_TO_Dict():
		pass

	def List_To_Dict(self,list):
		'''[(a1,b1),(a2,b2)] To {a1:b1,a2:b2}'''
		dict={}
		for item in list:
			dict[item[0]] = item[1]
		return dict

	def DL_To_Dict(self,arg):
		'''{a:[(a1,b1),(a2,b2])} To {a:{a1:b1,a2:b2}} '''
		self.arg = arg
		data={}
		for key in self.arg.keys():
			list=self.arg[key]
			dict=self.List_To_Dict(list)
			data[key]=dict
		return data

	def CfileToDict(self,file):
		'''a=1 b=2 TO {a:1,b:2},文件数据处理'''
		read_file=open(file, 'r')
		dict={}
		for line in read_file:
			line=line.strip('\n')
			data=line.split('=')
			dict[data[0]]=data[1]
		read_file.close()
		return dict

	def CreateTwoDict(self,key,data):
		'''key=a,data=[(a1,b1),(a2,b2)]'''
		dict={}
		dict[key]=self.List_To_Dict(data)
		return dict


if __name__ == '__main__':
	a=[('a1','b1'),('a2','b2')]
	d='a'
	b=Pdata()
	c=b.CreateTwoDict(d,a)
	print (c)