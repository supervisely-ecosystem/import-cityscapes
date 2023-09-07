<div align="center" markdown>
<img src="https://github.com/supervisely-ecosystem/import-cityscapes/assets/57998637/359774eb-c9bf-41ec-a414-37bdc2f3bc6b" width="1900px"/>

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

Import data in [Cityscapes](https://github.com/mcordts/cityscapesScripts) format to [Supervisely](https://supervise.ly/) from a folder or archive.

## Preparation

Upload your data as a project folder in Cityscapes format to `Team Files`.<br>
ℹ️ You can download the archive with data example [here](https://github.com/supervisely-ecosystem/import-cityscapes/files/12547999/my_cityscapes_project.zip).<br>

<img src="https://github.com/supervisely-ecosystem/import-cityscapes/assets/57998637/2bc7ec24-6efb-4ade-95ca-7204aee22d0e"/>

#### The structure of the project has to be the following:

```
📦project folder or archive
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

⚠️ **Note:** Import will crash if the archive with the parent directory doesn't contain corresponding data.

## How To Run 

**Step 1**: Add the app to your team from [Ecosystem](https://ecosystem.supervise.ly/apps/import-cityscapes) if it is not there.

**Step 2**: Go to the `Team Files` page, right-click on your archive or `folder`, containing cityscapes data, and choose `Run App`->`Import Cityscapes`. 

<img src="https://github.com/supervisely-ecosystem/import-cityscapes/assets/57998637/a5f78d65-cc15-4936-8975-e084d2a411af"/>

Another way to import is to find the app page in Ecosystem and click `RUN APP...` button. Then you will see a modal window.

<img src="https://github.com/supervisely-ecosystem/import-cityscapes/assets/57998637/b4d11cb2-a71b-48ae-8985-7b8128b62ec5">


There you can drag-and-drop projects or choose from `Team Files` too.

<img width="394" alt="ecosystem" src="https://github.com/supervisely-ecosystem/import-cityscapes/assets/57998637/234d6e49-8d2b-4a9e-9959-49406b419572">

**Step 3**: Set target slider value to split image sets to `train` and `val` and assign corresponding tags(only for cases, when the image set doesn't contain `val` folder). Press the `RUN` button. As a result, you will be redirected to `Workspace Tasks` page.



## How to use

The resulting project will be placed in your current `Workspace` with name in format `{archive/folder name}`. Images in datasets will have tags (`train`, `val`, or `test`) corresponding to the parent directories in which the datasets were located during import. If input data(archive or folder) contains `train` folder and doesn't contain `val` folder, the images from `train` folder will be tagged with `train` and `val` tags according to the exposed slider ratio.

<img src="https://github.com/supervisely-ecosystem/import-cityscapes/assets/57998637/145c3230-f9a6-4e86-bdf8-ef8174fd3729"/>

You can also access your project by clicking on its name from the `Workspace Tasks` page.

<img src="https://github.com/supervisely-ecosystem/import-cityscapes/assets/57998637/b5ed75cd-4003-4469-9be7-bfdf8931217b">
