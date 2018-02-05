import re

permissiveDecodingRx=re.compile('\\.decode\\(u"([\\w-]+)"\\)')
def permissiveDecoding(fileText):
	return permissiveDecodingRx.sub('.decode(u"\\1", errors="ignore")', fileText)

postprocessers={
	"permissiveDecoding": permissiveDecoding
}