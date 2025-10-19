import os
import random
import shutil

# Configura les rutes
src_images = 'images'
src_labels = 'labels'
dst_base = 'BirdsDatasetSplit'  # Nou nom per la carpeta dividida

split_ratio = 0.8  # 80% entrenament, 20% validació

# Llegeix i barreja les imatges
image_files = [f for f in os.listdir(src_images) if f.endswith(('.jpg', '.jpeg', '.png'))]
random.shuffle(image_files)

# Divideix les imatges
split_idx = int(len(image_files) * split_ratio)
train_files = image_files[:split_idx]
val_files = image_files[split_idx:]

def copy_files(file_list, subset):
    img_dst = os.path.join(dst_base, subset, 'images')
    lbl_dst = os.path.join(dst_base, subset, 'labels')
    os.makedirs(img_dst, exist_ok=True)
    os.makedirs(lbl_dst, exist_ok=True)

    for f in file_list:
        img_src_path = os.path.join(src_images, f)
        lbl_src_path = os.path.join(src_labels, f.rsplit('.', 1)[0] + '.txt')

        shutil.copy(img_src_path, img_dst)
        if os.path.exists(lbl_src_path):
            shutil.copy(lbl_src_path, lbl_dst)

# Còpia els arxius
copy_files(train_files, 'train')
copy_files(val_files, 'valid')

print(f"Divisió completada: {len(train_files)} entrenament, {len(val_files)} validació.")
