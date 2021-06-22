if [[ -z "$1" ]]; then
    echo "Usage: bash $0 YOUR_DATASET_ROOT"
    exit
else
    echo $0 $1
fi

echo "Download dataset"
mkdir -p $1
cd $1
echo "Download object_name_list..."
wget -q https://ocrtoc-public.oss-cn-hangzhou.aliyuncs.com/dataset/object_name_list.txt
echo "Download scene_name_list..."
wget -q https://ocrtoc-public.oss-cn-hangzhou.aliyuncs.com/dataset/scene_name_list.txt
echo "Download models..."
wget https://ocrtoc-public.oss-cn-hangzhou.aliyuncs.com/dataset/rgb_pcd_0.tar
echo "Download scenes..."
wget https://ocrtoc-public.oss-cn-hangzhou.aliyuncs.com/dataset/scenes_1-77.tar

echo "Uncompress models..."
tar -xf rgb_pcd_0.tar
echo "Uncompress scenes..."
tar -xf scenes_1-77.tar