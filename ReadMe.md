kaitaiStructCompile.py [![Unlicensed work](https://raw.githubusercontent.com/unlicense/unlicense.org/master/static/favicon.png)](https://unlicense.org/)
===============
[![PyPi Status](https://img.shields.io/pypi/v/kaitaiStructCompile.py.svg)](https://pypi.python.org/pypi/kaitaiStructCompile.py)
[![TravisCI Build Status](https://travis-ci.org/KOLANICH/kaitaiStructCompile.py.svg?branch=master)](https://travis-ci.org/KOLANICH/kaitaiStructCompile.py)
[![Coveralls Coverage](https://img.shields.io/coveralls/KOLANICH/kaitaiStructCompile.py.svg)](https://coveralls.io/r/KOLANICH/kaitaiStructCompile.py)
[![Libraries.io Status](https://img.shields.io/librariesio/github/KOLANICH/kaitaiStructCompile.py.svg)](https://libraries.io/github/KOLANICH/kaitaiStructCompile.py)

This is a tool automating compilation Kaitai Struct ```*.ksy``` files into python ones.

Prerequisites
-------------
* Kaitai Struct compiler must be unpacked somewhere and all its prerequisites like JRE must be installed.
* Path to Kaitai Struct compiler root dir (the one containing `lib`, `bin` and `formats`) must be exposed as ```KAITAI_STRUCT_ROOT```

Low level
---------

```python
from kaitaiStructCompile import compile
compile("./ksyFilePath.ksy", "./outputDir", additionalFlags=[
	#you can expose additional params here
])
```

High level
----------
Since we usually need this in the process of building python libraries using Kaitai Struct definitions, this tool is contains an addon to ```setuptools``` allowing you to just specify the files you need to compile in a declarative way.

Just an add a property ```kaitai``` into the dict. It is a dict specified and documented with [the JSON Schema](./kaitaiStructCompile/config.schema.json), so read it carefully.

Here a piece from one project with comments follows:

```python
from pathlib import Path
formatsPath=str(Path(__file__).parent / "kaitai_struct_formats") # since the format is in the kaitai_struct_formats repo, we just clone it, but we need its path to show the compiler where the ksy file is. So we put the directory of formats in the current directory.
cfg["kaitai"]={
	"outputDir": "SpecprParser", # the directory we will put the generated file to
	"inputDir": formatsPath, # the directory we take KSYs from
	"formatsRepo": { # we need to get the repo of formats, https://github.com/kaitai-io/kaitai_struct_formats
		"localPath" : formatsPath, # Where the repo will be downloaded and from which location the compiler will use it.
		"update": True # We need the freshest version to be downloaded from GitHub. We don't need the snapshot shipped with compiler!
	},
	"formats":{ # here we declare our targets. The key is the resulting file name. The value is the descriptor.
		"specpr.py": {
			"path":"scientific/spectroscopy/specpr.ksy", # the path of the spec within 
			"postprocess":["permissiveDecoding"] # Enumerate here the names of post-processing steps you need. The default ones are in toolbox file. You can also add the own ones by creating in the main scope the mapping name => function.
		}
	}
}

setup(use_scm_version = True, **cfg)
```
