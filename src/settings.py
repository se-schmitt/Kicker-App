# Import public modules
from nicegui import app, ui
import cv2, os.path

# Import custom modules
from init import df_players, player

is_file_uploaded = False
k_factor = 1.5
count = 0

def content() -> None:
    with ui.tab_panel('Einstellungen').style('background-color: rgb(255,255,255)'):
        with ui.card():
            ui.label('Allgemeine Einstellungen')
            ui.button('Spieler hinzufügen', on_click=lambda: dialog_add_player.open())

# Function to add player
with ui.dialog() as dialog_add_player:
    new_player = player('','media/dummy_player.png')
    with ui.card():
        ui.label('Spieler hinzufügen').style('font-size: 20px; font-weight: bold;')
        ui.input(placeholder='Hier Namen eingeben').bind_value_to(new_player,'name').style('font-size: 20px; font-weight: bold;')
        ui.upload(on_upload=lambda e: save_file_in_media(e,new_player), auto_upload=True, max_files=1).bind_enabled(new_player,target_name='image').bind_visibility_from(new_player,'name',lambda x: len(x) > 0 and not is_file_uploaded) #os.path.isfile(new_player.image.replace('.png','_original.png')
        image = ui.image().bind_visibility_from(new_player,'image',lambda x: x != 'media/dummy_player.png')
        with ui.row().bind_visibility_from(new_player,'image',lambda x: x != 'media/dummy_player.png').classes('w-full justify-center items-around text-center'):
            ui.button('-', on_click=lambda: crop_to_square_with_face_increase_k(new_player.image.replace('.png','_original.png'), new_player.image, 0.1)).style('width: 100px;')
            ui.label('Ausschnitt anpassen')#.classes('w-full justify-center items-around text-center')
            ui.button('+', on_click=lambda: crop_to_square_with_face_decrease_k(new_player.image.replace('.png','_original.png'), new_player.image, 0.1)).style('width: 100px;')
        with ui.row().bind_visibility_from(new_player,'name',lambda x: len(x) > 0).classes('w-full justify-center items-around text-center'):
            ui.button('Spieler hinzufügen', on_click=lambda: add_player_to_db(new_player)).style('font-weight: bold;')
            ui.button('Abbrechen', on_click=lambda: print(new_player.image)).style('font-weight: bold; background-color: rgb(255,0,0);')

# Function to set image file name
def save_file_in_media(e,new_player):
    global is_file_uploaded

    # Save file as 'original'
    new_player.image = 'media/' + new_player.name + '.png'
    with open(new_player.image.replace('.png','_original.png'),'wb') as f:
        f.write(e.content.read())

    # Crop image
    crop_to_square_with_face(new_player.image.replace('.png','_original.png'), new_player.image, k_factor)

    is_file_uploaded = True

# Function to crop image
def crop_to_square_with_face(image_path, output_path, k):
    global count

    # Load the image
    img = cv2.imread(image_path)
    htot, wtot, _ = img.shape
    
    # Load the face detection model from OpenCV
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    
    if len(faces) > 0:
        # Get the coordinates of the first detected face
        x, y, w, h = faces[0]
        
        # Determine the size of the square
        size = min(int(round(max(w, h)*k)),wtot,htot)
        
        # Calculate the center of the face
        center_x = min(max(x + w // 2, size // 2),wtot-size//2)
        center_y = min(max(y + h // 2, size // 2),htot-size//2)
        
        # Calculate the coordinates of the square
        x1 = center_x - size // 2
        x2 = center_x + size // 2
        y1 = center_y - size // 2
        y2 = center_y + size // 2
        
        # Crop the image to the square region
        cropped_img = img[y1:y2, x1:x2]
        
        # Save the cropped image
        cv2.imwrite(output_path, cropped_img)
        cv2.imwrite(output_path.replace('.png','_'+str(count)+'.png'), cropped_img)
        
        # image.set_source('media/dummy_player.png')
        image.set_source(output_path.replace('.png','_'+str(count)+'.png'))

        count += 1
        print(f"Image cropped and saved to {output_path}")
    else:
        print("No face detected in the image")

# Help functions to adjust crop size
def crop_to_square_with_face_increase_k(image_path, output_path, k):
    global k_factor
    k_factor += k
    crop_to_square_with_face(image_path, output_path, k_factor)

def crop_to_square_with_face_decrease_k(image_path, output_path, k):
    global k_factor
    k_factor -= k
    crop_to_square_with_face(image_path, output_path, k_factor)

# Function to add player to database
def add_player_to_db(p):
    df_players.loc[len(df_players)] = [p.name, 1000, p.image]