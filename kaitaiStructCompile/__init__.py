#setuptools_kaitai
import sys, os, io, subprocess
from pathlib import Path
from .utils import *
from .KaitaiCompilerException import KaitaiCompilerException
from .compile.cmdline import compile

#todo: create a version for jithon using KSC as java library
#todo: consider usage ksc as java library in cpython and pypy

def postprocessFile(path:Path, postprocessors:list):
	path=Path(path)
	fileText=None
	with path.open("rt", encoding="utf-8") as f:
		fileText=f.read()

	for postprocessor in postprocessors:
		fileText=postprocessor(fileText)

	with path.open("wt", encoding="utf-8") as f:
		f.write(fileText)