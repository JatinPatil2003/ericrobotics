#!/usr/bin/env python3

import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge
import asyncio
import websockets
from sensor_msgs.msg import CompressedImage
import base64
import json

connected_clients = set()
rospy.init_node('websocket_stream')

bridge = CvBridge()
msg = CompressedImage()
msg.format = "jpeg"


def camera_topic_callback(msgs):
    # Convert ROS CompressedImage to OpenCV image
    msg.data = msgs.data

async def video_stream(websocket, path):
    connected_clients.add(websocket)
    try:
        while True:
            
            # ret, frame = cap.read()
            # encoded_frame = cv2.imencode('.jpg', frame)[1].tostring()
            # msg = CompressedImage()
            # msg.format = "jpeg"
            # msg.data = encoded_frame

            # img_bytes = bridge.compressed_imgmsg_to_cv2(msg)

            base64_str = base64.b64encode(msg.data).decode('utf-8')
            image_data = {'base64': base64_str}
            # json_data = json.dumps(image_data)
            await asyncio.wait([client.send(json.dumps(image_data)) for client in connected_clients])
            print("sent")
    finally:
        connected_clients.remove(websocket)


camera_subscriber = rospy.Subscriber('camera_encoded', CompressedImage, camera_topic_callback)
start_server = websockets.serve(video_stream, 'localhost', 8765)  # Replace 'localhost' with the appropriate IP address

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
