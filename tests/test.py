#!/usr/bin/env python3
import sys
from pathlib import Path
import unittest
from collections import OrderedDict

testsDir=Path(__file__).parent.absolute()
parentDir=testsDir.parent.absolute()
sys.path.insert(0, str(parentDir))

from kaitaiStructCompile.setuptoolsHelper import kaitaiHelper
from kaitaiStructCompile.utils import kscDirs


class Test(unittest.TestCase):
	def testKaitai_keyword(self):
		testCfg={
			"kaitai":{
				"formats":{
					"test.py": {"path":"test.ksy"},
					#"postprocess":["permissiveDecoding"], #fucking jsonschema is broken
					#"flags": ["--ksc-json-output"] #fucking jsonschema is broken
				},
				"formatsRepo": {
					"git" : str(kscDirs.formats),
					"localPath" : testsDir / "formats",
					"update": True
				},
				"outputDir": testsDir / "output",
				"inputDir": testsDir / "ksys",
				"search": True
			}
		}
		kaitaiHelper(None, None, testCfg["kaitai"])
	
if __name__ == "__main__":
	unittest.main()
