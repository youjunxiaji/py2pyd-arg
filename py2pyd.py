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
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

__version__ = '0.2.0'

console = Console()

def check_dependencies():
    """检查必要的依赖是否已安装"""
    try:
        import Cython
        return True
    except ImportError:
        console.print("❌ [bold red]缺少必要的依赖: Cython[/bold red]")
        console.print("   请先安装依赖: pip install cython")
        return False

from module.single_py2pyd import py2pyd
from module.fileConversion import FileConversion

def process_files(files, need_remove=False, desc="转换进度"):
    """处理文件列表并显示进度条"""
    success_count = 0
    fail_count = 0
    failed_files = []
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:
        task = progress.add_task(desc, total=len(files))
        
        for file_path in files:
            success = py2pyd(file_path)
            if success:
                success_count += 1
                if need_remove:
                    os.remove(file_path)
            else:
                fail_count += 1
                failed_files.append(file_path)
            progress.update(task, advance=1)
    
    return success_count, fail_count, failed_files

def main():
    parser = argparse.ArgumentParser(
        description="将Python文件转换为pyd/so文件",
        epilog="示例:\n"
                "  py2pyd file.py              转换单个文件\n"
                "  py2pyd folder/              转换目录下的文件\n"
                "  py2pyd -r folder/           递归转换目录\n"
                "  py2pyd --remove file.py     转换后删除原文件",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("path", nargs='?', help="要转换的Python文件或目录路径")
    parser.add_argument("-r", "--recursive", action="store_true", help="递归处理目录")
    parser.add_argument("--remove", action="store_true", help="转换后删除原始.py文件")
    parser.add_argument("-v", "--version", action="version", version=f"py2pyd {__version__}")
    
    args = parser.parse_args()
    
    # 如果没有提供路径参数，显示帮助信息
    if not args.path:
        parser.print_help()
        sys.exit(0)
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 删除确认
    if args.remove:
        confirm = input("⚠️  警告: --remove 选项将会删除所有py源文件，是否继续? (y/n): ")
        if confirm.lower() != 'y':
            console.print("操作已取消")
            sys.exit(0)
    
    path = args.path
    
    if not os.path.exists(path):
        console.print(f"❌ [bold red]路径不存在: {path}[/bold red]")
        sys.exit(1)
    
    success_count = 0
    fail_count = 0
    failed_files = []
    
    if os.path.isfile(path):
        # 处理单个文件
        if not path.endswith(".py"):
            console.print(f"❌ [bold red]不是Python文件: {path}[/bold red]")
            sys.exit(1)
        console.print(f"📄 处理文件: [cyan]{path}[/cyan]")
        success_count, fail_count, failed_files = process_files([path], args.remove)
        
    elif os.path.isdir(path):
        # 处理目录
        if args.recursive:
            console.print(f"📁 递归处理目录: [cyan]{path}[/cyan]")
            converter = FileConversion()
            success = converter.get_all_file(path, args.remove)
            if success:
                console.print("\n🎉 [bold green]全部转换成功！[/bold green]")
            else:
                console.print("\n❌ [bold red]处理完成，但有部分文件转换失败！[/bold red]")
            sys.exit(0 if success else 1)
        else:
            # 仅处理当前目录下的.py文件
            console.print(f"📁 处理目录: [cyan]{path}[/cyan]")
            
            # 收集所有 .py 文件
            py_files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".py")]
            
            if not py_files:
                console.print("⚠️  [yellow]目录中没有找到 .py 文件[/yellow]")
                sys.exit(0)
            
            success_count, fail_count, failed_files = process_files(py_files, args.remove)
    
    # 显示结果
    console.print()
    if fail_count == 0:
        console.print(f"✅ [bold green]处理完成！成功: {success_count} 个文件[/bold green]")
    else:
        console.print(f"⚠️  [yellow]处理完成！成功: {success_count} 个文件，失败: {fail_count} 个文件[/yellow]")
        console.print("[red]失败的文件:[/red]")
        for f in failed_files:
            console.print(f"   - {f}")
    
    if fail_count == 0:
        console.print("\n🎉 [bold green]全部转换成功！[/bold green]")
        sys.exit(0)
    else:
        console.print("\n❌ [bold red]处理完成，但有部分文件转换失败！[/bold red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
