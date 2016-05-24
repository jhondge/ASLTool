#!/usr/bin/python
#coding:utf-8

__author__ = "Jackson"

import os

import re

from XlWorkers import Utils
from XlWorkers.Config import Lang
from XlWorkers.StrResXml import StrResXml
from XlWorkers.exceltemplatereader import FOExcelReader
from XlWorkers.androidresource import FOAndroidModule

class FOStringTranslator(object):
	"""docstring for FOStringTranslator"""
	def __init__(self,callback):
		self.callback = callback
		# super.__init__(self)
		# self.projectPath = projectPath
		# self.excelPath = excelPath

	def loadLibrary(self,projectPath,loadLibraryCallback):

		self.projectPath = projectPath

		settingPath = os.path.join(self.projectPath,"settings.gradle");
		
		self.callback("loading gradle setting file:",settingPath)
		self.libraries = []
		try:
			gradleSettingFile = open(settingPath,"r")
			for line in gradleSettingFile.readlines():
				if len(line.strip()) > 0 and line.startswith("//") == False:
					# self.callback(line)
					modules = line.strip().split(',')
					for module in modules:
						pattern = re.compile("'(.*)'")
						values = pattern.findall(module)
						for value in values:
							segments = value.split(':');
							library = os.path.join(self.projectPath,*segments)
							loadLibraryCallback(library)
							self.libraries.append(library)
			# self.callback("<<<<<<<read setting file completion")
			return self.libraries
		except Exception as e:
			self.callback("file not found",e)
		else:
			pass
		finally:
			self.callback("completion loading gradle setting file")
			pass
		pass


	def setExcelPath(self,excelPath):
		self.excelPath = excelPath
		pass

	def doTranslate(self,targetLibraries=None):
		#init excel reader and load to memory
		self.excelReader = FOExcelReader(self.excelPath,self.callback)
		if targetLibraries is not None:
			self.libraries = targetLibraries
		
		for libraryPath in self.libraries:
			self.callback(">>>>>>>> scaning and translate library : ",os.path.basename(libraryPath))
			libraryTranslator = FOAndroidModule(libraryPath,self.callback)
			libraryTranslator.doTranslate(self.excelReader)
			self.callback("<<<<<<<< scaning and translate library : ",os.path.basename(libraryPath))
			
		
	def hasDefinedKey(res_key):
		#find all of project string.xml to 
		pass

	def updateString(res_key,lang_code,value):

		pass