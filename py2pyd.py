#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: gu lei
Date: 2023-01-20 13:52:06
LastEditTime: 2023-09-26 10:43:03
LastEditors: gu lei
'''
import os
import sys
import argparse
from loguru import logger

def check_dependencies():
    """检查必要的依赖是否已安装"""
    try:
        import Cython
        logger.info(f"检测到Cython版本: {Cython.__version__}")
        return True
    except ImportError:
        logger.error("缺少必要的依赖: Cython \t 请先安装依赖: pip install cython")
        return False

from module.single_py2pyd import py2pyd
from module.fileConversion import FileConversion

def main():
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
        
    parser = argparse.ArgumentParser(description="将Python文件转换为pyd/so文件")
    parser.add_argument("path", help="要转换的Python文件或目录路径")
    parser.add_argument("-r", "--recursive", action="store_true", help="递归处理目录")
    parser.add_argument("--remove", action="store_true", help="转换后删除原始.py文件")
    
    args = parser.parse_args()
    
    path = args.path
    
    if not os.path.exists(path):
        logger.error(f"路径不存在: {path}")
        sys.exit(1)
    
    success = False
    
    if os.path.isfile(path):
        # 处理单个文件
        if not path.endswith(".py"):
            logger.error(f"不是Python文件: {path}")
            sys.exit(1)
        logger.info(f"处理单个文件: {path}")
        success = py2pyd(path)
        if success and args.remove:
            logger.info(f"删除原始文件: {path}")
            os.remove(path)
    elif os.path.isdir(path):
        # 处理目录
        if args.recursive:
            logger.info(f"递归处理目录: {path}")
            converter = FileConversion()
            success = converter.get_all_file(path, args.remove)
        else:
            # 仅处理当前目录下的.py文件
            logger.info(f"处理目录: {path}")
            success_count = 0
            fail_count = 0
            for filename in os.listdir(path):
                if filename.endswith(".py"):
                    file_path = os.path.join(path, filename)
                    file_success = py2pyd(file_path)
                    if file_success:
                        success_count += 1
                        if args.remove:
                            logger.info(f"删除原始文件: {file_path}")
                            os.remove(file_path)
                    else:
                        fail_count += 1
            
            logger.info(f"处理完成！成功: {success_count} 个文件，失败: {fail_count} 个文件")
            success = success_count > 0 and fail_count == 0
    
    if success:
        logger.info("处理完成！全部转换成功！")
        sys.exit(0)
    else:
        logger.error("处理完成，但有部分文件转换失败！")
        sys.exit(1)

if __name__ == "__main__":
    main() 