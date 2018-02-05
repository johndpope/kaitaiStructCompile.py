import sys, os, io, subprocess
from pathlib import Path
from ..utils import *
from ..KaitaiCompilerException import KaitaiCompilerException

def compile(sourceFilePath:str, destDir:str, progressCallback=None, compilerExecutable=None, additionalFlags:list=None):
	sourceFilePath=Path(sourceFilePath).absolute()
	destDir=Path(destDir).absolute()
	compilerExecutable=Path(compilerExecutable).absolute()
	
	if not sourceFilePath.exists():
		raise KaitaiCompilerException("Source file "+str(sourceFilePath)+" doesn't exist")
	if not compilerExecutable.exists():
		raise KaitaiCompilerException("Compiler executable "+str(compilerExecutable)+" doesn't exist")
	
	return compile_(str(sourceFilePath), str(destDir), progressCallback, str(compilerExecutable), additionalFlags)

def compile_(fileAbsPath:str, destDir:str, progressCallback, compilerExecutable, additionalFlags:list):
	"""Compiles KS package with kaitai-struct-compiler"""
	
	if progressCallback is None:
		progressCallback = lambda x: None
		#progressCallback = print
	
	params=[
		compilerExecutable,
		#"--ksc-json-output",
		"--target", "python",
		"--outdir", destDir
	]
	
	if additionalFlags:
		params.extend(additionalFlags)
	
	params.append(fileAbsPath)
	
	with subprocess.Popen(
		params,
		shell=True,
		stdout=subprocess.PIPE, stderr=subprocess.STDOUT
	) as proc:
		with io.TextIOWrapper(proc.stdout) as stdoutPipe:
			msg=stdoutPipe.read()
		proc.wait()
		if proc.returncode or msg.find("Exception in thread")>-1:
			raise KaitaiCompilerException(msg)
		else:
			return msg