import subprocess
import time
import cv2
import signal
import sys

# Parameters
DEST_IP = "192.168.1.86"
DEST_PORT = int(sys.argv[1])
WIDTH = 640
HEIGHT = 480
FRAMERATE = 30
SSRC = 22222222

ffmpeg_proc = None
camera = None

def start_ffmpeg():
    global ffmpeg_proc
    ffmpeg_command = [
        'ffmpeg',
        '-re',  # Read input at native frame rate
        '-f', 'rawvideo',  # Input format: raw video
        '-pix_fmt', 'bgr24',  # Pixel format for raw video (from OpenCV)
        '-s', f'{WIDTH}x{HEIGHT}',  # Resolution of the video
        '-r', str(FRAMERATE),  # Frame rate
        '-i', '-',  # Input from stdin (frames will be piped)
        '-an',  # Disable audio
        '-c:v', 'libx264',  # Use x264 codec for encoding
        '-profile:v', 'baseline',  # Set H.264 profile
        '-level', '3.2',  # Set H.264 level
        '-b:v', '2000k',  # Set video bitrate
        '-x264opts', 'keyint=30:min-keyint=30:no-scenecut',  # Keyframe settings
        '-ssrc', str(SSRC),  # Set SSRC (Synchronization Source Identifier)
        '-vf', 'format=yuv420p',  # Convert pixel format to yuv420p for compatibility
        '-f', 'rtp',  # Output format: RTP
        f'rtp://{DEST_IP}:{DEST_PORT}'  # Destination IP and port
    ]

    print(f"Starting ffmpeg to stream to {DEST_IP}:{DEST_PORT} with SSRC {SSRC}...")
    ffmpeg_proc = subprocess.Popen(
        ffmpeg_command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,  # Capture stdout
        stderr=subprocess.PIPE,  # Capture stderr
        bufsize=0
    )

def stop_ffmpeg():
    global ffmpeg_proc
    if ffmpeg_proc:
        try:
            ffmpeg_proc.stdin.close()
            ffmpeg_proc.terminate()
            ffmpeg_proc.wait(timeout=5)
        except Exception as e:
            print(f"Error stopping ffmpeg: {e}")
        finally:
            ffmpeg_proc = None

def release_camera():
    global camera
    if camera:
        camera.release()
        camera = None

def signal_handler(sig, frame):
    print("\nStopping...")
    stop_ffmpeg()
    release_camera()
    sys.exit(0)

def warmup_camera(cam):
    print("Warming up camera (60 frames)...")
    for _ in range(60):
        cam.read()

def main():
    global camera

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    camera.set(cv2.CAP_PROP_FPS, FRAMERATE)

    if not camera.isOpened():
        print("❌ Failed to open camera")
        return

    warmup_camera(camera)

    start_ffmpeg()
    print(f"✅ Streaming to {DEST_IP}:{DEST_PORT} (Ctrl+C to stop)")

    try:
        while True:
            ret, frame = camera.read()
            if not ret:
                print("❌ Failed to grab frame")
                break

            try:
                ffmpeg_proc.stdin.write(frame.tobytes())
                # Print message indicating the frame was sent successfully
                print("✅ Frame captured and sent successfully.")
            except BrokenPipeError:
                print("❌ FFmpeg has stopped unexpectedly.")
                break

    except KeyboardInterrupt:
        pass

    finally:
        stop_ffmpeg()
        release_camera()
        print("Resources released. Streaming stopped.")

if __name__ == "__main__":
    main()
