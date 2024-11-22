from PIL import Image

N = 8 # кол-во бит для длины сообщения

def set_bit(val, bit_val): 
    mask = 1            #Маска устанавливается в 1, что соответствует младшему биту.
    val &= ~mask    
    if bit_val:         #Если bit_val равно 1, то младший бит val устанавливается в 1
        val |= mask         
    return val

while True:
    variant = input('Что бы вы сделали? (упаковать(p), распаковать(u), выйти(q)) ') 
    if variant == 'p':
        image = Image.open("image.jpg")         
        result_image = image.copy()
        width, height = image.size              #Получаются размеры изображения (ширина и высота)
        message = input(f'Введите сообщение для упаковки (max {2**N - 1} символов) ')
        length = format(len(message), '08b')                          #Длина сообщения преобразуется в 8-битный двоичный формат
        message_bin = ''.join(format(ord(i), '08b') for i in message) #Каждый символ сообщения преобразуется в его двоичный эквивалент
        pack_data = [int(n) for n in length + message_bin]            #Все двоичные данные (длина и само сообщение) объединяются в один список 
        ind = 0                                  #встраивание двоичных данных в пиксели изображения
        for y in range(height):                  #Перебираются все пиксели изображения
            for x in range(width):               #Для каждого пикселя извлекаются его цветовые компоненты
                pixel = list(image.getpixel((x, y)))
                for c in range(len(pixel)):
                    if ind < len(pack_data):                        #Если еще есть данные для упаковки, младший бит соответствующей 
                        pixel[c] = set_bit(pixel[c], pack_data[ind])#цветовой компоненты изменяется с помощью функции 
                        ind += 1
                result_image.putpixel((x, y), tuple(pixel))         #Измененный пиксель сохраняется обратно в result_image
        
        result_image.save('output.png')
        result_image.show()
    elif variant == 'u':
        image = Image.open("output.png")
        width, height = image.size
        binary_res = []                          #пустой список для хранения извлеченных битов
        for y in range(height):                  #Перебираются все пиксели изображения
            for x in range(width):
                pixel = list(image.getpixel((x, y)))
                for c in range(len(pixel)):               #Для каждой цветовой компоненты извлекается младший бит и добавляется в binary_res
                    binary_res.append(str(pixel[c] & 1))
                                                          #двоичные данные собираются в строку и преобразуются обратно в текст
        binary_res_str = ''.join(binary_res)
        length = int(binary_res_str[:N], 2) * 8           # 8 - количество бит в байте. Длина сообщения извлекается из первых N бит
        res = ''
        for i in range(0, length, 8):                     #каждые 8 бит преобразуются обратно в символы, которые добавляются к результату 
            res += chr(int(binary_res_str[N + i:N + i + 8], 2))
        print(res)
    elif variant == 'q':
        break
    else:
        print('Неправильный ввод')