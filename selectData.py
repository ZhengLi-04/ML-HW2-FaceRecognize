import os
import shutil
import random

# 数据路径
data_dir = "Code/dataset/Multi_Pie/HR_128"
output_dir = "Code/dataset/split_data"
train_dir = os.path.join(output_dir, "train")
test_dir = os.path.join(output_dir, "test")
test_out_dir = os.path.join(output_dir, "test_out")  # 数据集外测试集

# 参数设置
selected_subjects = 10  # 选择10个人作为训练和测试
out_subjects = 10  # 数据集外测试集人数
valid_angles_train = ["051"]  # 训练集角度
valid_angles_test = ["051", "140"]  # 测试集角度
valid_lighting = ["06", "07", "08", "15", "16", "17"]  # 有效光照条件

# 创建输出目录
os.makedirs(train_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)
os.makedirs(test_out_dir, exist_ok=True)

# 获取所有受试者编号
subject_ids = sorted(set(f.split("_")[0] for f in os.listdir(data_dir) if f.endswith(".png")))
random.seed(40)  # 固定随机种子
selected_ids = random.sample(subject_ids, selected_subjects)
remaining_ids = list(set(subject_ids) - set(selected_ids))  # 剩余人
out_ids = random.sample(remaining_ids, out_subjects) 

# 数据划分
for subject_id in selected_ids:
    subject_files = [f for f in os.listdir(data_dir) if f.startswith(subject_id) and f.endswith(".png")]
    
    # 筛选训练集图片
    train_files = [
        f for f in subject_files
        if f.split("_")[3] in valid_angles_train and f.split("_")[4] in valid_lighting
    ]
    train_files = random.sample(train_files, min(6, len(train_files)))  # 每人最多6张

    # 从剩余图片中筛选测试集图片
    remaining_files = set(subject_files) - set(train_files)  # 确保测试集不与训练集重复
    test_files = [
        f for f in remaining_files
        if f.split("_")[3] in valid_angles_test and f.split("_")[4] in valid_lighting
    ]
    test_files = random.sample(test_files, min(3, len(test_files)))  # 每人最多3张

    # 复制文件到训练集和测试集
    for f in train_files:
        src = os.path.join(data_dir, f)
        dst = os.path.join(train_dir, subject_id)
        os.makedirs(dst, exist_ok=True)
        shutil.copy(src, os.path.join(dst, f))
    
    for f in test_files:
        src = os.path.join(data_dir, f)
        dst = os.path.join(test_dir, subject_id)
        os.makedirs(dst, exist_ok=True)
        shutil.copy(src, os.path.join(dst, f))

# 数据集外测试集划分
for subject_id in out_ids:
    subject_files = [f for f in os.listdir(data_dir) if f.startswith(subject_id) and f.endswith(".png")]
    
    # 筛选测试集图片
    test_out_files = [
        f for f in subject_files
        if f.split("_")[3] in valid_angles_test and f.split("_")[4] in valid_lighting
    ]
    test_out_files = random.sample(test_out_files, min(3, len(test_out_files)))  # 每人最多3张

    # 复制文件到数据集外测试集
    for f in test_out_files:
        src = os.path.join(data_dir, f)
        dst = os.path.join(test_out_dir, subject_id)
        os.makedirs(dst, exist_ok=True)
        shutil.copy(src, os.path.join(dst, f))

print("数据集划分完成！")