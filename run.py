#!/usr/bin/env python
import os
import sys

from app.ripple_app import create_app


jana_env = os.environ.get('RIPPLEENV')
if not jana_env:
    print "please set RIPPLEENV environment var"
    sys.exit(1)

ripple = create_app(jana_env)
ripple.run(host='0.0.0.0', port=5000, debug=True)
