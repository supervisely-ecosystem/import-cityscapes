import os
import zipfile, tarfile
import cv2
import supervisely_lib as sly
from collections import defaultdict
from supervisely_lib.annotation.tag_meta import TagValueType
from supervisely_lib.io.fs import download, file_exists, get_file_name, remove_dir
from supervisely_lib.video_annotation.video_tag import VideoTag
from supervisely_lib.video_annotation.video_tag_collection import VideoTagCollection


my_app = sly.AppService()
TEAM_ID = int(os.environ['context.teamId'])
WORKSPACE_ID = int(os.environ['context.workspaceId'])
INPUT_DIR = str(os.environ['context.Folder'])
#INPUT_DIR = os.environ.get("modal.state.slyFolder")

project_name = 'cityscapes'
IMAGE_EXT = '.png'

#ARH_NAMES = ['MOT15.zip', 'MOT16.zip', 'MOT17.zip', 'MOT20.zip']
#LINKS = ['https://motchallenge.net/data/MOT15.zip', 'https://motchallenge.net/data/MOT16.zip', 'https://motchallenge.net/data/MOT17.zip', 'https://motchallenge.net/data/MOT20.zip']
obj_class_name = 'pedestrian'
conf_tag_name = 'ignore_conf'
video_ext = '.mp4'
mot_bbox_file_name = 'gt.txt'
seqinfo_file_name = 'seqinfo.ini'
frame_rate_default = 25
image_name_length = 6
logger = sly.logger



@my_app.callback("import_cityscapes")
@sly.timeit
def import_cityscapes(api: sly.Api, task_id, context, state, app_logger):
    storage_dir = my_app.data_dir
    logger.warn(storage_dir)
    logger.warn(INPUT_DIR)

    if INPUT_DIR:
        cur_files_path = INPUT_DIR
        extract_dir = os.path.join(storage_dir, cur_files_path)
        logger.warn(extract_dir)
        archive_path = os.path.join(storage_dir, project_name + '.zip')
        logger.warn(archive_path)

        api.file.download(TEAM_ID, cur_files_path, archive_path)

        if zipfile.is_zipfile(archive_path):
            logger.info('Extract archive {}'.format(archive_path))
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
        else:
            raise Exception("No such file".format(project_name + 'zip'))

    my_app.stop()

    '''
    new_project = api.project.create(WORKSPACE_ID, project_name, change_name_if_conflict=True)
    obj_class = sly.ObjClass(obj_class_name, sly.Rectangle)
    conf_tag_meta = sly.TagMeta(conf_tag_name, TagValueType.NONE)
    meta = sly.ProjectMeta(sly.ObjClassCollection([obj_class]), sly.TagMetaCollection([conf_tag_meta]))
    api.project.update_meta(new_project.id, meta.to_json())

    for ARH_NAME, LINK in zip(ARH_NAMES, LINKS):

        archive_path = os.path.join(storage_dir, ARH_NAME)

        if not file_exists(archive_path):
            logger.info('Download archive {}'.format(ARH_NAME))
            download(LINK, archive_path)
        #api.file.download(TEAM_ID, cur_files_path, archive_path)
        if zipfile.is_zipfile(archive_path):
            logger.info('Extract archive {}'.format(ARH_NAME))
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(storage_dir)
        else:
            raise Exception("No such file {}".format(ARH_NAME))

        logger.info('Check input mot format')
        if get_file_name(ARH_NAME) in ['MOT16']:
            remove_dir(os.path.join(storage_dir, 'test'))
            curr_mot_dir = os.path.join(storage_dir, 'train')
        else:
            curr_mot_dir = os.path.join(storage_dir, get_file_name(ARH_NAME))
        check_mot_format(curr_mot_dir)

        dataset_name = get_file_name(ARH_NAME)
        new_dataset = api.dataset.create(new_project.id, dataset_name, change_name_if_conflict=True)
        for r, d, f in os.walk(curr_mot_dir):
            if mot_bbox_file_name in f:
                video_name = r.split('/')[-2] + video_ext
                logger.info('Video {} being processed'.format(video_name))
                video_path = os.path.join(curr_mot_dir, video_name)
                imgs_path = r[:-2] + 'img1'
                images = os.listdir(imgs_path)
                progress = sly.Progress('Create video and figures for frame', len(images), app_logger)
                images_ext = images[0].split('.')[1]
                seqinfo_path = r[:-2] + seqinfo_file_name
                frames_with_objects, frames_without_objs_conf = get_frames_with_objects_gt(os.path.join(r, mot_bbox_file_name))
                if os.path.isfile(seqinfo_path):
                    img_size, frame_rate = img_size_from_seqini(seqinfo_path)
                else:
                    img = sly.image.read(os.path.join(imgs_path, images[0]))
                    img_size = (img.shape[1], img.shape[0])
                    frame_rate = frame_rate_default
                video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'MP4V'), frame_rate, img_size)
                im_names = []
                im_paths = []
                ids_to_video_object = {}
                new_frames = []
                for image_id in range(1, len(images) + 1):
                    new_figures = []
                    image_name = str(image_id).zfill(image_name_length) + '.' + images_ext
                    im_names.append(image_name)
                    im_paths.append(os.path.join(imgs_path, image_name))
                    video.write(cv2.imread(os.path.join(imgs_path, image_name)))
                    frame_object_coords = frames_with_objects[image_id]
                    for idx, coords in frame_object_coords.items():
                        if idx not in ids_to_video_object.keys():
                            curr_frame_ranges = frames_without_objs_conf[idx]
                            if len(curr_frame_ranges) == 0:
                                ids_to_video_object[idx] = sly.VideoObject(obj_class)
                            else:
                                conf_tags = [VideoTag(conf_tag_meta, frame_range=[curr_frame_range[0]-1, curr_frame_range[1]-1]) for curr_frame_range in curr_frame_ranges]
                                ids_to_video_object[idx] = sly.VideoObject(obj_class, tags=VideoTagCollection(conf_tags))
                        left, top, w, h = coords
                        bottom = top + h
                        if round(bottom) >= img_size[1] - 1:
                            bottom = img_size[1] - 2
                        right = left + w
                        if round(right) >= img_size[0] - 1:
                            right = img_size[0] - 2
                        if left < 0:
                            left = 0
                        if top < 0:
                            top = 0
                        if right <= 0 or bottom <= 0 or left >= img_size[0] or top >= img_size[1]:
                            continue

                        geom = sly.Rectangle(top, left, bottom, right)
                        figure = sly.VideoFigure(ids_to_video_object[idx], geom, image_id - 1)
                        new_figures.append(figure)
                    new_frame = sly.Frame(image_id - 1, new_figures)
                    new_frames.append(new_frame)
                    progress.iter_done_report()

                video.release()
                file_info = api.video.upload_paths(new_dataset.id, [video_name], [video_path])
                new_frames_collection = sly.FrameCollection(new_frames)
                new_objects = sly.VideoObjectCollection(ids_to_video_object.values())
                ann = sly.VideoAnnotation((img_size[1], img_size[0]), len(new_frames), objects=new_objects, frames=new_frames_collection)
                logger.info('Create annotation for video {}'.format(video_name))
                api.video.annotation.append(file_info[0].id, ann)
        remove_dir(curr_mot_dir)
    my_app.stop()
    '''


def main():
    sly.logger.info("Script arguments", extra={
        "TEAM_ID": TEAM_ID,
        "WORKSPACE_ID": WORKSPACE_ID
    })

    # Run application service
    my_app.run(initial_events=[{"command": "import_cityscapes"}])



if __name__ == '__main__':
        sly.main_wrapper("main", main)

