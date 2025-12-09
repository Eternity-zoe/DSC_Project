import os

def print_tree(root_dir, prefix="", file=None):  # 明确声明 file 参数
    """
    以树形结构打印文件夹，并写入文件
    :param root_dir: 目标目录路径
    :param prefix: 递归前缀（内部使用）
    :param file: 文件句柄（用于写入txt）
    """
    # 先检查目录是否存在
    if not os.path.exists(root_dir):
        error_msg = f"错误：目录不存在 → {root_dir}"
        print(error_msg)
        if file:
            file.write(error_msg + "\n")
        return
    if not os.path.isdir(root_dir):
        error_msg = f"错误：不是文件夹 → {root_dir}"
        print(error_msg)
        if file:
            file.write(error_msg + "\n")
        return
    
    # 获取目录下的所有条目（按名称排序）
    entries = sorted(os.scandir(root_dir), key=lambda e: e.name)
    last_idx = len(entries) - 1
    
    for idx, entry in enumerate(entries):
        # 分支符号
        branch = "└── " if idx == last_idx else "├── "
        line = f"{prefix}{branch}{entry.name}"
        # 控制台打印
        print(line)
        # 写入文件（如果文件句柄存在）
        if file:
            file.write(line + "\n")
        
        # 递归处理子目录
        if entry.is_dir():
            sub_prefix = prefix + ("    " if idx == last_idx else "│   ")
            print_tree(entry.path, sub_prefix, file)  # 递归时传递 file 参数

if __name__ == "__main__":
    # ========== 配置项（按需修改） ==========
    # 目标目录（替换为你要遍历的文件夹路径）
    target_dir = r"E:\AAUniversity\Junior\Data Structure Course\DSC_Project\my_assignment_project"
    # 保存的txt文件路径（默认保存在脚本目录，命名为file_tree.txt）
    save_path = "file_tree.txt"  # 也可以指定绝对路径，如 r"D:\文件结构.txt"
    
    # ========== 执行逻辑 ==========
    # 打印标题（控制台+文件）
    title = f"文件结构树：{target_dir}\n"
    print(title)
    
    # 打开文件并写入（encoding='utf-8' 避免中文乱码）
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(title)  # 写入标题
        print_tree(target_dir, file=f)  # 写入树形结构
    
    # 提示完成
    finish_msg = f"\n✅ 文件夹结构已保存到：{os.path.abspath(save_path)}"
    print(finish_msg)