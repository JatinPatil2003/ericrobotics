#!/usr/bin/env python3

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

def main():
    rospy.init_node('camera_publisher_node', anonymous=True)
    rate = rospy.Rate(10)  # Set the publishing rate (10 Hz in this case)

    # Replace 'camera_topic' with the topic name to publish the camera frames
    pub = rospy.Publisher('/normal_image', Image, queue_size=10)
    bridge = CvBridge()

    # Open the camera (you can also use other image sources like video files)
    cap = cv2.VideoCapture(0)

    while not rospy.is_shutdown():
        ret, frame = cap.read()
        if not ret:
            rospy.logerr("Failed to read camera frame.")
            break

        # Convert the OpenCV image to a ROS Image message
        ros_image_msg = bridge.cv2_to_imgmsg(frame, "bgr8")

        # Publish the ROS Image message
        pub.publish(ros_image_msg)
        cv2.imshow('Webcam', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        rate.sleep()

    cap.release()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
