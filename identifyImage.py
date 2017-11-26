#   This module is a part of WebSight project for OpenSource workshop.
# -----------------------------------------------------------------------------
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
from skimage.transform import resize
import os.path
import re
import sys
import numpy as np
import tensorflow as tf
import Request
import Response

MODEL_DIR = "./identifyImage_weights"
TEST_IMAGE = os.path.join(MODEL_DIR, 'cropped_panda.jpg')


class NodeLookup(object):
  """Converts integer node ID's to human readable labels."""

  def __init__(self,
               label_lookup_path=None,
               uid_lookup_path=None):
    if not label_lookup_path:
      label_lookup_path = os.path.join(
          MODEL_DIR, 'imagenet_2012_challenge_label_map_proto.pbtxt')
    if not uid_lookup_path:
      uid_lookup_path = os.path.join(
          MODEL_DIR, 'imagenet_synset_to_human_label_map.txt')
    self.node_lookup = self.load(label_lookup_path, uid_lookup_path)

  def load(self, label_lookup_path, uid_lookup_path):
    """Loads a human readable English name for each softmax node.

    Args:
      label_lookup_path: string UID to integer node ID.
      uid_lookup_path: string UID to human-readable string.

    Returns:
      dict from integer node ID to human-readable string.
    """
    if not tf.gfile.Exists(uid_lookup_path):
      tf.logging.fatal('File does not exist %s', uid_lookup_path)
    if not tf.gfile.Exists(label_lookup_path):
      tf.logging.fatal('File does not exist %s', label_lookup_path)

    # Loads mapping from string UID to human-readable string
    proto_as_ascii_lines = tf.gfile.GFile(uid_lookup_path).readlines()
    uid_to_human = {}
    p = re.compile(r'[n\d]*[ \S,]*')
    for line in proto_as_ascii_lines:
      parsed_items = p.findall(line)
      uid = parsed_items[0]
      human_string = parsed_items[2]
      uid_to_human[uid] = human_string

    # Loads mapping from string UID to integer node ID.
    node_id_to_uid = {}
    proto_as_ascii = tf.gfile.GFile(label_lookup_path).readlines()
    for line in proto_as_ascii:
      if line.startswith('  target_class:'):
        target_class = int(line.split(': ')[1])
      if line.startswith('  target_class_string:'):
        target_class_string = line.split(': ')[1]
        node_id_to_uid[target_class] = target_class_string[1:-2]

    # Loads the final mapping of integer node ID to human-readable string
    node_id_to_name = {}
    for key, val in node_id_to_uid.items():
      if val not in uid_to_human:
        tf.logging.fatal('Failed to locate: %s', val)
      name = uid_to_human[val]
      node_id_to_name[key] = name

    return node_id_to_name

  def id_to_string(self, node_id):
    if node_id not in self.node_lookup:
      return ''
    return self.node_lookup[node_id]


def create_graph():
  """Creates a graph from saved GraphDef file and returns a saver."""
  # Creates graph from saved graph_def.pb.
  with tf.gfile.FastGFile(os.path.join(
      MODEL_DIR, 'classify_image_graph_def.pb'), 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')

def run_inference_on_image(image, top_pred_amount):
  if not tf.gfile.Exists(image):
    tf.logging.fatal('File does not exist %s', image)
  image_data = tf.gfile.FastGFile(image, 'rb').read()

  # Creates graph from saved GraphDef.
  create_graph()

  with tf.Session() as sess:
    # --- ron visualization of the graph with tensorboard --logdir "C:\\visu":
    # writer = tf.summary.FileWriter("C:\\visu") 
    # writer.add_graph(sess.graph)
    
    #  --- the 1 before last layer will be used to connect to the LSTM:
    # pool_3_tensor = sess.graph.get_tensor_by_name('pool_3:0') 
    
    softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')
    predictions = np.squeeze(sess.run(softmax_tensor,
                           {'DecodeJpeg/contents:0': image_data}))
    
    # reached here ==============================================
    # Creates node ID --> English string lookup.
    node_lookup = NodeLookup()

    top_k = predictions.argsort()[-top_pred_amount:][::-1]
    for node_id in top_k:
      human_string = node_lookup.id_to_string(node_id)
      score = predictions[node_id]
      print('%s (score = %.5f)' % (human_string, score))
    prediction = node_lookup.id_to_string(top_k[0])
    return prediction.split(' ')[0]


def predict(image=TEST_IMAGE, top_pred_amount=5):
  print("begin")
  run_inference_on_image(image, top_pred_amount)
  print("done")

def crop_and_resize(image):
    """
    An heuristic invented by Ron and should be tested.
    Adjust given input image to best fit the network by
    cropping it to be the middle biggest square which is included,
    and resizing it to be 256x256, as ImageNet training set was.
    """
    image = imread(image)
    edge_size = np.min(image.shape)
    top_left_corner = image.shape[0]//4, image.shape[1]//4
    cropped = image[top_left_corner[0]:, top_right_corner[1]:]
    small = resize(cropped, (256,256), anti_aliasing=True, mode='reflect')
    return small

def main(request):
    image_path = request.getImage()
    prediction =  predict(image_path, 1)
    response = Response(True, prediction)
    return response

    
  
if __name__ ==   "__main__":
    # img_test = crop_and_resize("c.jpg")
    # imshow(img_test)
    predict(os.path.join(MODEL_DIR,"c.jpg"))

