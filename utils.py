from typing import Dict
import os
import os.path as osp
import json


def get_file_name(file_path: str) -> str:
    _, fullflname = os.path.split(file_path)
    return fullflname


def mkdir_p(folder_path: str) -> None:
    if not osp.exists(folder_path):
        os.mkdir(folder_path)


def read_json(json_path: str) -> Dict:
    js_dicts = dict()
    with open(json_path, "r", encoding="utf-8")as f:
        js_dicts = json.load(f)
    return js_dicts
