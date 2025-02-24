import cv2
import os
import threading

def create_mappings():
    char_to_val = {chr(i): i for i in range(256)}
    val_to_char = {i: chr(i) for i in range(256)}
    return char_to_val, val_to_char

def encrypt_message(image, message):
    char_to_val, _ = create_mappings()
    height, width, _ = image.shape

    x, y, color_channel = 0, 0, 0

    for char in message:
        if x >= height:
            print("⚠️ Error: Message is too long for this image!")
            return None
        image[x, y, color_channel] = char_to_val[char]
        y += 1
        if y >= width:
            y = 0
            x += 1
        color_channel = (color_channel + 1) % 3

    return image

def decrypt_message(image, message_length, passcode, original_passcode):
    input_passcode = input("\n🔑 Enter the passcode for decryption: ")
    if input_passcode == original_passcode:
        _, val_to_char = create_mappings()
        height, width, _ = image.shape

        decrypted_message = ""
        x, y, color_channel = 0, 0, 0

        for _ in range(message_length):
            if x >= height:
                break
            decrypted_message += val_to_char[image[x, y, color_channel]]
            y += 1
            if y >= width:
                y = 0
                x += 1
            color_channel = (color_channel + 1) % 3

        print(f"\n✅ Decryption successful! \n📩 Hidden Message: {decrypted_message}")
    else:
        print("\n❌ Authentication failed! Incorrect passcode.")

image_path = "SyedMoinUddinAyaz.jpg"
image = cv2.imread(image_path)

if image is None:
    print("❌ Error: Could not load image. Check the file path!")
    exit()

secret_message = input("\n🔒 Enter the secret message: ")
passcode = input("🔑 Set a passcode for encryption: ")

encrypted_image = encrypt_message(image.copy(), secret_message)
if encrypted_image is not None:
    output_image_path = "encryptedImage.jpg"
    cv2.imwrite(output_image_path, encrypted_image)
    print("\n✅ Message encrypted successfully!")
    print(f"📁 Encrypted image saved as '{output_image_path}'.")

    cv2.namedWindow("🖼️ Encrypted Image", cv2.WINDOW_NORMAL)
    
    decryption_thread = threading.Thread(target=decrypt_message, args=(encrypted_image, len(secret_message), passcode, passcode))
    decryption_thread.start()

    cv2.imshow("🖼️ Encrypted Image", encrypted_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
