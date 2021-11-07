"""
Написать программу, которая будет синхронизировать два каталога:
    каталог-источник и каталог-реплику.
    Задача программы – приводить содержимое каталога-реплики 
    в соответствие содержимому каталога-источника.
Требования:
    • Сихронизация должна быть односторонней: 
после завершения процесса синхронизации содержимое каталога-реплики должно в точности соответствовать содержимому каталогу-источника;
    • Синхронизация должна производиться периодически;
    • Операции создания/копирования/удаления объектов должны логироваться в файле и выводиться в консоль;
    • Пути к каталогам, интервал синхронизации и путь к файлу логирования должны задаваться параметрами командной строки при запуске программы.
"""

from argparse import ArgumentParser
import logging
import shutil
from filecmp import dircmp
from time import sleep
import os


def delete(path):
    """path could either be relative or absolute. """
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)
    elif os.path.isdir(path):
        # remove directory and all its content
        shutil.rmtree(path)
    else:
        raise ValueError(f'Path {path} is not a file or dir.')


def ucopy(src, dst):
    
    if os.path.isfile(src) or os.path.islink(src):
        shutil.copyfile(src, dst)
    elif os.path.isdir(src):
        shutil.copytree(src, dst) #copy directory and all its content
    else:
        raise ValueError(f'Path {src} or {dst} is not a file or dir.')        


def main():
    
    parser = ArgumentParser(description='''Main description''')
    parser.add_argument("--main", required=True, type=str, help="Path to main dir")
    parser.add_argument("--mirror", required=True, type=str,help="Path to mirror dir")
    parser.add_argument("-t",default=10, type=int, 
        help="Interval between sync in seconds, default value is 10 seconds")
    parser.add_argument("--log",default="task2_log.txt", type=str, 
        help='''Optional name of file with log of working, default name is 'output_log.txt' 
    in current directory''')
    
    args = parser.parse_args() #args.main, args.mirror, args.t, args.log

    #logging setups
    logger = logging.getLogger('task2')
    logger.setLevel('INFO')
    task2_format = logging.Formatter(fmt='{asctime}-{levelname}-{message}',
    style ='{', datefmt='%Y-%m-%d %H:%M:%S')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(task2_format)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(args.log, mode='w')
    file_handler.setFormatter(task2_format)
    logger.addHandler(file_handler)
    #end of logging setups

    def sync(dcmp):
        
        #sync definition inside main() because it's using logger
        
        if dcmp.funny_files:
            logger.warning(os.path(dcmp.left)+' '+os.path(dcmp.right))
            logger.warning('Next files can\'t be normally prcessed:' + str(dcmp.funny_files) )
            
        for item in dcmp.right_only:
            path=os.path.join(dcmp.right, item)
            delete(path)
            logger.info(f'{path} was removed because was n\'t in main dir')
            
        for item in dcmp.left_only+dcmp.diff_files:
            
            path1=os.path.join(dcmp.left,item)
            path2=os.path.join(dcmp.right,item)
            ucopy(path1, path2)
            if item in dcmp.left_only:
                status='copied'
            else:
                status='updated'
            logger.info(f'{path1} was {status} in {path2}')
            
        for subdir in dcmp.subdirs.values():
            sync(subdir)

    try:
        while True:
            dcmp = dircmp(args.main, args.mirror)
            sync(dcmp)
            sleep(args.t)
    
    except KeyboardInterrupt:
        logger.info("Programm was interrupted from keyboard with Ctrl+C")
        
        
if __name__=="__main__":
    main()
