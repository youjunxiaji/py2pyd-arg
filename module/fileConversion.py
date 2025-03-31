'''
Author: gu lei
Date: 2023-01-20 13:52:06
LastEditTime: 2023-09-26 10:43:03
LastEditors: gu lei
'''
import os
import shutil
import time
import glob
import subprocess
from loguru import logger

class FileConversion:

    def __init__(self) -> None:
        self.initpy = None

    def py2pyd(self, path):
        logger.info(f"==========================================")
        logger.info(f"开始处理文件: {path}")
        logger.info(f"当前工作目录: {os.getcwd()}")
        
        # 保存原始工作目录
        original_dir = os.getcwd()
        try:
            # 转换为绝对路径
            abs_path = os.path.abspath(path)
            folder_path = os.path.dirname(abs_path)  # 文件夹路径
            file_path: str = os.path.basename(abs_path)  # 带py的文件名
            filename = file_path.split('.py')[0]  # 不带py的文件名

            logger.info(f"目标文件夹路径: {folder_path}")
            logger.info(f"文件名: {file_path}")

            # 更改工作目录
            os.chdir(folder_path)
            logger.info(f"切换后的工作目录: {os.getcwd()}")

            # 生成setup.py文件
            with open('setup.py', 'w') as f:
                f.write('from setuptools import setup\n')
                f.write('from Cython.Build import cythonize\n')
                f.write('setup(\n')
                f.write(f"name='{filename}',\n")
                f.write("ext_modules=cythonize('%s')\n" % file_path)
                f.write(")\n")

            logger.info(f"开始执行 setup.py")
            subprocess.check_call(['python', 'setup.py', 'build_ext', '--inplace'])

            pyd_name = f"{filename}.so"
            logger.info(f"目标so文件名: {pyd_name}")

            if os.path.exists(pyd_name):
                logger.info(f"删除已存在的so文件: {pyd_name}")
                os.remove(pyd_name)  # 删除老的so

            amd64_pyd = glob.glob(filename + "*.so")
            logger.info(f"找到的so文件: {amd64_pyd}")

            os.rename(amd64_pyd[0], pyd_name)  # 改名字，删除多余的cp38-win_amd64.等
            logger.info(f"重命名so文件完成")

            # 清理临时文件
            logger.info("开始清理临时文件")
            if os.path.exists('%s.c' % filename):
                os.remove('%s.c' % filename)    # 删除临时文件
            if os.path.exists('build'):
                shutil.rmtree('build')
            if os.path.exists('setup.py'):
                os.remove('setup.py')   # 删除掉生成的setup.py
            if os.path.exists('__pycache__'):
                shutil.rmtree('__pycache__')  # 删除 __pycache__文件夹
            [os.remove(i) for i in glob.glob("*.ui")]  # 删除ui文件
            logger.info("清理临时文件完成")
            logger.info(f"==========================================\n")

        finally:
            # 恢复原始工作目录
            os.chdir(original_dir)
            logger.info(f"恢复原始工作目录: {original_dir}")
            logger.info(f"==========================================\n")

    def get_all_file(self, path, need_remove: bool):  # 遍历此目录下的所有py文件，包含子目录里的py
        for root, dirs, files in os.walk(path):
            if "__init__.py" in files:
                self.process_init_py(root)
                files.remove("__init__.py")
            for name in files:
                if name.endswith(".py"):
                    file_path = os.path.join(root, name)
                    self.py2pyd(file_path)
                    if need_remove:
                        os.remove(name)
            if self.initpy:
                self.process_init_py(root)

    def process_init_py(self, path):
        init_py_path = os.path.join(path, '__init__.py')
        if self.initpy:
            with open(init_py_path, 'w', encoding='utf-8') as file:
                file.write(self.initpy)
            self.initpy = None
        else:
            with open(init_py_path, 'r', encoding='utf-8') as file:
                self.initpy = file.read()
            os.remove(init_py_path)
