#setuptools_kaitai
import sys, os, git
from pathlib import Path
from urllib3.util import Url, parse_url

from .defaults import *

def getKSCRoot():
	return Path(os.getenv("KAITAI_STRUCT_ROOT", default=Path(".") / compilerName))

class KSCDirs:
	def __init__(self, subDirsNames):
		self.root=getKSCRoot()
		self.subDirsNames=subDirsNames
	
	def __getattr__(self, key):
		return self.root / self.subDirsNames[key]
	
	def __hasattr__(self, key):
		return key in self.subDirsNames

kscDirs=KSCDirs(subDirsNames)

def searchKaitaiJavaLib():
	return next(kscDirs.lib.glob(compilerPackageName+"*.jar"))


osBinariesNamesTable={
	"nt": lambda : kscDirs.bin / (compilerName+".bat"),
	"posix": lambda : kscDirs.bin / compilerName,
	"java": searchKaitaiJavaLib
}

def findKaitaiCommand():
	return Path(osBinariesNamesTable[os.name]())

def empty(o, k):
	return k not in o or not o[k]

def upgradeLibrary(localPath, gitUri, refspec=None, progressCallback=None):
	"""Upgrades a library of Kaitai Struct formats"""
	if progressCallback is None:
		progressCallback=lambda x: None
	
	localPath=Path(localPath).absolute()
	r=None
	actName=""
	if not (localPath.exists() and localPath.is_dir()):
		actName="Clon"
		r=git.Repo.init(str(localPath)) # git.Repo.clone disallows to specify a dir, so we workaround with init + pull
	else:
		actName="Pull"
		r=git.Repo(str(localPath))
	progressCallback(actName+"ing "+gitUri+" to " + str(localPath) + " ...")
	#progress=print
	#A function (callable) that is called with the progress information.
	#Signature: ``progress(op_code, cur_count, max_count=None, message='')``.
	gargs=[gitUri]
	if refspec:
		gargs.append(refspec)
		r.git.checkout(refspec, B=True)
	gkwargs={
		"depth":1,
		"force":True,
		"update-shallow":True,
		#"verify-signatures":True,
		#"ff":True,
		#"ff-only":True,
		"progress":True,
		"verbose":True
	}
	r.git.pull(*gargs, **gkwargs)
	progressCallback("\b"+actName+"ed")
