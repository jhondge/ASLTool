#!/usr/bin/python

__author__ = "Jackson"

from tkinter import *
from tkinter.filedialog import askopenfilename

from tkinter.filedialog import askdirectory

from stringtranslator import *

class Application:
	"""docstring for Application"""

	def callback(self,*values):
		self.output.insert(END,"\n")
		for value in values:
			self.output.insert(END,value)
		pass
	def loadSettingCallback(self,value):
		count = len(self.modules)
		if count == 0:
			#insert description label
			self.libraryDesc = Label(self.master,text="Choose libraries which need to translate:")
			self.libraryDesc.grid(row=3,column=1,columnspan=3,padx=5,sticky=W)

		var = StringVar()

		cb = Checkbutton(self.master,text=os.path.basename(value),variable=var,onvalue=value,offvalue="")
		
		targetRow = 4 + (count // 3)
		targetColumn = ( count % 3 ) + 1
		print("targetRow%d,targetColumn:%d",targetRow,targetColumn)
		cb.grid(row=targetRow,column=targetColumn,sticky=W,padx=5)
		cb.select()

		self.modules.append({"view":cb,"value":var})

		self.beginButton.grid(row=(targetRow+1),column=1,columnspan=3,pady=10)

		self.output.grid(row=(targetRow + 2),column=1,columnspan=3)

	def __init__(self, master):
		self.master = master
		self.frame = Frame(master,bg="#f00")
		self.frame.grid(row=0,column=0)
		self.setupViews(master)
		#store dict list {"view":view,"value":var}
		self.modules = []
		self.libraryDesc = None
		'''
		Begin process translate
		'''
		self.translator = FOStringTranslator(self.callback)

	def OpenFile(self):
		self.file = askopenfilename()
		if self.file is not None:
			self.excelInput.delete(0,END)
			self.excelInput.insert(0,self.file)
			print("open file:",self.file)
		# self.translator.setExcelPath(self.file)

	def ChooseProjectPath(self):
		self.projectPath = askdirectory()
		if self.projectPath is not None:
			self.inputText.insert(0,self.projectPath)
			print("project path:",self.projectPath)
			if self.modules is not None:
				for module in self.modules:
					module["view"].grid_forget()
					pass
			if self.libraryDesc is not None:
				self.libraryDesc.grid_forget()

			self.modules = []

			self.translator.loadLibrary(self.projectPath,self.loadSettingCallback)

	def onProcessClick(self):
		self.output.delete("1.0",END)
		self.output.insert('1.0',"Prepare translate libraries....")
		libraries = []
		for module in self.modules:
			path = module["value"].get()
			if len(path) > 0:
				libraries.append(path)
				self.callback("library->",os.path.basename(path))
				pass
		self.translator.setExcelPath(self.excelInput.get())
		self.callback("Begin translate ....")
		self.translator.doTranslate(libraries)
		self.callback("Completion translate ....")
		pass

	def setupViews(self,mainFrame):

		Label(mainFrame,text="Gradle Project Path:").grid(row=1,column=1,pady=10)


		self.inputText = Entry(mainFrame,bd=2,state="readonly")

		self.inputText.grid(row=1,column=2,pady=10)

		# self.inputText.insert(0,"/Users/Jhondge/android/AndroidStudioWorkSpace/Fotor")


		self.openPPButton = Button(mainFrame,text="Open",command=self.ChooseProjectPath)

		self.openPPButton.grid(row=1,column=3,pady=10)

		Label(mainFrame,text="Excel file path:").grid(row=2,column=1,pady=10)

		self.excelInput = Entry(mainFrame,bd=2)

		self.excelInput.grid(row=2,column=2,pady=10)

		# self.excelInput.insert(0,"/Users/Jhondge/Documents/Dev/assitant_tools/string_translator/abc.xlsx")

		self.openExcelButton = Button(mainFrame,text="Open",command=self.OpenFile)

		self.openExcelButton.grid(row=2,column=3,pady=10)

		self.beginButton = Button(mainFrame,text="Process",command=self.onProcessClick)

		self.beginButton.grid(row=3,column=1,columnspan=3,pady=10)

		self.output = Text(mainFrame)

		self.output.insert('1.0',"Watting process....")

		self.output.grid(row=4,column=1,columnspan=3)

def main():
	root = Tk()
	root.title("Robo Translate")
	app = Application(root)
	# root.geometry('600×400') 
	root.mainloop()
	# root.destroy()

if __name__ == '__main__':
	main()
