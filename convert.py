from typing import Optional, Dict, Tuple
import os
import os.path as osp
import shutil
import numpy as np
import xml.dom.minidom as minidom
import argparse
from tqdm import tqdm
from PIL import Image
from utils import get_file_name, mkdir_p, read_json


def WriteXml(xml_path: str, 
             name: str, 
             js_data: Optional[Dict] =None, 
             hw: Optional[Tuple] = None) -> None:
    doc = minidom.Document()
    root_node = doc.createElement("annotation")
    doc.appendChild(root_node)
    folder_node = doc.createElement("folder")
    folder_value = doc.createTextNode("images")
    folder_node.appendChild(folder_value)
    root_node.appendChild(folder_node)
    filename_node = doc.createElement("filename")
    filename_value = doc.createTextNode(name)
    filename_node.appendChild(filename_value)
    root_node.appendChild(filename_node)
    size_node = doc.createElement("size")
    if js_data is not None:
        if hw is not None:
            H, W = hw
        elif "size" in js_data["labels"][0].keys():
            W = js_data["labels"][0]["size"]["width"]
            H = js_data["labels"][0]["size"]["height"]
        else:
            return
        for item, value in zip(["width", "height", "depth"], [W, H, 3]):
            elem = doc.createElement(item)
            elem.appendChild(doc.createTextNode(str(value)))
            size_node.appendChild(elem)
        root_node.appendChild(size_node)
        seg_node = doc.createElement("segmented")
        seg_node.appendChild(doc.createTextNode(str(0)))
        root_node.appendChild(seg_node)
        # object
        for lab in js_data["labels"]:
            obj_node = doc.createElement("object")
            name_node = doc.createElement("name")
            name_node.appendChild(doc.createTextNode(lab["name"]))
            obj_node.appendChild(name_node)
            pose_node = doc.createElement("pose")
            pose_node.appendChild(doc.createTextNode("Unspecified"))
            obj_node.appendChild(pose_node)
            trun_node = doc.createElement("truncated")
            trun_node.appendChild(doc.createTextNode(str(0)))
            obj_node.appendChild(trun_node)
            trun_node = doc.createElement("difficult")
            trun_node.appendChild(doc.createTextNode(str(0)))
            obj_node.appendChild(trun_node)
            bndbox_node = doc.createElement("bndbox")
            for item, value in zip(
                ["xmin", "ymin", "xmax", "ymax"], 
                [lab["x1"], lab["y1"], lab["x2"], lab["y2"]]):
                elem = doc.createElement(item)
                elem.appendChild(doc.createTextNode(str(value)))
                bndbox_node.appendChild(elem)
            obj_node.appendChild(bndbox_node)
            root_node.appendChild(obj_node)
    elif hw is not None:
        H, W = hw
        for item, value in zip(["width", "height", "depth"], [W, H, 3]):
            elem = doc.createElement(item)
            elem.appendChild(doc.createTextNode(str(value)))
            size_node.appendChild(elem)
        root_node.appendChild(size_node)
    else:
        return
    # write xml
    with open(xml_path, "w", encoding="utf-8") as f:
        doc.writexml(f, indent="", addindent="\t", newl="\n", encoding="utf-8")


def Json2Xml(json_path: str, save_path: str, img_path: str) -> None:
    if not osp.exists(json_path):
        return
    js_data = read_json(json_path)
    img_name = get_file_name(img_path)
    img = np.asarray(Image.open(img_path))
    h, w = img.shape[:2]
    WriteXml(save_path, img_name, js_data, (h, w))


def Batch2Xmls(easydl_folder: str, save_path: str) -> None:
    img_save_folder = osp.join(save_path, "images")
    xml_save_folder = osp.join(save_path, "annotations")
    mkdir_p(save_path)
    mkdir_p(img_save_folder)
    mkdir_p(xml_save_folder)
    names = os.listdir(easydl_folder)
    for name in tqdm(names):
        file_name, file_ext = name.split(".")
        if file_ext != "json":
            img_path = osp.join(easydl_folder, name)
            save_img_path = osp.join(img_save_folder, name)
            shutil.copy(img_path, save_img_path)
            json_path = osp.join(easydl_folder, (file_name + ".json"))
            xml_path = osp.join(xml_save_folder, (file_name + ".xml"))
            if osp.exists(json_path):
                Json2Xml(json_path, xml_path, img_path)
            else:
                img = np.asarray(Image.open(img_path))
                h, w = img.shape[:2]
                WriteXml(xml_path, name, hw=(h, w))


parser = argparse.ArgumentParser(description="easydl folder and save folder")
parser.add_argument("--easydl_folder", "-o", help="easydl folder, required", required=True)
parser.add_argument("--save_folder", "-d", help="save folder, required", required=True)


if __name__ == "__main__":
    args = parser.parse_args()
    easydl_folder = args.easydl_folder
    save_folder = args.save_folder
    Batch2Xmls(easydl_folder, save_folder)
