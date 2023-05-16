from kbc_transformation.transformation import Transformation
import sys
import traceback

try:
    app = Transformation('/data/')
    app.execute()
except ValueError as err:
    print(err, file=sys.stderr)
    sys.exit(1)
except Exception as err:
    print(err, file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    sys.exit(2)
