import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import cv2


def draw_bboxes_with_labels(image, bboxes, label_texts):
    """
    在ndarray或tf.Tensor对象上，画bboxes和对应的labels
    :param image:       一张图片，shape 为 [height, width, channels]
    :param bboxes:      一组bounding box，shape 为 [bbox_number, 4]，顺序为 ymin, xmin, ymax, xmax
                        float类型，取值范围[0, height/width]
    :param label_texts:      要显示的标签，shape为(bbox_number, )
    :return:        画完bbox的图片，为ndarray类型，shape与输入相同
    """
    if isinstance(image, tf.Tensor):
        image = image.numpy()
    if isinstance(bboxes, tf.Tensor):
        bboxes = bboxes.numpy()
    if isinstance(label_texts, tf.Tensor):
        label_texts = label_texts.numpy()
    idx = 0
    for bbox in bboxes:
        ymin, xmin, ymax, xmax = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        if label_texts is not None:
            cv2.putText(img=image,
                        text=str(label_texts[idx]),
                        org=(xmin, ymin + 20),
                        fontFace=cv2.FONT_HERSHEY_COMPLEX,
                        fontScale=1e-3 * image.shape[0],
                        color=(0, 0, 255),
                        thickness=2,
                        )
        idx += 1
    return image


def show_one_image(preprocessed_image, bboxes, labels_text=None, preprocessing_type='caffe', caffe_pixel_means=None,
                   figsize=(15, 10), enable_matplotlib=True):
    """
    显示图片
    :param preprocessed_image:      preprocessed image by `preprocessing_type`, if caffe then bgr, if tf then rgb
    :param bboxes:
    :param labels_text:
    :param preprocessing_type:
    :param caffe_pixel_means:
    :param figsize:
    :param enable_matplotlib:
    :return:
    """
    if isinstance(preprocessed_image, tf.Tensor):
        preprocessed_image = tf.squeeze(preprocessed_image, axis=0).numpy()
    if isinstance(bboxes, tf.Tensor):
        bboxes = bboxes.numpy()
    if isinstance(labels_text, tf.Tensor):
        labels_text = labels_text.numpy()
    if preprocessing_type == 'caffe':
        cur_means = caffe_pixel_means
        preprocessed_image[..., 0] += cur_means[0]
        preprocessed_image[..., 1] += cur_means[1]
        preprocessed_image[..., 2] += cur_means[2]
        preprocessed_image = preprocessed_image[..., ::-1]
        preprocessed_image = preprocessed_image.astype(np.uint8)
    elif preprocessing_type == 'tf':
        preprocessed_image = ((preprocessed_image + 1.0) / 2.0) * 255.0
        preprocessed_image = preprocessed_image.astype(np.uint8)
    elif preprocessing_type is None:
        pass
    else:
        raise ValueError('unknown preprocess_type {}'.format(preprocessing_type))
    image_with_bboxes = draw_bboxes_with_labels(preprocessed_image, bboxes, labels_text)
    if enable_matplotlib:
        plt.figure(figsize=figsize)
        plt.imshow(image_with_bboxes)
        plt.show()

    return image_with_bboxes
