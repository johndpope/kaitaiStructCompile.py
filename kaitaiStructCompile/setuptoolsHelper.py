#setuptools_kaitai
import os
from pathlib import Path
from urllib3.util import Url

from .utils import *
from . import compile, postprocessFile

from .validator import validator, schema

from .toolkit import postprocessers

def empty(o, k):
	return k not in o or not o[k]

def prepareFdir(fdir):
	if empty(fdir, "update"):
		fdir["update"]=schema["definitions"]["formatsRepo"]["properties"]["update"]["default"]
	
	if empty(fdir, "git"):
		fdir["git"]=schema["definitions"]["formatsRepo"]["properties"]["git"]["default"]
	
	if empty(fdir, "refspec"):
		fdir["refspec"]=schema["definitions"]["formatsRepo"]["properties"]["refspec"]["default"]
	
	if empty(fdir, "localPath"):
		if fdir["update"]:
			localDirName=os.path.basename(fdir["git"])
			a=os.path.splitext(localDirName)
			if len(a)>1 and a[-1]==".git":
				localDirName=a[0]
			
			fdir["localPath"]=Path(".") / localDirName
		else:
			fdir["localPath"]=None

def prepareCfg(cfg):
	if empty(cfg, "postprocessers"):
		cfg["postprocessers"]=type(postprocessers)(postprocessers)
	if empty(cfg, "compilerExecutable"):
		cfg["compilerExecutable"]=findKaitaiCommand()
	if empty(cfg, "search"):
		cfg["search"]=schema["properties"]["search"]["default"]
	if empty(cfg, "flags"):
		cfg["flags"]=schema["definitions"]["compilationFlags"]["default"]
	
	validator.check_schema(cfg)
	validator.validate(cfg)
	
	prepareFdir(cfg["formatsRepo"])
	
	cfg["inputDir"]=Path(cfg["inputDir"])
	if empty(cfg, "outputDir"):
		cfg["outputDir"]=cfg["inputDir"]
	cfg["outputDir"]=Path(cfg["outputDir"])
	
	if cfg["search"]:
		for file in cfg["inputDir"].glob("*.ksy"):
			cfg["formats"][cfg["outputDir"] / file.parent.relative_to(cfg["inputDir"]) / (file.stem+".py")]={"path": file}
	
	newFormats=type(cfg["formats"])(cfg["formats"])
	
	for target, descriptor in cfg["formats"].items():
		if not isinstance(target, Path):
			del(newFormats[target])
			newFormats[cfg["outputDir"]/target]=descriptor
	cfg["formats"]=newFormats
	
	for target, descriptor in cfg["formats"].items():
		if not isinstance(descriptor["path"], Path):
			cfg["formats"][target]["path"]=cfg["inputDir"]/descriptor["path"]
	
	validator.check_schema(cfg)
	validator.validate(cfg)

def kaitaiHelper(dist, keyword, cfg:dict):
	prepareCfg(cfg)
	
	if cfg["formatsRepo"]["update"]:
		upgradeLibrary(cfg["formatsRepo"]["localPath"], cfg["formatsRepo"]["git"], cfg["formatsRepo"]["refspec"], print)
	
	for compilationResultFilePath, targetDescr in cfg["formats"].items():
		flags=type(cfg["flags"])(cfg["flags"])
		if "flags" in targetDescr:
			flags.extend(targetDescr["flags"])
		
		print("Compiling "+str(targetDescr["path"])+" into "+str(compilationResultFilePath)+" ...")
		
		print(compile(
			targetDescr["path"], cfg["outputDir"],
			progressCallback=print,
			compilerExecutable=cfg["compilerExecutable"],
			additionalFlags=flags
		))
		
		print("Postprocessing "+str(compilationResultFilePath)+" ...")
		
		if "postprocess" in targetDescr:
			postprocessFile(
				compilationResultFilePath,
				(cfg["postprocessers"][funcName] for funcName in targetDescr["postprocess"])
			)
			
