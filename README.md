# KidGym: A 2D Grid-Based Reasoning Benchmark for MLLMs

<div align="center">
<a href='https://bobo-ye.github.io/KidGym/'><img src='https://img.shields.io/badge/%F0%9F%8C%90%20Homepage-00A3FF'></a>
<a href='https://arxiv.org/abs/2603.20209'><img src='https://img.shields.io/badge/%F0%9F%93%96%20ArXiv-C71585'></a>
<a href='https://huggingface.co/spaces/BoBo-Ye/KidGym_Playground'><img src='https://img.shields.io/badge/%F0%9F%A4%97%20Playground-red'></a>
<a><img src="https://img.shields.io/github/stars/BoBo-Ye/KidGym"></a>
</div>

Drawing inspiration from the **[Wechsler Intelligence Scales](https://en.wikipedia.org/wiki/Wechsler_Intelligence_Scale_for_Children)**, a widely recognized intelligence test for children, we define 5 essential abilities required of current MLLMs: **Execution**, **Memory**, **Learning**, **Planning** and **Perception Reasoning**. To this end, we introduce KidGym, a 2D grid-based benchmark for evaluating these five core capabilities.

<img src="./static/images/capability.png" alt="capability_preview" style="zoom:15%;" />



## News

- [2025.09.24] We released KidGym and open-sourced the code on **[GitHub](https://github.com/BoBo-Ye/KidGym)**.
- [2026.01.26] KidGym has been accepted as a poster at **ICLR 2026**. 🎉
- [2026.03.10] We have created KidGym Playground on **[Hugging Face](https://huggingface.co/spaces/BoBo-Ye/KidGym_Playground)** for online experience.

## Tasks

### Single Capacity Task

|            Scene            |        Task        |                                                                                                                                                                          Description                                                                                                                                                                          |           Capability           |
| :-------------------------: | :-----------------: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :-----------------------------: |
| ![CL](./static/gifs/Classification.gif) | Classification (CL) |                                                                                             In CL task, the agent is required to place each item into its designated container based on specific instructions, such as*"placing the sushi in the green basket"*.                                                                                             |            Execution            |
| ![SE](./static/gifs/Selection.gif) |     Selection (SE)     | In SE task, several random items will appear in the left hint bar at first. Once the task starts, these items will be hidden, and the agent need to select the items that appeared in the hint bar before. |            Memory            |
| ![SO](./static/gifs/Sorting.gif) | Sorting (SO) | In SO task, the agent is presented with a rule that may contradict real-world knowledge. For instance, the agent might be instructed that*"the faster the animal, the heavier it is"*. The agent is expected to correctly rank the animals based on the given rule. | Learning |
| ![MA](./static/gifs/Maze.gif) | Maze (MA) | This task is inspired by [Procgon](https://github.com/openai/train-procgen), where the agent must obtain the diamond in a maze with several locked doors. The agent needs to collect the corresponding colored keys to unlock these doors. | Planning |
| ![FI](./static/gifs/Filling.gif) |    Filling (FI)    |                                             In FI task, the agent will be presented with an image in which a quarter section has been removed, such as*“an elephant with a missing head”*. Then it needs to restore the image by selecting the correct missing piece from a set of distractors in the backpack.                                             |      Perception Reasoning      |
| ![PU](./static/gifs/Puzzle.gif) |     Puzzle (PU)     |                                                                             In PU task, a target image composed of four puzzle pieces is displayed in the hint bar, and the agent needs to assemble the scattered puzzle pieces from its backpack to reconstruct the target image.                                                                             | Perception Reasoning (Abstract) |

### Composite Capacity Task

|             Scene             |         Task         |                                                                                                                                                               Description                                                                                                                                                               |           Capability           |
| :---------------------------: | :------------------: | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :-----------------------------: |
| ![PL](./static/gifs/Placement.gif) | Placement (PL) | In PL task, the agent is required to place the item in the opposite position based on the given goal. For instance, if the rule states*"place the tortoise on the north side of the toy horse"*, the agent actually needs to place it on the*"south"* side. | Learning + Perception Reasoning |
|  ![CL](./static/gifs/Counting.gif)  |    Counting (CO)    |                                                             In CO task, the scene contains several piles of items, with quantities ranging from 1 to 3. At the start of the task, the agent is given a target number and then it must collect exactly that number of items.                                                             | Planning + Perception Reasoning |
| ![DMA](./static/gifs/Decode_Maze.gif) | Decode Maze (DMA) | This task follows the same rules as the “Maze”, with an added challenge. The agent can no longer use a same-colored key to open a door. Instead, it must learn the “key-door” correspondence shown in the hint bar. | Learning + Planning |
| ![MMA](./static/gifs/Memory_Maze.gif) | Memory Maze (MMA) |                                                                                   This task follows the same rules as the "Maze", with an added challenge. Before the task begins, the agent is shown the location of the diamond, but once the task starts, the diamond in the scene will be hidden and several treasure chests will appear. To succeed, the agent must correctly open the chest containing the diamond.                                                                                   |  Memory + Planning  |
| ![MDE](./static/gifs/Memory_Decode.gif) |  Memory Decode (MDE)  | This task follows the same rules as "Decode", with an added challenge. The agent must additionally remember the relationships indicated in the code table, which will be hidden once the task starts. |        Memory + Perception Reasoning        |
| ![MFI](./static/gifs/Memory_Filling.gif) | Memory Filling (MFI) |                                                                  This task follows the same rules as "Filling", with an added challenge. The agent must additionally remember the target, which will disappear once the task starts.                                                                  |        Memory + Learning        |

## Getting Started

[![python version](https://img.shields.io/badge/Python_Version_%3E=_3.10-green)](https://www.python.org/downloads/release/python-3100/)

```cmd
$ conda create -n KidGym python==3.10
$ pip install -r requirements.txt
```

## Using KidGym

KidGym repository's code structure is as follows:

```sh
├── assets/
│   ├── imgs/
│   ├── jsons/
│   └── ...   
├── src/
│   ├── agent.py
│   ├── grid.py
│   └── ...   
├── tasks/
│      ├── task_1.py
│      ├── task_2.py
│      └── ...
└── main.py
```

Each task type is a **class** file located in `tasks/` and you can run it by:

```cmd
$ python main.py --task = <task_name>_<difficulty_level>
```

For example, you can run `python main.py --task = CL_L1` to test Classification Level-1.

## Citing KidGym

```
@inproceedings{ye2026kidgym,
  title     = {Children's Intelligence Tests Pose Challenges for MLLMs? KidGym: A 2D Grid-Based Reasoning Benchmark for MLLMs},
  author    = {Ye, Hengwei and Guan, Yuanting and Ge, Yuxuan and Zhu, Tianying and Guan, Zhenhan and Zhong, Yijia and Zhang, Yijing and Zhang, Han and Wu, Yingna and Tian, Zheng},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2026}
}
```
