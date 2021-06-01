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
[![views](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/import-cityscapes&counter=views&label=views)](https://supervise.ly)
[![used by teams](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/import-cityscapes&counter=downloads&label=used%20by%20teams)](https://supervise.ly)
[![runs](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/import-cityscapes&counter=runs&label=runs&123)](https://supervise.ly)

</div>

## Overview

Import data in [Cityscapes](https://github.com/mcordts/cityscapesScripts) format to [Supervisely](https://supervise.ly/) from folder or `tar` archive.

## Preparation

Upload your data in Cityscapes format to `Team Files` (for example you can create `import_cityscapes` folder). You can also upload data from `.tar` archive ([download example](https://www.cityscapes-dataset.com/downloads/)).

<img src="https://i.imgur.com/GZtPx4b.png"/>

#### Structure of directory or  archive have to be the following:   
```
.
├── gtFine
│   ├── test
│   │   ├── ...
│   ├── train
│   │   ├── ...
│   └── val
│       └── ...
└── leftImg8bit
    ├── test
    │   ├── ...
    ├── train
    │   ├── ...
    └── val
        └── ...
```

#### Note:

Import will crash, if archive with parent directory doesn't contain corresponding data.

## How To Run 

**Step 1**: Add app to your team from [Ecosystem](https://ecosystem.supervise.ly/apps/import-cityscapes) if it is not there.

**Step 2**: Go to `Current Team`->`Files` page, right-click on your `.tar` archive or `folder`, containing cityscapes data and choose `Run App`->`import-cityscapes`. 

<img src="https://i.imgur.com/3ItAVU7.png"/>

**Step 3**: Set target slider value to split image sets to `train` and `val` and assign corresponding tags(only for case, when image set doesn't contain `val` folder). You will be redirected to `Workspace`->`Tasks` page.

<img src="https://i.imgur.com/jErwlV0.png" width="600px"/>



## How to use

Resulting project will be placed to your current `Workspace` with the same name as the cityscapes archive. Images in datasets will have tags (`train`, `val`, or `test`) corresponding to the parent directories in which the datasets were located during import. If the `train` directories are in the input folders, but the `val` directories are not, then the images in `train` folder will be tagged with `train` and `val` tags in the ratio, exposed in the slider.

<img src="https://i.imgur.com/TMjl7Pt.png"/>

You can also access your project by clicking on it's name from `Tasks` page.

<img src="https://i.imgur.com/i0pfXRV.png">
