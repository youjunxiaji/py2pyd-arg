'''
Author: gu lei
Date: 2023-01-20 13:52:06
LastEditTime: 2023-09-26 10:43:03
LastEditors: gu lei
'''
import os
import time
from loguru import logger
from .single_py2pyd import py2pyd

class FileConversion:

    def __init__(self) -> None:
        self.initpy = None
        self.success_count = 0
        self.fail_count = 0

    def get_all_file(self, path, need_remove: bool):  # 遍历此目录下的所有py文件，包含子目录里的py
        for root, dirs, files in os.walk(path):
            if "__init__.py" in files:
                self.process_init_py(root)
                files.remove("__init__.py")
            for name in files:
                if name.endswith(".py"):
                    file_path = os.path.join(root, name)
                    success = py2pyd(file_path)
                    if success:
                        self.success_count += 1
                        if need_remove:
                            os.remove(file_path)
                    else:
                        self.fail_count += 1
            if self.initpy:
                self.process_init_py(root)
        
        logger.info(f"处理完成！成功: {self.success_count} 个文件，失败: {self.fail_count} 个文件")
        return self.success_count > 0 and self.fail_count == 0

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
