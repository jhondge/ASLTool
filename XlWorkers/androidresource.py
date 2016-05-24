#!/usr/bin/python

__author__ = "Jackson"

import os

from XlWorkers.StrResXml import StrResXml

from XlWorkers.Config	import Lang

import XlWorkers.Utils as Utils

class FOAndroidModule(object):
	"""docstring for FOAndroidModule"""
	def __init__(self,projectPath,logger):
		# super.__init__(self)
		self.logger = logger
		self.rootPath = projectPath
		self.resRootPath = os.path.join(projectPath,"src","main","res")

		#store xml readers key(file name) values is keys
		self.needTranslateStrings = {}

		self.defaultStrResXmlReaders = []
		enResPath = os.path.join(self.resRootPath,"values")
		#load default language xml reander
		if os.path.exists(enResPath):
			for f in os.listdir(enResPath):
				# print("file:",f)
				realPath = os.path.join(enResPath, f)
				if os.path.isfile(realPath) and (f.endswith("strings.xml") or f.endswith("string.xml")):
					# print("real path:",realPath)
					self.logger("default xml reader:",os.path.basename(realPath))
					self.defaultStrResXmlReaders.append(StrResXml(realPath))
		'''
		#load all resource xml reader
		for lang_obj in Lang:
            for region_code in lang_obj.reverse_region_codes():
                suffix = '-' + region_code if Utils.is_str_valid(region_code) else region_code
                values_dir = path.join(self.resRootPath, 'values' + suffix)
                for f in os.listdir(values_dir):
					realPath = os.path.join(values_dir, f)
					if os.path.isfile(realPath) and (f.endswith("strings.xml") or f.endswith("string.xml")):
						self.defaultReaders.append(StrResXml(realPath))
		'''

		

	def doTranslate(self,excelReader):
		#translate english first (Because should be sure which keys will be tranlsate)
		for xmlReader in self.defaultStrResXmlReaders:
			self.needTranslateStrings[xmlReader.getIdentify()] = []
			needSave = False
			for entity in xmlReader.gen_trans_entities():
				if excelReader.hasResourceKey(entity.key):
					#if found out key in excel update it
					trans_str = excelReader.get_res_str(Lang.EN.code, entity.key)
					self.logger("need translate infile:{0} key:{1}".format(xmlReader.getIdentify(),entity.key))
					if Utils.is_str_valid(trans_str):
						self.needTranslateStrings[xmlReader.getIdentify()].append(entity.key)
						xmlReader.update_res_node(entity.key, trans_str)
						needSave = True
					pass
			if needSave:
				xmlReader.save()
		needTranslateItemTotal = 0
		for key, values in self.needTranslateStrings.items():
			needTranslateItemTotal = needTranslateItemTotal + len(values)
		if needTranslateItemTotal <= 0:
			self.logger("No one for translate in this library")
			return
		# print("need translate keys:",self.needTranslateStrings.keys())
		#update other languages
		for lang_obj in Lang:
			#don't translate english again
			if lang_obj != Lang.EN:
				for region_code in lang_obj.reverse_region_codes():
					suffix = '-' + region_code if Utils.is_str_valid(region_code) else region_code
					# print("translate language:",suffix)
					values_dir = os.path.join(self.resRootPath, 'values' + suffix)
					if os.path.exists(values_dir) != True:
						continue
					self.logger("begin translate language:",suffix[1:])
					xmlReaders = {}
					for f in os.listdir(values_dir):
						realPath = os.path.join(values_dir, f)
						# print("real path:",realPath)
						if os.path.isfile(realPath) and (f.endswith("strings.xml") or f.endswith("string.xml")):
							reader = StrResXml(realPath)
							xmlReaders[reader.getIdentify()] = reader
					# print("xmlReaders:",xmlReaders)
					#need add to defaut string reader
					needAddToDefault = {}
					for key, values in self.needTranslateStrings.items():
						if len(values) <= 0 :
							continue
						# print("get key:",key)
						xmlReader = xmlReaders.get(key)
						# print("")
						needSave = False
						if xmlReader is not None:
							elseValues = []
							for value in values:
								trans_str = excelReader.get_res_str(lang_obj.code, value)
								self.logger("translate file:{2} [{0}={1}] ".format(value,trans_str,key))
								#insert or update translate in same file name reader
								xmlReader.insert_or_update_res_node(value,trans_str)
								needSave = True
								pass
						else:
							#add to default string reader
							needAddToDefault[key] = values
							self.logger("this keys will add translate to default xml:",values)

						if needSave:
							xmlReader.save()
					if len(needAddToDefault) > 0 :
						print("something will insert to short name string xml")
						keyLen = 0
						targetKey = None
						# get short xml name file
						for readerKey in xmlReaders.keys():
							if keyLen == 0:
								keyLen = len(readerKey)
								targetKey = readerKey;
							if len(readerKey) < keyLen :
								targetKey = readerKey
								keyLen = len(readerKey)

						self.logger("insert or update untrasnlate in correct file to default file:",targetKey)

						xmlReader = xmlReaders[targetKey]
						needSave = False
						for key,values in needAddToDefault.items():
							#insert to default xml in this language.
							for value in values:
								trans_str = excelReader.get_res_str(lang_obj.code, value)
								self.logger("translate file:{2} [{0}={1}]".format(value,trans_str,key))
								#insert or update translate in same file name reader
								xmlReader.insert_or_update_res_node(value,trans_str)
								needSave = True
							pass
						if needSave:
							xmlReader.save()

					self.logger("completion translate language:",suffix[1:])
