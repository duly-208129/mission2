import io
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_requirements
stream = io.StringIO()
result = unittest.TextTestRunner(stream=stream, verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(test_requirements))
Path(__file__).with_name('requirements-results.txt').write_text(stream.getvalue(), encoding='utf-8')
print(stream.getvalue())
sys.exit(not result.wasSuccessful())
