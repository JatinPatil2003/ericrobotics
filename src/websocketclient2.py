#!/usr/bin/env python3
import asyncio
import websockets
import numpy as np
import cv2
import requests
import base64

async def connect_to_stream():
    async with websockets.connect('ws://localhost:8765') as websocket: 
        while True:
            # Receive and process the stream data from the WebSocket server
            stream_data = await websocket.recv()
            # Process the stream data as needed
            image_data = eval(stream_data)  # Convert the JSON string to a Python dictionary
            base64_str = image_data['base64']
            img_data = base64.b64decode(base64_str)
            nparr = np.frombuffer(img_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # img_np = np.frombuffer(stream_data, dtype=np.uint8)
            # frame = nparr.reshape((480, 640, 3))
            # frame = cv2.imdecode(stream_data, cv2.IMREAD_COLOR)
            print("recv")
            # Display the frame
            cv2.imshow('Video Stream 1', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


asyncio.get_event_loop().run_until_complete(connect_to_stream())
