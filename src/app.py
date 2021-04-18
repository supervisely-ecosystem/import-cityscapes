import os
import zipfile, json
import cv2
import supervisely_lib as sly
import glob
from pathlib import Path
from collections import defaultdict
from supervisely_lib.annotation.tag_meta import TagValueType
from supervisely_lib.io.fs import download, file_exists, get_file_name, remove_dir
from supervisely_lib.video_annotation.video_tag import VideoTag
from supervisely_lib.video_annotation.video_tag_collection import VideoTagCollection


my_app = sly.AppService()
TEAM_ID = int(os.environ['context.teamId'])
WORKSPACE_ID = int(os.environ['context.workspaceId'])
INPUT_DIR = os.environ.get("modal.state.slyFolder")
INPUT_FILE = os.environ.get("modal.state.slyFile")

PROJECT_NAME = 'cityscapes'
IMAGE_EXT = '.png'

logger = sly.logger




def json_path_to_image_path(json_path):
    img_path = json_path.replace('/gtFine/', '/leftImg8bit/')
    img_path = img_path.replace('_gtFine_polygons.json', '_leftImg8bit' + IMAGE_EXT)
    return img_path


def convert_points(simple_points):
    return [sly.PointLocation(int(p[1]), int(p[0])) for p in simple_points]


@my_app.callback("import_cityscapes")
@sly.timeit
def import_cityscapes(api: sly.Api, task_id, context, state, app_logger):
    tag_metas = sly.TagMetaCollection()
    obj_classes = sly.ObjClassCollection()
    dataset_names = []

    storage_dir = my_app.data_dir

    if INPUT_DIR:
        project_name = PROJECT_NAME
        cur_files_path = INPUT_DIR
        extract_dir = os.path.join(storage_dir, cur_files_path)
        input_dir = os.path.join(extract_dir, project_name)
        archive_path = os.path.join(storage_dir, project_name + '.zip')
    else:
        cur_files_path = INPUT_FILE
        extract_dir = os.path.join(storage_dir, sly.fs.get_file_name(cur_files_path))
        archive_path = os.path.join(storage_dir, sly.fs.get_file_name_with_ext(cur_files_path))
        input_dir = extract_dir
        project_name = sly.fs.get_file_name_with_ext(INPUT_FILE)

    #api.file.download(TEAM_ID, cur_files_path, archive_path)

    #if zipfile.is_zipfile(archive_path):
    #    logger.info('Extract archive {}'.format(archive_path))
    #    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
    #        zip_ref.extractall(extract_dir)
    #else:
    #    raise Exception("No such file".format(project_name + 'zip'))


    new_project = api.project.create(WORKSPACE_ID, project_name, change_name_if_conflict=True)
    search_fine = os.path.join(extract_dir, "gtFine", "*", "*", "*_gt*_polygons.json")
    files_fine = glob.glob(search_fine)
    files_fine.sort()

    search_imgs = os.path.join(extract_dir, "leftImg8bit", "*", "*", "*_leftImg8bit" + IMAGE_EXT)
    files_imgs = glob.glob(search_imgs)
    files_imgs.sort()

    samples_count = len(files_fine)
    progress = sly.Progress('Project: {!r}'.format(new_project.name), samples_count)

    images_pathes = {}
    images_names = {}
    anns_data = {}
    ds_name_to_id = {}
    for orig_ann_path in files_fine:
        parent_dir, json_filename = os.path.split(os.path.abspath(orig_ann_path))

        dataset_name = os.path.basename(parent_dir)
        if dataset_name not in dataset_names:
            dataset_names.append(dataset_name)
            ds = api.dataset.create(new_project.id, dataset_name, change_name_if_conflict=True)
            ds_name_to_id[dataset_name] = ds.id
            images_pathes[dataset_name] = []
            images_names[dataset_name] = []
            anns_data[dataset_name] = []

        sample_name = json_filename.replace('_gtFine_polygons.json', IMAGE_EXT)
        orig_img_path = json_path_to_image_path(orig_ann_path)
        images_pathes[dataset_name].append(orig_img_path)
        images_names[dataset_name].append(sly.io.fs.get_file_name_with_ext(orig_img_path))

        tag_path = os.path.split(parent_dir)[0]
        train_val_tag = os.path.basename(tag_path)

        tag_meta = sly.TagMeta(train_val_tag, sly.TagValueType.NONE)
        if not tag_metas.has_key(tag_meta.name):
            tag_metas = tag_metas.add(tag_meta)
        tag = sly.Tag(tag_meta)

        json_data = json.load(open(orig_ann_path))
        ann = sly.Annotation.from_img_path(orig_img_path)

        for obj in json_data['objects']:
            class_name = obj['label']
            if class_name == 'out of roi':
                polygon = obj['polygon'][:5]
                interiors = [obj['polygon'][5:]]
            else:
                polygon = obj['polygon']
                interiors = []

            interiors = [convert_points(interior) for interior in interiors]
            polygon = sly.Polygon(convert_points(polygon), interiors)
            obj_class = sly.ObjClass(name=class_name, geometry_type=sly.Polygon)
            ann = ann.add_label(sly.Label(polygon, obj_class))
            if not obj_classes.has_key(class_name):
                obj_classes = obj_classes.add(obj_class)

        ann = ann.add_tag(tag)
        anns_data[dataset_name].append(ann)



        #if all(os.path.isfile(x) for x in (orig_img_path, orig_ann_path)):
        #    ds.add_item_file(sample_name, orig_img_path, ann=ann)
        #else:
        #    sly.logger.warn('Skipped sample without a complete set of files: {}'.format(sample_name),
        #                    exc_info=False, extra={'sample_name': sample_name,
        #                                           'image_path': orig_img_path,
        #                                           'annotation_path': orig_ann_path})

        progress.iter_done_report()

    

    stat_dct = {'samples': samples_count, 'src_ann_cnt': len(files_fine), 'src_img_cnt': len(files_imgs)}

    sly.logger.info('Found img/ann pairs.', extra=stat_dct)
    if stat_dct['samples'] < stat_dct['src_ann_cnt']:
        sly.logger.warn('Found source annotations without corresponding images.', extra=stat_dct)

    out_meta = sly.ProjectMeta(obj_classes=obj_classes, tag_metas=tag_metas)
    new_project.set_meta(out_meta)
    sly.logger.info('Found classes.', extra={'cnt': len(obj_classes),
                                             'classes': sorted([obj_class.name for obj_class in self.obj_classes])})
    sly.logger.info('Created tags.', extra={'cnt': len(out_meta.tag_metas),
                                            'tags': sorted([tag_meta.name for tag_meta in out_meta.tag_metas])})

    my_app.stop()



def main():
    sly.logger.info("Script arguments", extra={
        "TEAM_ID": TEAM_ID,
        "WORKSPACE_ID": WORKSPACE_ID
    })

    # Run application service
    my_app.run(initial_events=[{"command": "import_cityscapes"}])



if __name__ == '__main__':
        sly.main_wrapper("main", main)

