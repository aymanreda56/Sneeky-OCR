import customtkinter as ctk
import pyautogui

from PIL import Image, ImageTk
import time
import os

import Nayocr




# Globals (Bad practice)
root = None
screenshot_area = None
screenshot_image = None
img = None
loading_lbl = None
text_area=None
output_obj = None

new_snip_button = None
scan_button = None
correction_button = None



def MainMenu():
    global root
    global screenshot_area
    global loading_lbl
    global text_area

    global new_snip_button
    global scan_button
    global correction_button


    root = ctk.CTk()
    root.title('Tawgeehat R2aseya')
    root.iconbitmap('favicon.ico')
    root.geometry("1400x800")

    title_frame = ctk.CTkLabel(master=root, text="Naynoona's OCR", font=('Comic Sans MS', 40, 'bold'))
    title_frame.pack()


    master_frame = ctk.CTkFrame(master=root, width=1000, height=1000)
    master_frame.pack()
    

    buttons_frame = ctk.CTkFrame(master=master_frame)
    buttons_frame.grid(row=0, column=0, rowspan=5)

    new_snip_button = ctk.CTkButton(master=buttons_frame, text="New Snip", command=snip_and_save, font=('Arial', 16, 'bold'))
    new_snip_button.grid(row=0, column=0, pady=20, padx=20)

    scan_button = ctk.CTkButton(master=buttons_frame, text="Scan", command=preOCR, font=('Arial', 16, 'bold'))
    scan_button.grid(row=1, column=0, pady=20, padx=20)

    correction_button = ctk.CTkButton(master=buttons_frame, text="Correct Spelling Mistakes", command=preCorr, state=ctk.DISABLED, font=('Arial', 16, 'bold'))
    correction_button.grid(row=2, column=0, pady=20, padx=20)

    text_area = ctk.CTkTextbox(master=master_frame, width=700, height=700, font=('Arial', 20, 'bold'))
    text_area.grid(row=0, column=1, rowspan=2)

    loading_lbl = ctk.CTkLabel(master=master_frame, text="")
    loading_lbl.grid(row=2, column=1)

    screenshot_area = ctk.CTkCanvas(master=master_frame, width = 400, height = 600, bg='#404258')
    placeholder_img = ImageTk.PhotoImage(Image.open('image_placeholder.png').resize((150,150), Image.Resampling.BILINEAR))
    screenshot_area.create_image((200,300), anchor=ctk.CENTER, image=placeholder_img)
    screenshot_area.grid(row=0, column=2, rowspan=2)

    if(img == None):
        scan_button.configure(state=ctk.DISABLED)

    fuckthearmy()

    print('here')

    root.mainloop()









def snip_and_save():
    global root
    global img
    global text_area
    global scan_button

    text_area.delete(1.0, ctk.END)

    # Hide the root window
    root.withdraw()
    time.sleep(0.15)
    

    # Take a screenshot of the entire screen
    screenshot = pyautogui.screenshot()

    # Create a new fullscreen window for selecting the area
    snip_window = ctk.CTkToplevel(root)
    snip_window.attributes("-fullscreen", True)
    snip_window.attributes("-topmost", True)
    snip_window.configure(cursor="cross")
    canvas = ctk.CTkCanvas(snip_window, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Display the screenshot on the canvas
    screenshot_image = ImageTk.PhotoImage(screenshot)
    canvas.create_image(0, 0, anchor="nw", image=screenshot_image)

    start_x = start_y = None
    rect_id = None

    # Function to start drawing the rectangle
    def on_mouse_press(event):
        nonlocal start_x, start_y
        start_x, start_y = event.x, event.y

    # Function to update the rectangle while dragging
    def on_mouse_drag(event):
        nonlocal rect_id
        if rect_id:
            canvas.delete(rect_id)
        rect_id = canvas.create_rectangle(
            start_x, start_y, event.x, event.y, outline="red", width=2
        )

    # Function to finalize the selection and save the snip
    def on_mouse_release(event):
        global img, scan_button
        nonlocal start_x, start_y
        end_x, end_y = event.x, event.y

        # Sort coordinates to ensure proper cropping
        x1, x2 = sorted([start_x, end_x])
        y1, y2 = sorted([start_y, end_y])

        # Crop the screenshot
        cropped_image = screenshot.crop((x1, y1, x2, y2))
        cropped_image.save("snipped_image.png")
        img = cropped_image
        print("Snipped image saved as 'snipped_image.png'")

        # Close the snip window
        snip_window.destroy()
        update_image_frame(detected_flag=False, image=img)
        scan_button.configure (state=ctk.NORMAL)
        root.deiconify()

    # Bind mouse events
    canvas.bind("<ButtonPress-1>", on_mouse_press)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_release)

    snip_window.mainloop()



def update_image_frame(detected_flag:bool, image:Image=None):
    global root
    global screenshot_area
    global screenshot_image

    canvas_width, canvas_height = screenshot_area.winfo_width(), screenshot_area.winfo_height()

    if(not image):
        image_path = './test_detected.png' if detected_flag else "./snipped_image.png"
        image = Image.open(image_path)
    
   
    imgwidth, imgheight = resizeimg(imwidth=image.size[0], imheight=image.size[1], targetwidth=canvas_width, targetheight=canvas_height)
    
    image = image.resize((imgwidth, imgheight))

    screenshot_image = ImageTk.PhotoImage(image)
    screenshot_area.screenshot_image = screenshot_image
    screenshot_area.create_image((200,300), anchor=ctk.CENTER, image=screenshot_image)


def resizeimg(imwidth, imheight, targetwidth, targetheight):
    if imwidth > targetwidth:
        newwidth = targetwidth
        newheight = newwidth*imheight/imwidth

        imwidth = newwidth
        imheight = newheight
    
    if imheight > targetheight:
        newheight = targetheight
        newwidth = newheight*imwidth / imheight

        imwidth = newwidth
        imheight = newheight

    return int(imwidth), int(imheight)





def preOCR():
    global loading_lbl, img, text_area, root, correction_button, scan_button, new_snip_button
    loading_lbl.configure(text="OCRing...")
    root.after(100, runOCR)

    new_snip_button.configure(state = ctk.DISABLED)
    scan_button.configure(state = ctk.DISABLED)
    correction_button.configure(state= ctk.DISABLED)
    


def runOCR():
    global loading_lbl, img, text_area, output_obj, root, new_snip_button, correction_button, scan_button
    text, newImg, output_obj = Nayocr.ocr(img)
    text_area.delete(1.0, ctk.END)
    lines = text.split("\n")
    padded_text = "\n".join(f"{line.rjust(100)}" for line in lines)  # Adjust padding as needed
    text_area.insert(1.0, text=padded_text)
    update_image_frame(detected_flag=True, image=newImg)
    loading_lbl.configure(text="OCR Finished.")

    new_snip_button.configure(state=ctk.NORMAL)
    scan_button.configure(state=ctk.NORMAL)
    correction_button.configure(state = ctk.NORMAL)




    
    
    

def preCorr():
    global loading_lbl, img, text_area, root, new_snip_button, correction_button, scan_button
    loading_lbl.configure(text="Correcting Spelling Mistakes...")
    root.after(100, runCorr)

    new_snip_button.configure(state = ctk.DISABLED)
    scan_button.configure(state = ctk.DISABLED)
    correction_button.configure(state= ctk.DISABLED)



def runCorr():
    global output_obj, new_snip_button, correction_button, scan_button
    corrected_text = Nayocr.correct(output_obj=output_obj)
    text_area.delete(1.0, ctk.END)

    lines = corrected_text.split("\n")
    padded_text = "\n".join(f"{line.rjust(100)}" for line in lines)  # Adjust padding as needed

    text_area.insert(1.0, text=padded_text)
    loading_lbl.configure(text="Finished")
    output_obj = corrected_text


    new_snip_button.configure(state=ctk.NORMAL)
    scan_button.configure(state=ctk.NORMAL)
    correction_button.configure(state = ctk.NORMAL)




def fuckthearmy():
    global root
    root.after(100000, displayfuckarmy)


def unfuckthearmy():
    global root
    root.after(5000, undisplayfuckarmy)


def displayfuckarmy():
    global loading_lbl
    loading_lbl.configure(text = "FUCK THE ARMY", text_color = "red", font=('Arial',16, 'bold'))
    unfuckthearmy()

def undisplayfuckarmy():
    global loading_lbl
    loading_lbl.configure(text = "", text_color = "white", font=('Arial',16, 'bold'))






if __name__ == "__main__":
    MainMenu()
