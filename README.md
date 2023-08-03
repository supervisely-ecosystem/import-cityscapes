<div align="center" markdown>
<img src="https://i.imgur.com/sfh2ILA.png" width="1900px"/>

# Import Cityscapes

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#Preparation">Preparation</a> •
  <a href="#How-To-Run">How To Run</a> •
  <a href="#How-To-Use">How To Use</a>
</p>


[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/import-cityscapes)
[![views](https://app.supervise.ly/img/badges/views/supervisely-ecosystem/import-cityscapes.png)](https://supervise.ly)
[![runs](https://app.supervise.ly/img/badges/runs/supervisely-ecosystem/import-cityscapes.png)](https://supervise.ly)

</div>

## Overview

Import data in [Cityscapes](https://github.com/mcordts/cityscapesScripts) format to [Supervisely](https://supervise.ly/) from a folder or `.tar` archive.

## Preparation

Upload your data in Cityscapes format to `Team Files` (for example you can create `import_cityscapes` folder). You can also upload data from `.tar` archive ([download example](https://www.cityscapes-dataset.com/downloads/)).

<img src="https://i.imgur.com/GZtPx4b.png"/>

#### The structure of the directory or archive has to be the following:

```
📦project folder or .tar archive
├──📂gtFine
│   ├──📂test
│   │   └──...
│   ├──📂train
│   │   └──...
│   └──📂val
│       └──...
└──📂leftImg8bit
    ├──📂test
    │   └──...
    ├──📂train
    │   └──...
    └──📂val
        └──...
```

#### Note:

Import will crash if the archive with the parent directory doesn't contain corresponding data.

## How To Run 

**Step 1**: Add the app to your team from [Ecosystem](https://ecosystem.supervise.ly/apps/import-cityscapes) if it is not there.

**Step 2**: Go to the `Team Files` page, right-click on your `.tar` archive or `folder`, containing cityscapes data, and choose `Run App`->`Import Cityscapes`. 

<img src="https://i.imgur.com/3ItAVU7.png"/>

**Step 3**: Set target slider value to split image sets to `train` and `val` and assign corresponding tags(only for cases, when the image set doesn't contain `val` folder). Press the `RUN` button. As a result, you will be redirected to `Workspace Tasks` page.

<img src="https://i.imgur.com/m4ew7vo.png" width="600px"/>



## How to use

The resulting project will be placed in your current `Workspace` with name in format `{archive/folder name}`. Images in datasets will have tags (`train`, `val`, or `test`) corresponding to the parent directories in which the datasets were located during import. If input data(archive or folder) contains `train` folder and doesn't contain `val` folder, the images from `train` folder will be tagged with `train` and `val` tags according to the exposed slider ratio.

<img src="https://i.imgur.com/TMjl7Pt.png"/>

You can also access your project by clicking on its name from the `Workspace Tasks` page.

<img src="https://i.imgur.com/i0pfXRV.png">
