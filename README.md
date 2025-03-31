# Python转pyd/so工具

这个工具用于将Python文件(.py)转换为编译后的Python扩展模块(.pyd或.so)，使用Cython进行编译。

## 功能特点

- 支持单个Python文件的转换
- 支持目录批量转换
- 支持递归处理子目录
- 转换后可选择是否删除原始Python文件
- 保留`__init__.py`文件内容处理
- 自动检测依赖并提供错误处理
- 针对不同操作系统自动选择正确的扩展名（Windows为.pyd，Linux/MacOS为.so）
- 优化编译选项，消除常见警告信息

## 安装依赖

在使用此工具前，请确保已安装以下依赖：

```bash
pip install cython loguru
```

此外，你的系统需要有合适的C/C++编译器：
- Windows: 需要安装Visual C++ Build Tools
- Linux: 需要安装GCC
- macOS: 需要安装XCode命令行工具（`xcode-select --install`）

## 使用方法

### 1. 转换单个文件

```bash
python py2pyd.py path/to/your/file.py
```

### 2. 转换目录下所有Python文件

```bash
python py2pyd.py path/to/your/directory
```

### 3. 递归转换目录及其子目录中的所有Python文件

```bash
python py2pyd.py -r path/to/your/directory
```

### 4. 转换后删除原始Python文件

```bash
python py2pyd.py --remove path/to/your/file.py
```

### 5. 全部选项组合

```bash
python py2pyd.py -r --remove path/to/your/directory
```

## 作为模块导入

你也可以在自己的Python代码中导入该模块：

```python
# 转换单个文件
from module.single_py2pyd import py2pyd
success = py2pyd('path/to/your/file.py')
if success:
    print("转换成功")
else:
    print("转换失败")

# 转换整个目录
from module.fileConversion import FileConversion
converter = FileConversion()
success = converter.get_all_file('path/to/your/directory', need_remove=False)
print(f"成功：{converter.success_count} 个文件，失败：{converter.fail_count} 个文件")
```

## 错误处理

工具会自动检测必要的依赖并提供错误信息。常见问题包括：

1. **缺少Cython**: 运行前会检查Cython是否已安装，若未安装则会提示安装。
2. **编译失败**: 如果编译失败，会提供详细错误信息，可能是缺少编译器或者Python文件内容有问题。

## 优化的编译选项

本工具针对不同操作系统和环境进行了编译选项优化：

1. **设置语言级别**: 显式设置Cython的`language_level`为3，避免语言级别警告
2. **禁止无用代码警告**: 添加适当的编译选项(`-Wno-unreachable-code`)以禁止Cython生成的C代码中的不可达代码警告
3. **修复Conda/Miniconda链接警告**: 在Conda环境中自动调整链接选项，避免重复的rpath警告

## 注意事项

- 确保已安装Cython和适当的编译器
- 转换后的so/pyd文件会保留在原始Python文件的相同目录中
- 在Windows系统上生成.pyd文件，在Linux/MacOS上生成.so文件
- 对于复杂的Python项目，可能需要额外的编译选项 