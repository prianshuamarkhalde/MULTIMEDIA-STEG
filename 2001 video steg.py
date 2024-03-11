from tkinter import *
from tkinter import filedialog
import os
import cv2
import numpy as np
from stegano import lsb
import cv2
from PIL import Image
from io import BytesIO

root = Tk()
root.title("Video Steganography - Hide a Secret Text Message in a Video")
root.geometry("700x500+250+180")
root.resizable(False, False)
root.configure(bg="#2f4155")

# Define global variables
video_filename = None
secret_frames = []


def show_video():
    global video_filename
    video_filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                                title='Select Video File',
                                                filetypes=(("MP4 file", "*.mp4"),
                                                           ("AVI File", "*.avi"),
                                                           ("All files", "*.*")))
    lbl_video.config(text=f"Selected Video: {os.path.basename(video_filename)}")


def hide_message():
    global secret_frames
    secret_frames = []  # Reset frames
    message = text_video.get(1.0, END)

    if video_filename:
        cap = cv2.VideoCapture(video_filename)
        for _ in range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))):
            ret, frame = cap.read()
            if ret:
                # Save the frame as an image file
                _, temp_frame = cv2.imencode('.png', frame)
                image_io = BytesIO(temp_frame.tobytes())
                img = Image.open(image_io)

                # Hide the message in the image
                secret_img = lsb.hide(img, message)

                # Convert the secret image back to a NumPy array
                secret_frame = cv2.cvtColor(np.array(secret_img), cv2.COLOR_RGB2BGR)
                secret_frames.append(secret_frame)
            else:
                break
        cap.release()

def show_hidden_message():
    global hidden_message
    hidden_message = ""

    if secret_frames:
        for secret_frame in secret_frames:
            # Save the secret frame as an image file
            _, temp_frame = cv2.imencode('.png', secret_frame)
            image_io = BytesIO(temp_frame.tobytes())
            secret_img = Image.open(image_io)

            # Reveal the message from the image
            hidden_message = lsb.reveal(secret_img)

        # Display the hidden message
        print(f"Hidden Message: {hidden_message}")



def save_video():
    if secret_frames:
        # Create a new video file with hidden frames
        output_video_filename = "hidden_video.mp4"
        out = cv2.VideoWriter(output_video_filename, cv2.VideoWriter_fourcc(*'mp4v'), 30, (640, 480))
        for secret_frame in secret_frames:
            out.write(secret_frame)
        out.release()
        print(f"Hidden video saved as {output_video_filename}")
    else:
        print("No hidden frames to save.")


# Icon
image_icon = PhotoImage(file="logo.jpg")
root.iconphoto(False, image_icon)

# Logo
logo = PhotoImage(file="logo.png")
Label(root, image=logo, bg="#2f4155").place(x=10, y=0)

Label(root, text="CYBER SCIENCE", bg="#2d4155", fg="white", font="arial 25 bold").place(x=100, y=20)

# First Frame
f_video = Frame(root, bd=3, bg="black", width=340, height=100, relief=GROOVE)
f_video.place(x=10, y=80)

lbl_video = Label(f_video, bg="black", fg="white", font="arial 14 bold")
lbl_video.place(x=10, y=10)

# Second Frame
frame2_video = Frame(root, bd=3, width=340, height=280, bg="white", relief=GROOVE)
frame2_video.place(x=10, y=200)

text_video = Text(frame2_video, font="Roboto 20", bg="white", fg="black", relief=GROOVE, wrap=WORD)
text_video.place(x=0, y=0, width=320, height=250)

scrollbar2 = Scrollbar(frame2_video)
scrollbar2.place(x=320, y=0, height=250)

scrollbar2.configure(command=text_video.yview)
text_video.configure(yscrollcommand=scrollbar2.set)

# Third Frame
frame3_video = Frame(root, bd=3, bg="#2f4155", width=330, height=100, relief=GROOVE)
frame3_video.place(x=360, y=80)

Button(frame3_video,
       text="Open Video",
       width=10,
       height=2,
       font="arial 14 bold",
       command=show_video).place(x=20, y=30)
Button(frame3_video,
       text="Save Video",
       width=10,
       height=2,
       font="arial 14 bold",
       command=save_video).place(x=180, y=30)
Label(frame3_video,
      text="Video File",
      bg="#2f4155",
      fg="yellow").place(x=20, y=5)

# Fourth Frame
frame4_video = Frame(root, bd=3, bg="#2f4155", width=330, height=100, relief=GROOVE)
frame4_video.place(x=360, y=200)

Button(frame4_video,
       text="Hide Data",
       width=10,
       height=2,
       font="arial 14 bold",
       command=hide_message).place(x=20, y=30)
Button(frame4_video,
       text="Show Data",
       width=10,
       height=2,
       font="arial 14 bold",
       command=show_hidden_message).place(x=180, y=30)
Label(frame4_video,
      text="Video File",
      bg="#2f4155",
      fg="yellow").place(x=20, y=5)

root.mainloop()
