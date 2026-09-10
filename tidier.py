import os
import shutil
from pathlib import Path
from datetime import datetime

class DesktopTidier:
    """Windows 桌面自动整理工具"""
    
    def __init__(self):
        # 获取用户桌面路径
        self.desktop_path = Path.home() / "Desktop"
        
        # 定义文件类型分类
        self.file_categories = {
            "图片": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".ico", ".webp"],
            "文档": [".doc", ".docx", ".pdf", ".txt", ".xlsx", ".xls", ".ppt", ".pptx", ".odt"],
            "视频": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v"],
            "音乐": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a"],
            "压缩包": [".zip", ".rar", ".7z", ".tar", ".gz", ".iso"],
            "代码": [".py", ".js", ".java", ".cpp", ".c", ".html", ".css", ".json", ".xml", ".sql"],
            "其他": []
        }
        
    def get_file_category(self, file_path):
        """根据文件扩展名确定文件类别"""
        suffix = file_path.suffix.lower()
        
        for category, extensions in self.file_categories.items():
            if suffix in extensions:
                return category
        
        return "其他"
    
    def create_category_folders(self):
        """创建分类文件夹"""
        for category in self.file_categories.keys():
            folder_path = self.desktop_path / category
            if not folder_path.exists():
                folder_path.mkdir()
                print(f"✓ 创建文件夹: {category}")
    
    def move_file(self, file_path, destination_folder):
        """移动文件到目标文件夹"""
        try:
            dest_path = destination_folder / file_path.name
            
            # 如果文件已存在，添加时间戳避免覆盖
            if dest_path.exists():
                name, suffix = file_path.stem, file_path.suffix
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                dest_path = destination_folder / f"{name}_{timestamp}{suffix}"
            
            shutil.move(str(file_path), str(dest_path))
            print(f"  移动: {file_path.name} → {destination_folder.name}/")
            return True
        except Exception as e:
            print(f"  ✗ 错误: 无法移动 {file_path.name}: {str(e)}")
            return False
    
    def tidy_desktop(self):
        """整理桌面"""
        if not self.desktop_path.exists():
            print("✗ 错误: 找不到桌面路径")
            return
        
        print(f"开始整理桌面: {self.desktop_path}")
        print("-" * 50)
        
        # 创建分类文件夹
        self.create_category_folders()
        print()
        
        # 获取桌面上的所有文件
        files_moved = 0
        folders_skipped = 0
        
        for item in self.desktop_path.iterdir():
            # 跳过文件夹和系统文件
            if item.is_dir():
                # 不移动已有的分类文件夹
                if item.name not in self.file_categories:
                    print(f"⊘ 跳过文件夹: {item.name}")
                    folders_skipped += 1
                continue
            
            # 跳过系统文件
            if item.name.startswith("."):
                continue
            
            # 确定文件类别
            category = self.get_file_category(item)
            destination_folder = self.desktop_path / category
            
            # 移动文件
            if self.move_file(item, destination_folder):
                files_moved += 1
        
        print()
        print("-" * 50)
        print(f"整理完成！")
        print(f"  ✓ 已移动文件: {files_moved} 个")
        print(f"  ⊘ 跳过文件夹: {folders_skipped} 个")

def main():
    """主程序"""
    print("=" * 50)
    print("     Windows 桌面自动整理工具")
    print("=" * 50)
    print()
    
    tidier = DesktopTidier()
    
    try:
        tidier.tidy_desktop()
        print("\n✓ 桌面整理成功！")
    except Exception as e:
        print(f"\n✗ 发生错误: {str(e)}")

if __name__ == "__main__":
    main()
