# py2pyd - Python转pyd/so工具

将Python文件(.py)转换为编译后的Python扩展模块(.pyd或.so)，使用Cython进行编译。

## 功能特点

- 支持单个Python文件的转换
- 支持目录批量转换
- 支持递归处理子目录
- 转换后可选择是否删除原始Python文件（交互式确认）
- 保留`__init__.py`文件内容处理
- 自动检测依赖并提供错误处理
- 针对不同操作系统自动选择正确的扩展名（Windows为.pyd，Linux/macOS为.so）
- 编译后保留带 ABI 标签的原始文件名（如 `module.cpython-311-darwin.so`）
- 美观的进度条显示

## 安装

```bash
pip install gl-py2pyd
```

### 系统要求

你的系统需要有合适的C/C++编译器：
- **Windows**: 需要安装 Visual C++ Build Tools
- **Linux**: 需要安装 GCC
- **macOS**: 需要安装 XCode 命令行工具（`xcode-select --install`）

## 使用方法

### 命令行使用

```bash
# 转换单个文件
py2pyd file.py

# 转换目录下所有Python文件
py2pyd folder/

# 递归转换目录及其子目录中的所有Python文件
py2pyd -r folder/

# 转换后删除原始Python文件（会弹出交互式确认菜单）
py2pyd -d file.py

# 删除且跳过确认提示（适用于 CI/CD 或脚本自动化）
py2pyd -d --no-confirm file.py

# 组合使用
py2pyd -r -d folder/

# 查看版本
py2pyd -v

# 查看帮助
py2pyd -h
```

### 输出示例

```
📄 处理文件: test.py
  转换进度 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%

✅ 处理完成！成功: 1 个文件

🎉 全部转换成功！
```

### 关于编译后的文件名

编译后的文件会保留带有 Python 版本和平台信息的 ABI 标签，例如：

- `module.cpython-311-darwin.so`（macOS, Python 3.11）
- `module.cpython-311-x86_64-linux-gnu.so`（Linux, Python 3.11）
- `module.cp311-win_amd64.pyd`（Windows, Python 3.11）

> **注意**: 编译后的扩展模块只能在对应的 Python 版本上使用。例如用 Python 3.11 编译的模块无法在 Python 3.10 或 3.12 上加载。

### 作为模块导入

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

1. **缺少Cython**: 运行前会检查Cython是否已安装，若未安装则会提示安装
2. **编译失败**: 可能是缺少编译器或者Python文件内容有问题

## 优化的编译选项

本工具针对不同操作系统和环境进行了编译选项优化：

1. **设置语言级别**: 显式设置Cython的`language_level`为3，避免语言级别警告
2. **禁止无用代码警告**: 添加适当的编译选项(`-Wno-unreachable-code`)以禁止Cython生成的C代码中的不可达代码警告
3. **修复Conda/Miniconda链接警告**: 在Conda环境中自动调整链接选项，避免重复的rpath警告

## 注意事项

- 确保已安装Cython和适当的编译器
- 转换后的so/pyd文件会保留在原始Python文件的相同目录中
- 在Windows系统上生成.pyd文件，在Linux/macOS上生成.so文件
- 编译后的模块绑定特定 Python 版本，不同版本间不兼容
- 对于复杂的Python项目，可能需要额外的编译选项

## License

MIT License
