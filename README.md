# easydl2paddlex-det

easydl json to paddlex voc [detection]

## 准备

使用EasyDL标注好的物体检测数据可以通过AI Studio的数据集功能导出为数据集。下载数据集到本地后，可将json格式的标签转换为对应的xml标签。

## 使用

使用如下方式进行转换：

```
python convert.py -o easydl_folder -d save_folder
```

或导入`Batch2Xmls`按下列方式进行转换：

```python
from convert import Batch2Xmls

easydl_folder = r"test\easydl_datas"
save_path = r"test\datasets"
Batch2Xmls(easydl_folder, save_path)
```

## TODO

- [x] 未标注数据生成不含object的xml标签。
- [x] 适应jpg以外的图像数据。
- [x] 适应json中不存在size，从图像读取size。
