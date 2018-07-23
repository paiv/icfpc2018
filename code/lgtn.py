import glob
import nmms
import numpy as np
import os


TARGETDIR='../batch1'


for model_fn in glob.glob('../spec/problemsL/*.mdl'):
    basename = os.path.basename(model_fn)[:-8]
    trace_fn = '../spec/dfltTracesL/{}.nbt'.format(basename)
    target_fn = '{}/{}.nbt'.format(TARGETDIR, basename)
    log(model_fn)
    model = nmms.read_model(model_fn)
    trace = nmms.read_trace(trace_fn)
    score, m = nmms.score_trace(model, trace)
    res = nmms.solver1.solve(model)
    try:
        x, t = nmms.score_trace(model, res)
        if x <= score and np.all(m == t):
            nmms.write_trace(target_fn, res)
            continue
        else:
            log('  ** discarded')
    except Exception as e:
        log(e)

    nmms.write_trace(target_fn, trace)
