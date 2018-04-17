#!/user/bin/env python
# _*_ coding:utf-8 _*_
import os

from learning import retrain

# retrain.main(__import__(bottleneck_dir='d://tensorflow_pb/tf_files/bottlenecks',
#                         how_many_training_steps=500,
#                         model_dir='d://tensorflow_pb/tf_files/inception',
#                         output_graph='d://tensorflow_pb/tf_files/retrained_graph.pb',
#                         output_labels='d://tensorflow_pb/tf_files/retrained_labels.txt',
#                         image_dir ='d://picReptile'))

os.system('python D:/pythonWork/reptile/pic_reptile/learning/retrain.py --bottleneck_dir=/tf_files/bottlenecks --how_many_training_steps 4000 --model_dir=/tf_files/inception --output_graph=/tf_files/retrained_graph.pb --output_labels=/tf_files/retrained_labels.txt --image_dir d:/picReptile')