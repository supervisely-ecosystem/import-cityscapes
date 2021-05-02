<div align="center" markdown>
<img src="https://i.imgur.com/sfh2ILA.png" width="1900px"/>

# From Cityscapes to Supervisely format

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#Preparation">Preparation</a> •
  <a href="#How-To-Run">How To Run</a> •
  <a href="#How-To-Use">How To Use</a>
</p>

[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/export-to-cityscapes)
[![views](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/import-mot-format(https://github.com/supervisely-ecosystem/import-cityscapes)&counter=views&label=views)](https://supervise.ly)
[![used by teams](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/import-cityscapes&counter=downloads&label=used%20by%20teams)](https://supervise.ly)
[![runs](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/import-cityscapes&counter=runs&label=runs&123)](https://supervise.ly)

</div>

## Overview

App transforms folder or `tar` archive with images and labels in [Cityscapes](https://github.com/mcordts/cityscapesScripts) to [Supervisely format](https://docs.supervise.ly/data-organization/00_ann_format_navi) and uploads data to Supervisely Platform.

## Preparation

Upload images and labels in Cityscapes format to team files in `import_cityscapes` folder. It is possible to upload tar archives ([download example](https://www.cityscapes-dataset.com/downloads/)).



<img src="https://i.imgur.com/AxyGfli.png" width="900px"/>



#### Directory structure in archive have to be the following:   

```
.
├── gtFine
│   ├── test
│   │   ├── ...
│   ├── train
│   │   ├── ...
│   └── val
│       ├── ...
└── leftImg8bit
    ├── test
    │   ├── ...
    ├── train
    │   ├── ...
    └── val
        └── ...
   
```



#### Note:

If you will drag and drop archive with parent directory instead of its content, import will crash.



## How To Run 

**Step 1**: Add app to your team from [Ecosystem](https://ecosystem.supervise.ly/apps/convert-supervisely-to-cityscapes-format) if it is not there.

**Step 2**: Go to `Current Team`->`Files` page, right-click on your `.zip` archive or `import_cityscapes` folder and choose `Run App`->`import-cityscapes`. You will be redirected to `Workspace`->`Tasks` page. 

<img src="https://i.imgur.com/HUG0l7S.png" width="900px"/>



## How to use

Result project is saved your current `Workspace` with the same name as the cityscapes archive has. Images in datasets will have tags(`train`, `val`, or `test`) corresponding to the parent directories in which the datasets were located during import.

<img src="https://i.imgur.com/7VxnyjK.png"/>

You can also access your project by clicking on it's name from `Tasks` page.

<img src="https://i.imgur.com/d5phaBL.png"/>