import argparse
from module.fileConversion import FileConversion

VERSION = '2.1'  # 定义版本号

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="py转pyd")
    parser.add_argument('-f', '--folder', type=str, help='需要转换的文件夹')
    parser.add_argument('-d', '--delete', action='store_true', help='删除py源文件')
    parser.add_argument('-y', '--yes', action='store_true', help='确认删除py源文件,跳过警告')
    parser.add_argument('-v', '--version', action='version', version=VERSION,help='显示版本号')  # 添加版本号参数
    args = parser.parse_args()
    
    if args.delete and not args.yes:
        confirm = input("警告: -d 选项将会删除所有py源文件,是否继续? (y/n): ")
        if confirm.lower() != 'y':
            print("操作已取消")
            exit(0)

    instance = FileConversion()
    instance.get_all_file(args.folder, need_remove=args.delete)
