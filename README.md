# createStrm.py
 
基于Rclone生成strm文件的脚本

编辑```createStrm.py```中syncList数组

元素格式为（rclone可索引目录地址，映射到本地保存的strm文件地址，生成的strm文件的前缀）

仅索引第一层文件夹中远程存在且本地不存在的文件夹，因此如果要更新子目录的内容，先删除本地文件夹再运行脚本。

## rcloneRenameTool.py

基于Rclone的重命名工具

输入rclone可索引目录地址，会列出当前目录下所有文件，且不会索引子目录

编辑生成的txt文件并保存，会按照原始顺序修改文件名称