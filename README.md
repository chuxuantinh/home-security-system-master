# Home Security System using Face Recognition
Built system to recognize faces and give access to home, based on access profile (family, friend, intruder) in database.
Possesses multi-level security. (PIR motion sensor inside for motion detection and webcam outside home for surveillance and face recognition)
Owner/s can access system remotely and can also see live video surveillance on mobile phones/PC at any time.
(Check out test_videos.txt for links to YouTube videos to see the project in action!)

Which file does what-

homesec.py- does the security part of the project (uses webcam, identifies faces, uses Pushover API to send notifications to the Pushover app)
blynk_motor.py- uses Blynk API to control the motors (doors) through the Blynk app
The 24x7 surveillance was managed by using an Android app called RaspiCam Remote which after initial setup, automatically acquired and displayed live stream from the Raspberry Pi Camera (The app uses RTSP- Real Time Streaming Protocol coupled with VLC)
