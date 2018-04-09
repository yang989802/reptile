from multiprocessing import Pool
import os,time,random
# 子进程要执行的代码
def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random()*3)
    end = time.time()
    print('Task %s runs %0.2f seconds'%(name,(end-start)))


if __name__=='__main__':
    print('Parent %s'%(os.getpid()))
    p = Pool(4)
    for i in range(5):
        p.apply_async(run_proc,args=(i,))
    print('waiting for all subprocesses done')
    p.close()
    p.join()
    print('All done')