from multiprocessing import cpu_count

from fabric.api import lcd, local, task, env

from utils.files import md5_file, expand_tree
from utils.config import get_conf

from utils.jobs.runners import sync_runner, async_process_runner, async_thread_runner
from utils.jobs.runners import runner as base_runner
from utils.jobs.dependency import check_dependency, check_hashed_dependency, dump_file_hashes

env.FORCE = False
@task
def force():
    "Sets a flag that forces rebuilds of all generated and processed content."

    env.FORCE = True

env.PARALLEL = True
@task
def serial():
    "Sets a flag that removes parallelism from the build process."

    env.PARALLEL = False

env.POOL = None
@task
def pool(value):
    "Manually control the size of the worker pool."

    env.POOL = int(value)

@task
def make(target):
    "Build a make target, indirectly."

    conf = get_conf()

    with lcd(conf.paths.projectroot):
        if isinstance(target, list):
            target_str = make + ' '.join([target])
        elif isinstance(target, basestring):
            target_str = ' '.join(['make', target])

        local(target_str)

############### Task Running Framework ###############

def runner(jobs, pool=None, parallel='process', force=False, retval='count'):
    if pool is None:
        pool = cpu_count()

    if env.FORCE is True:
        force = True
    if env.PARALLEL is False or pool == 1:
        parallel = False

    return base_runner(jobs, pool, parallel, force, retval)
