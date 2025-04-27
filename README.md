Stream Video using OpenCV and FFmpeg
This project captures video frames from a camera and streams them via RTP to a specified IP address using FFmpeg for encoding and streaming.

Steps to get it working:

1. Start the Server
Ensure you have a server running that can receive RTP streams. This could be any server configured to listen on a specific port for incoming RTP streams.

2. Set the Port
The destination port is passed as a parameter when running the Python program.

You will provide the port number on the command line when running the program.

Example: python main.py 00000

Port is passed as an parameter at the begining of the program.

3. Start Sending the Stream
Once the server is running and the port is set, you can start the stream by running the program with the desired port as a parameter.

The program will capture video frames from your camera and send them over RTP to the specified IP and port using FFmpeg.

4. Run the Program
Ensure that Python 3.x is installed on your system.

Install the necessary dependencies: pip install opencv-python

You will also need FFmpeg installed. You can install FFmpeg using the following command: sudo apt-get install ffmpeg

Once all dependencies are set up, you can start the Python program as described in step 3.

Example to run the program with a port number: python main.py 16146

Additional Information
FFmpeg: This project uses FFmpeg for encoding and sending the RTP stream. Ensure FFmpeg is properly installed and accessible in your system's PATH.

Camera Settings: The program uses OpenCV to capture video frames. You can adjust the frame size (WIDTH, HEIGHT) and framerate (FRAMERATE) in the script if necessary.

Troubleshooting
Camera not found: Ensure that the camera is properly connected and accessible. If you are using an external camera, check that the correct device is selected.

FFmpeg errors: If FFmpeg fails to start, ensure that FFmpeg is installed correctly and that all dependencies are met.

Stream not working: Verify that the server is correctly set up to receive the RTP stream and that the IP and port in the script are correctly configured.

License
This project is open-source and available under the MIT License.

