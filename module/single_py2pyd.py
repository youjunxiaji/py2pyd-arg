'''
Author: gu lei
Date: 2023-01-20 13:52:06
LastEditTime: 2023-09-26 10:43:03
LastEditors: gu lei
'''
import os
import shutil
import glob
import subprocess
import sys
from loguru import logger

def py2pyd(path):
    """
    将单个Python文件转换为pyd/so文件
    
    Args:
        path: Python文件路径
    """
    logger.info(f"==========================================")
    logger.info(f"开始处理文件: {path}")
    logger.info(f"当前工作目录: {os.getcwd()}")
    
    # 保存原始工作目录
    original_dir = os.getcwd()
    try:
        # 检查Cython是否已安装
        try:
            import Cython
        except ImportError:
            logger.error("缺少必要的依赖: Cython")
            logger.info("请先安装依赖: pip install cython")
            return False
            
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

        # 根据系统配置编译参数和链接参数
        extra_compile_args = []
        extra_link_args = []
        
        if sys.platform == 'darwin':  # macOS
            extra_compile_args = ['-Wno-unreachable-code']
            # 对于Conda环境，修复重复rpath警告
            if 'conda' in sys.prefix or 'miniconda' in sys.prefix:
                extra_link_args = ['-Wl,-rpath,@loader_path/../lib']
        elif sys.platform.startswith('linux'):  # Linux
            extra_compile_args = ['-Wno-unreachable-code']
            # 对于Conda环境，修复重复rpath警告
            if 'conda' in sys.prefix or 'miniconda' in sys.prefix:
                extra_link_args = ['-Wl,-rpath,$ORIGIN/../lib']
        # Windows不需要这些参数

        # 生成setup.py文件
        with open('setup.py', 'w') as f:
            f.write('from setuptools import setup, Extension\n')
            f.write('from Cython.Build import cythonize\n')
            f.write('import sys\n\n')
            
            # 写入编译选项
            f.write('# 配置编译参数\n')
            f.write('extra_compile_args = %s\n' % extra_compile_args)
            f.write('extra_link_args = %s\n\n' % extra_link_args)
            
            f.write('# 创建扩展模块\n')
            f.write('extensions = [\n')
            f.write('    Extension(\n')
            f.write(f"        '{filename}',\n")
            f.write(f"        ['{file_path}'],\n")
            f.write('        extra_compile_args=extra_compile_args,\n')
            f.write('        extra_link_args=extra_link_args\n')
            f.write('    )\n')
            f.write(']\n\n')
            
            f.write('setup(\n')
            f.write(f"    name='{filename}',\n")
            f.write('    ext_modules=cythonize(\n')
            f.write('        extensions,\n')
            f.write("        compiler_directives={'language_level': '3'}\n")
            f.write('    )\n')
            f.write(')\n')

        logger.info(f"开始执行 setup.py")
        try:
            subprocess.check_call(['python', 'setup.py', 'build_ext', '--inplace'])
        except subprocess.CalledProcessError as e:
            logger.error(f"执行setup.py失败: {e}")
            logger.error("请确保已正确安装Cython，并且Python环境中有适当的编译器")
            # 清理临时文件
            if os.path.exists('setup.py'):
                os.remove('setup.py')
            return False

        # 确定扩展名 (.so 或 .pyd)
        is_windows = sys.platform.startswith('win')
        extension = '.pyd' if is_windows else '.so'
        output_file = f"{filename}{extension}"
        logger.info(f"目标文件名: {output_file}")

        if os.path.exists(output_file):
            logger.info(f"删除已存在的文件: {output_file}")
            os.remove(output_file)  # 删除老的文件

        # 查找生成的扩展文件
        if is_windows:
            ext_files = glob.glob(filename + "*.pyd")
        else:
            ext_files = glob.glob(filename + "*.so")
            
        if not ext_files:
            logger.error(f"未找到编译后的文件")
            return False
            
        logger.info(f"找到的文件: {ext_files}")

        os.rename(ext_files[0], output_file)  # 改名字，删除多余的cp38-win_amd64.等
        logger.info(f"重命名文件完成")

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
        return True

    except Exception as e:
        logger.error(f"处理文件时发生错误: {e}")
        return False
    finally:
        # 恢复原始工作目录
        os.chdir(original_dir)
        logger.info(f"恢复原始工作目录: {original_dir}")
        logger.info(f"==========================================\n")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="将单个Python文件转换为pyd/so文件")
    parser.add_argument("file_path", help="要转换的Python文件路径")
    
    args = parser.parse_args()
    py2pyd(args.file_path)
