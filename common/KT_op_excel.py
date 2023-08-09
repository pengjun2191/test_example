# -*- coding:utf8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import xlrd,xlwt,xlsxwriter
from xlutils.copy import copy
from datetime import datetime


class OpExcel(object):
	"""读取excel"""
	def __init__(self, file_path):
		super(OpExcel, self).__init__()
		self.file_path=file_path
		self.Excel = xlrd.open_workbook(file_path)
		self.tables = self.Excel.sheet_names()

	def get_tableindex(self,table):
		#获取excel需要操作的sheet的索引值
		if table in self.tables:
			index_data=self.tables.index(table)
			return (index_data)
		else:
			print (table+u'不是excel的sheet名称')
			return False

	def get_data(self):
		#获取excel所有数据已字典形式保存，按行取
		excle={}
		for table in self.tables:
			all_value=[]
			for i in range(self.get_nrows(table)):
				all_value.append(self.get_rowdate(table,i))
			excle[table]=all_value
		return excle

	def get_nrows(self,table):
		#获取表行数
		self.sheet=self.Excel.sheet_by_name(table)
		self.nrows=self.sheet.nrows
		return self.nrows

	def get_mcols(self,table):
		#获取表列数
		self.sheet=self.Excel.sheet_by_name(table)
		self.mcols=self.sheet.mcols
		return self.mcols

	def get_rowdate(self,table,nrow=0,mcol=0):
		#从M列开始获取第N行数据
		self.sheet=self.Excel.sheet_by_name(table)
		data=self.sheet.row_values(nrow)
		n=len(data)
		for i in range(n):
			data[i]=self.get_cellate(table,nrow,i)[1]
		return (data[mcol:])

	def get_coldate(self,table,nrow=0,mcol=0):
		#从N行开始获取第M列数据
		self.sheet=self.Excel.sheet_by_name(table)
		data=self.sheet.col_values(mcol)
		n=len(data)
		for i in range(n):
			data[i]=self.get_cellate(table,i,mcol)[1]
		return (data[nrow:])

	def get_cellate(self,table,nrow=0,mcol=0):
		#获取某个单元格数据和类型
		#ctype : 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
		self.sheet=self.Excel.sheet_by_name(table)
		type1=self.sheet.cell(nrow,mcol).ctype
		if (type1 == 3):
			data_value = xlrd.xldate_as_tuple(self.sheet.cell(nrow,mcol).value,self.Excel.datemode)
			value = datetime(*data_value)
		else:
			value=self.sheet.cell(nrow,mcol).value
		data=[type1,value]
		return (data)

	def get_mergedcell(self,table):
		#获取合并单元格有值得行和列
		self.sheet=self.Excel.sheet_by_name(table)
		data = []
		for (nrow,rowhigh,mcol,colhigh) in self.sheet.merged_cells:
			data.append([nrow,mcol])
		return (data)

	def get_ctype3(self,table):
		#检查每一个单元格的ctype:0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
		#输出ctype=3的单元格
		nrows=self.get_nrows(table)
		mcols=self.get_mcols(table)
		data=[]
		for nrow in range(nrows):
			for mcol in range(mcols):
				type=self.sheet.cell(nrow,mcol).ctype
				if (type==3):
					data.append([nrow,mcol])
		if data !=[]:
			return data
		else:
			return False

	def get_datarow(self,table,data,cols=0):
		#根据内容查找nrow行
		if type(data)==str or type(data)==unicode:
			mcol=None
			nlist=[]
			datanrow={}
			table_data=self.get_coldate(table,0,cols)
			print(u'开始查找数据')
			for nrow,row_data in enumerate(table_data):
				if row_data == data:
					nlist.append(nrow)
					print ('%s is in the %s Row'%(data,str(nrow)))
			if nlist!=[] :
				datanrow[data]=nlist
				return (datanrow)
			else:
				print (u'没匹配到数据')
				return False
		else:
			print('Value type is wrong')
			return False

	def get_datarowcol(self,table,data):
		#根据内容查找nrow,mcol，行列
		mcol=None
		nlist=[]
		all_data=self.get_data()
		table_data=all_data[table]
		print(u'开始查找数据')
		for row_data in table_data:
			nrow=table_data.index(row_data)
			if data in row_data:
				mcol=row_data.index(data)
				print (u'第'+str(nrow)+u'行已找到数据，数据在第'+str(mcol)+'列')
				nlist.append([data,nrow,mcol])
			else:
				print (u'第'+str(nrow)+u'行没找到数据')
		if nlist!=[] :
			return (nlist)
		else:
			print (u'没匹配到数据')
			return False

class EdXls(object):
	"""编辑追加Xls"""
	def __init__(self, file_path):
		super(EdXls, self).__init__()
		self.file_path=file_path
		self.rd_excel=OpExcel(self.file_path)
		self.book=copy(self.rd_excel.Excel)
		
	
	def get_sheet(self,sheet_name):
		#获取需要编辑的sheet
		index=self.rd_excel.get_tableindex(sheet_name)
		newsheet=self.book.get_sheet(index)
		return newsheet

	def write_rows(self,sheet,values,nrow=0,mcols=0):
		#从第mcols列开始填充第nrow行数据
		for mcol in range(0,len(values)):
			sheet.write(nrow,mcol+mcols,values[mcol])
		return True

	def write_cols(self,sheet,values,mcol=0,nrows=0):
		#从第nrows行开始填充第mcol列数据
		for nrow in range(0,len(values)):
			sheet.write(nrow+nrows,mcol,values[nrow])
		return True

	def save_file(self):
		#保存编辑的excel
		self.book.save(self.file_path)
		return True




class WtXls(object):
	"""创建excel"""
	def __init__(self,file_name):
		super(WtXls, self).__init__()
		self.file_name = file_name
		self.book=xlwt.Workbook()

	def add_sheet(self,sheet_name):
		#新增一个sheet，避免重复操作单元格报错：cell_overwrite_ok=True
		self.sheet=self.book.add_sheet(sheet_name,cell_overwrite_ok=True)
		return self.sheet

	def write_rows(self,sheet,nrow,mcols,values):
		#从第mcols列开始填充第nrow行数据
		for mcol in range(0,len(values)):
			sheet.write(nrow,mcol+mcols,values[mcol])
		return True


	def write_cols(self,sheet,nrows,mcol,values):
		#从第nrows行开始填充第mcol列数据
		for nrow in range(0,len(values)):
			sheet.write(nrow+nrows,mcol,values[nrow])
		return True


	def write_merge(self,sheet,nrows_mcols):
		#填充合并单元格
		for nrow_mcol in nrows_mcols:
			sheet.write_merge(nrow_mcol[0],nrow_mcol[1],nrow_mcol[2],nrow_mcol[3],nrow_mcol[4])
		return True

	def save_file(self):
		#保存excel
		self.book.save(self.file_name)
		return True

class WtXlsx(object):
	"""docstring for WtXlsx"""
	def __init__(self, file_name):
		super(WtXlsx, self).__init__()
		self.file_name = file_name
		self.book = xlsxwriter.Workbook(file_name)

	def add_sheet(self,sheet_name):
		#新增一个sheet
		self.sheet=self.book.add_worksheet(sheet_name)
		return self.sheet

	def write_rows(self,sheet,nrow,mcols,values):
		#从第mcols列开始填充第nrow行数据
		for mcol in range(0,len(values)):
			sheet.write(nrow,mcol+mcols,values[mcol])
		return True

	def write_cols(self,sheet,nrows,mcol,values):
		#从第nrows行开始填充第mcol列数据
		for nrow in range(0,len(values)):
			sheet.write_string(nrow+nrows,mcol,values[nrow])
		return True

	def format(self,arg):
		#设置单元格式
		format=self.book.add_format()
		format.set_border(arg[0])
		if len(arg)>1:
			format.set_bg_color(arg[1])
		elif len(arg)>2:
			format.set_align(arg[2])
		return format

	def chart_series_rows(self,chart,sheet_name,nrows,nrow,mcol,mcols):
	#按行设置图表值
		categories='='+sheet_name+'!$'+chr(ord(mcol)+1)+'$'+nrows+':$'+mcols+'$'+nrows
		values='='+sheet_name+'!$'+chr(ord(mcol)+1)+'$'+nrow+':$'+mcols+'$'+nrow
		name='='+sheet_name+'!$'+mcol+'$'+nrow
		chart.add_series({
			'categories': categories,    #将nrows行第mcol到mcols列的数据作为x轴
			'values':     values,    #将nrow行第mcol到mcols列的数据作为柱状图数据
			#为数据区域
			'line':       {'color': 'black'},    #线条颜色定义为black(黑色)
			'name': name,    #引用第一列第nrow行数据作为统计项
		})

	def chart_series_cols(self,chart,sheet_name,nrows,nrow,mcol,mcols):
	#按列设置图表值
		categories='='+sheet_name+'!$'+mcol+'$'+str(nrows+1)+':$'+mcol+'$'+nrow
		values='='+sheet_name+'!$'+mcols+'$'+str(nrows+1)+':$'+mcols+'$'+nrow
		name='='+sheet_name+'!$'+mcols+'$'+str(nrows)
		chart.add_series({
			'categories': categories,    #将nrows行第mcol到mcols列的数据作为x轴
			'values':     values,    #将nrow行第mcol到mcols列的数据作为柱状图数据
			#为数据区域
			'line':       {'color': 'black'},    #线条颜色定义为black(黑色)
			'name': name,    #引用第一列第nrow行数据作为统计项
		})

	def write_chart(self,sheet,width_height,names,cell,nrows_mcols):
		#按行生成图表
		chart = self.book.add_chart({'type': 'column'})
		for nrow in range(nrows_mcols[1]+1, nrows_mcols[2]+1):    #数据域以第nrow+1～nrow行进行图表数据系列函数调用
			self.chart_series_rows(chart,nrows_mcols[0],str(nrows_mcols[1]),str(nrow),nrows_mcols[3],nrows_mcols[4])
		
		for col in range(1,ord(nrows_mcols[4])-ord(nrows_mcols[3])+1):
			self.chart_series_cols(chart,nrows_mcols[0],nrows_mcols[1],str(nrows_mcols[2]),nrows_mcols[3],chr(ord(nrows_mcols[3])+col))
		
		chart.set_size({'width': width_height[0], 'height': width_height[1]})    #设置图表大小
		chart.set_title ({'name': names[0]})    #设置图表（上方）大标题
		chart.set_y_axis({'name': names[1]})    #设置y轴（左侧）小标题
		chart.set_x_axis({'name': names[2]})    #设置x轴（下方）小标题
		sheet.insert_chart(cell, chart)    #在cell单元格插入图表

	def save_file(self):
		#关闭操作的xlsx
		self.book.close()



if __name__ == '__main__':
	file='./config/Data_Case.xls'
	OpExcel=OpExcel(file)
	table_dict=OpExcel.get_data()
		

	
	'''
	file = '..\\data\\result_data\\result.xls'
	table=u'sys_machine_process'
	mcol=10
	nrow=10
	OpExcel=EdXls(file)
	a=OpExcel.get_sheet('sys_config')
	OpExcel.write_rows(a,nrow,mcol,['a','b','c'])
	OpExcel.save_file()	
	'''
	
	
	'''	
	import random
	def get_num():
		return random.randrange(0, 201, 2)
	title=['result','fail','success']
	buname= [u'a',u'b',u'c',u'd',u'e']    
	data = []
	for i in range(2):
		tmp = []
		for j in range(5):
			tmp.append(get_num())
		data.append(tmp)
	file = 'C:\\Users\\a\\Desktop\\hua\\a.xlsx'
	table=u'sys_machine_process'
	print(file)
	OpExcel=WtXlsx(file)
	a=OpExcel.add_sheet(table)
	format=OpExcel.format([1,'#cccccc','center'])
	OpExcel.write_rows(a,1,2,buname)
	OpExcel.write_cols(a,1,1,title)
	n=2
	for data_value in data:
		OpExcel.write_rows(a,n,2,data_value)
		n=n+1
	width_height=[300,287]
	names=['data_result','number','names']
	cell='B8'
	nrows_mcols=[table,2,2+len(data),'B',chr(ord('B')+len(title)-1)]
	OpExcel.write_chart(a,width_height,names,cell,nrows_mcols)
	OpExcel.save_file()'''

	'''import random
				def get_num():
					return random.randrange(0, 201, 2)
				title=['result','fail','success']
				buname= [u'a',u'b',u'c',u'd',u'e']    
				data = []
				for i in range(5):
					tmp = []
					for j in range(2):
						tmp.append(get_num())
					data.append(tmp)
				file = 'C:\\Users\\a\\Desktop\\hua\\a.xlsx'
				table=u'sys_machine_process'
				print(file)
				OpExcel=WtXlsx(file)
				a=OpExcel.add_sheet(table)
				format=OpExcel.format([1,'#cccccc','center'])
				OpExcel.write_rows(a,1,1,title)
				OpExcel.write_cols(a,2,1,buname)
				n=2
				for data_value in data:
					OpExcel.write_rows(a,n,2,data_value)
					n=n+1
				width_height=[300,287]
				names=['data_result','number','names']
				cell='B8'
				nrows_mcols=[table,2,2+len(data),'B',chr(ord('B')+len(title)-1)]
				print(nrows_mcols)
				OpExcel.write_chart(a,width_height,names,cell,nrows_mcols)
				OpExcel.save_file()
			'''

	

