from ErrorAnalysis import ErrAnaFormatter
from SigFigParser import SigFigFormatter
import sys

SigFigFormatter(ErrAnaFormatter(sys.argv[1]))
