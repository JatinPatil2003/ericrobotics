#!/usr/bin/env python3
import rospy
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage

rospy.init_node('webcam_pub')


bridge = CvBridge()

image_publisher = rospy.Publisher('camera_encoded', CompressedImage, queue_size=10)


def image_callback(ros_image_msg):
    
        # Convert the ROS Image message to an OpenCV image
        bridge = CvBridge()
        cv_image = bridge.imgmsg_to_cv2(ros_image_msg, "bgr8")
        _, encoded_frame = cv2.imencode('.jpg', cv_image)

        msg = CompressedImage()
        msg.header.stamp = rospy.Time.now()
        msg.format = "jpeg"
        msg.data = encoded_frame.tostring()

        image_publisher.publish(msg)

        # cv2.imshow('Webcam', cv_image)

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        # Display the image (you can also perform other processing here)
        # cv2.waitKey(1)

def main():

    # Replace 'camera_topic' with the topic name to subscribe to the camera frames
    rospy.Subscriber('normal_image', Image, image_callback)

    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
