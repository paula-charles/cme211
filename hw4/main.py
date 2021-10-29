import sys

import truss

if len(sys.argv) < 3:
    print('Usage:')
    print('    python3 main.py [joints file] [beams file] [optional plot output file]')
    sys.exit(0)

joints_file = sys.argv[1]
beams_file = sys.argv[2]

if len(sys.argv) == 4:
    output_plot = sys.argv[3]
else:
    output_plot = None

t = truss.Truss(joints_file,beams_file,output_plot)
print(t)
