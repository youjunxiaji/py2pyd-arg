'''
Author: gu lei
Date: 2023-01-20 13:52:06
LastEditTime: 2023-09-26 10:43:03
LastEditors: gu lei
'''
import os
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from .single_py2pyd import py2pyd

console = Console()

class FileConversion:

    def __init__(self) -> None:
        self.initpy = None
        self.success_count = 0
        self.fail_count = 0
        self.failed_files = []  # 记录失败的文件

    def get_all_file(self, path, need_remove: bool):  # 遍历此目录下的所有py文件，包含子目录里的py
        # 首先收集所有需要处理的文件
        all_files = []
        init_py_dirs = []  # 记录有 __init__.py 的目录
        
        for root, dirs, files in os.walk(path):
            if "__init__.py" in files:
                init_py_dirs.append(root)
                files = [f for f in files if f != "__init__.py"]
            for name in files:
                if name.endswith(".py"):
                    all_files.append(os.path.join(root, name))
        
        if not all_files:
            console.print("⚠️  [yellow]目录中没有找到 .py 文件[/yellow]")
            return True
        
        # 使用 rich 进度条
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:
            task = progress.add_task("转换进度", total=len(all_files))
            
            for file_path in all_files:
                # 处理 __init__.py
                dir_path = os.path.dirname(file_path)
                if dir_path in init_py_dirs and self.initpy is None:
                    self.process_init_py(dir_path)
                    init_py_dirs.remove(dir_path)
                
                success = py2pyd(file_path)
                if success:
                    self.success_count += 1
                    if need_remove:
                        os.remove(file_path)
                else:
                    self.fail_count += 1
                    self.failed_files.append(file_path)
                
                # 恢复 __init__.py
                if self.initpy and dir_path not in init_py_dirs:
                    self.process_init_py(dir_path)
                
                progress.update(task, advance=1)
        
        # 显示结果
        console.print()
        if self.fail_count == 0:
            console.print(f"✅ [bold green]处理完成！成功: {self.success_count} 个文件[/bold green]")
        else:
            console.print(f"⚠️  [yellow]处理完成！成功: {self.success_count} 个文件，失败: {self.fail_count} 个文件[/yellow]")
            console.print("[red]失败的文件:[/red]")
            for f in self.failed_files:
                console.print(f"   - {f}")
        
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
