from argparse import ArgumentParser
from sys import platform, exit
import subprocess
from time import sleep
import logging

try: from psutil import Process
except ImportError:
    print('''    This programm using module \'psutil\' which not included
    in standart python library, please install it before using programm''')
    exit()


def main():
    parser = ArgumentParser(
    description='''    This programm show CPU percentage usage and memory usage
    get keys \'-name\' with path and name of calling external programm, 
    key \'-t\' with intervall (in milliseconds) of polling,
     \'-log\' path and name of log file (each time log file will rewriting)''')

    parser.add_argument("-name", required=True, help="Name of calling programm (with path)")
    parser.add_argument("-t",default=1000, type=int, 
        help="Interval of checking in milliseconds, default value is 1000 ms")
    parser.add_argument("-log",default="output_log.txt", type=str, 
        help='''Optional name of file with log of working, default name is 'output_log.txt' 
    in current directory''')

    args = parser.parse_args()
    
    #logging setups
    logger = logging.getLogger('task1')
    logger.setLevel('INFO')
    task1_format = logging.Formatter(fmt='{asctime}-{levelname}-{message}',style ='{')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(task1_format)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(args.log, mode='w')
    file_handler.setFormatter(task1_format)
    logger.addHandler(file_handler)
    #end of logging setups

    subprog = subprocess.Popen(args.name, stderr=subprocess.PIPE)
    putil = Process(subprog.pid)
    if platform.lower().startswith('win') :
        logger.info(platform)
        logger.info(args.name)
        logger.info(args.log)
        logger.info(str(args.t)+'ms\n')
        while subprog.poll() is None:
            logger.info('CPU loading ' + str(putil.cpu_percent()) + '%')
            logger.info('Working Set ' + str(putil.memory_info().wset/(1024*1024))+' Mb')
            logger.info('Private Bytes ' + str(putil.memory_info().private/(1024*1024))+' Mb')
            logger.info('Open handles ' + str(putil.num_handles())+'\n')
            sleep(args.t/1000)
    elif platform.startswith('linux') or platform.lower()=='cygwin':
        logger.info(platform)
        logger.info(args.name)
        logger.info(args.log)
        logger.info(str(args.t)+'ms\n')
        while subprog.poll() is None:
            logger.info('CPU loading ' + str(putil.cpu_percent()) + '%' )
            logger.info('Resident Set Size ' + str(putil.memory_info().rss/(1024*1024))+' Mb')
            logger.info('Virtual Memory Size ' + str(putil.memory_info().vms/(1024*1024))+' Mb')
            logger.info('Descriptors open (linux) ' + str(putil.num_fds()) +'\n' )
            sleep(args.t/1000)


if __name__=="__main__":
    main()
