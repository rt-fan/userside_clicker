import pyautogui as pa
from time import sleep
import pytesseract as pt
import cv2
import shutil

pt.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
flag = True
flag2 = False

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!    МАСШТАБ МЕНЯЕМ НА 110 %    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

while flag:
    i = 1

    ##################################################################################################################
    #                                                                                                                #
    #                                                    ГЛАВНАЯ                                                     #
    #                                                                                                                #
    ##################################################################################################################
    # Ищем на главной странице координаты изображения "MAC", исходя из них, делаем скрины и распознаем значения
    # ... UPLINK-порта и количества MAC-адресов с UPLINK-порта.

    ip = ""
    uplink_port = ""
    uplink_mac = ""
    # mac_pos = pa.locateOnScreen("image\\110_search_mac_main.png", confidence=0.8)
    mac_pos = None

    while True:
        a = pa.locateOnScreen("image\\110_search_mac_main.png", confidence=0.8)
        if a is not None:
            mac_pos = a
            break
        else:
            sleep(2)
            print("Жду главный экран...")

    try:
        # pa.screenshot('temp_img\\110_main_port.png',                                          >>>>>>>>>>>>>>>>>>>>>>
        #               region=(1050, mac_pos[1] + 42, 76, 19))  # скрин номера uplink-порта
        # uplink_port_img = cv2.imread('temp_img\\110_main_port.png')
        # uplink_port_img = cv2.cvtColor(uplink_port_img, cv2.COLOR_BGR2RGB)
        # config = r'--oem 3 --psm 6'
        # uplink_port = pt.image_to_string(uplink_port_img, config=config)
        # uplink_port = uplink_port.strip().split("/")[-1]
        #
        # pa.screenshot('temp_img\\110_main_mac.png',
        #               region=(1130, mac_pos[1] + 42, 40, 19))  # скрин количества мак-адресов
        # uplink_mac_img = cv2.imread('temp_img\\110_main_mac.png')
        # uplink_mac_img = cv2.cvtColor(uplink_mac_img, cv2.COLOR_BGR2RGB)
        # config = r'--oem 3 --psm 6'
        # uplink_mac = pt.image_to_string(uplink_mac_img, config=config)
        # uplink_mac = uplink_mac.strip()                                                       <<<<<<<<<<<<<<<<<<<<<<

        pa.screenshot('temp_img\\000_110_main_port_mac.png', region=(415, mac_pos[1] + 42, 1100, 19))
        uplink_port_img = cv2.imread('temp_img\\000_110_main_port_mac.png')
        uplink_port_img = cv2.cvtColor(uplink_port_img, cv2.COLOR_BGR2RGB)
        config = r'--oem 3 --psm 6'
        uplink_port_mac_description = pt.image_to_string(uplink_port_img, config=config)
        print(uplink_port_mac_description)
        uplink_port_mac = uplink_port_mac_description.strip().split()
        print(uplink_port_mac)
        while True:
            try:
                uplink_port_mac.remove('=')
                print(uplink_port_mac)
            except ValueError:
                break

        uplink_port_mac = uplink_port_mac[-2]
        uplink_port_mac = uplink_port_mac.split('/')[-1]
        if uplink_port_mac == '‘W250':
            uplink_port_mac = '25'
        if uplink_port_mac == '260':
            uplink_port_mac = '26'
        if uplink_port_mac == '=25':
            uplink_port_mac = '25'

        print(uplink_port_mac)

        # Заходим на коммутатор
        pa.moveTo(480, mac_pos[1] + 45)
        sleep(1)
        pa.click(480, mac_pos[1] + 45)
        # sleep(2)

    except TypeError:
        with open('110_log.txt', 'a') as line:
            line.writelines("Не могу найти надпись МАК на главной странице." + '\n')

        print("Не могу найти надпись МАК на главной странице.")

    ##################################################################################################################
    #                                                                                                                #
    #                                                    ИНТЕРФЕЙСЫ                                                  #
    #                                                                                                                #
    ##################################################################################################################
    # Ищем на странице с интерфейсами изображение "MAC:", и по полученной координате делаем новый скрин этой
    # области, но уже длиннее, чтоб захватить количество маков и считать их, записав в словарь. Так же скриним
    # участок выше, где отображается поле "Descr:", считываем текст с номером порта итоже записываем в словарь.
    # Далее скролим ниже и проделываем процедуру до тех пор, пока не окажемся в конце страницы. Значения словаря
    # преобразуем в список, который проверяем на подходящие значения (чтоб мак-адресов не было меньше 3, чтоб были
    # числовые значения).

    while True:
        on = pa.locateCenterOnScreen("image\\110_link_green_on.png", confidence=0.6)
        if on is not None:
            break
        else:
            sleep(2)
            print("Жду загрузку окна с портами...")

    # НАХОДИМ, РАСПОЗНАЕМ И ЗАПИСЫВАЕМ IP-АДРЕС КОММУТАТОРА  *********************************************************

    ip_pos = pa.locateOnScreen("image\\110_search_ip.png", confidence=0.9)
    try:
        pa.screenshot('temp_img\\110_ip.png', region=(ip_pos[0], ip_pos[1], 200, 22))
        img_ip = cv2.imread('temp_img\\110_ip.png')
        img_ip = cv2.cvtColor(img_ip, cv2.COLOR_BGR2RGB)
        config = r'--oem 3 --psm 6'
        ip_line = pt.image_to_string(img_ip, config=config)
        ip_line = ip_line.replace("IP: ", "")
        index_end = ip_line.find("http")
        ip_line = ip_line[0:index_end]
        print(ip_line)

        with open('110_log.txt', 'a') as line:
            line.write('IP Адресс коммутатора: ' + ip_line + '\n')

    except TypeError:
        with open('log.txt', 'a') as line:
            line.writelines("Нет надписи IP на экране." + '\n')
        print("Нет надписи IP на экране.")
        break

    # ДЕЛАЕМ СКРИНЫ ОБЛАСТЕЙ "MAC" И "DESCR"  ************************************************************************

    #    i = 1
    dict_i = 1
    dict_j = 1
    dict1 = {}

    while True:
        for pos in pa.locateAllOnScreen('image\\110_search_mac.png', confidence=0.7, region=(700, 0, 1100, 1050)):

            name = 'temp_img\\{}_110.png'.format(i)
            name2 = 'temp_img\\{}-port_110.png'.format(i)
            i += 1
            x, y = pos[0], pos[1]  # находим координаты совпадения "MAC:"

            # делаем скрин с найденными координатами чуть длинее для захвата цифр
            pa.screenshot(name, region=(x, y, 80, 18))
            img = cv2.imread(name)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # делаем скрин области на строку выше, чтоб захватить "Descr:"
            pa.screenshot(name2, region=(770, y - 38, x - 770, 20))
            img2 = cv2.imread(name2)
            img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

            # РАСПОЗНАВАНИЕ ТЕКСТА  **********************************************************************************

            config = r'--oem 3 --psm 6'

            mac_line = pt.image_to_string(img, config=config)  # распознаем текст в скрине "MAC:"
            mac_line = mac_line.strip()

            descr_line = pt.image_to_string(img2, config=config)  # распознаем текст в скрине "Descr:"
            descr_line = descr_line.strip()

            with open('110_log.txt', 'a') as line:
                line.writelines(descr_line + '    ' + mac_line + '\n')

            print(descr_line, mac_line)

            # ОЧИЩАЕМ МАКИ И ПОРТЫ ОТ МУСОРА *************************************************************************

            # чистим порт от мусора
            for p in descr_line:
                p = descr_line.strip()
                if p.find(":"):
                    p = p.replace(":", ": ")
                if p.find("GigabitEthernet0/0/"):
                    p = p.replace("GigabitEthernet0/0/", "")
                if p.find("Ethernet1/"):
                    p = p.replace("Ethernet1/", "")
                if p.find("Ethernet1/0/"):
                    p = p.replace("Ethernet1/0/", "")
                if p.find("Ethernet0/0/"):
                    p = p.replace("Ethernet0/0/", "")
                if p.find("Ethernet1/0/"):
                    p = p.replace("Ethernet1/0/", "")
                if p.find("1/"):
                    p = p.replace("1/", "")
                if p.find("."):
                    p = p.replace(".", "")
                if p.find(","):
                    p = p.replace(",", "")
                if p.find(")"):
                    p = p.replace(")", "")
                if p.find("|"):
                    p = p.replace("|", "")
                if p.find("?"):
                    p = p.replace("?", "")

                descr_line = p.split()[-1]

            # записываем в словарь
            dict1[dict_i] = [descr_line]
            dict_i += 1

            # чистим счетчик мак от мусора
            m2 = ""
            for m in mac_line:
                m = mac_line.strip()
                if m.find(")") != -1:
                    m = m.replace(")", "")
                if m.find("]") != -1:
                    m = m.replace("]", "")
                if m.find("}") != -1:
                    m = m.replace("}", "")
                if m.find(",") != -1:
                    m = m.replace(",", "")
                if m.find(".") != -1:
                    m = m.replace(".", "")
                if m.find("|") != -1:
                    m = m.replace("|", "")
                if m.find("?") != -1:
                    m = m.replace("?", "2")
                if m.find("II") != -1:
                    m = m.replace("II", "11")

                mac_line = m.split()[-1]

            # записываем в словарь
            m2 = dict1[dict_j]
            m2.append(mac_line)
            dict1[dict_j] = m2
            dict_j += 1

        end_page = pa.locateCenterOnScreen("image\\110_end_page.png", confidence=0.9)
        if end_page is None:  # <================================================================ if end_page == None:
            pa.scroll(-1000)
            sleep(0.5)
        else:
            break

    # преобразуем словарь в список из списков
    list2 = list(dict1.values())

    # проверяем счетчик мак-адреса на то, что оно число, и значение не меньше 3
    list3 = []

    for value in list2:
        if value[1].isdigit():
            if int(value[1]) > 3:
                list3.append(value[0])

    unique_numbers = list(set(list3))
    with open('110_log.txt', 'a') as line:
        line.writelines(str(unique_numbers) + '\n')
    print(unique_numbers)

    # print(uplink_port)                                                                        >>>>>>>>>>>>>>>>>>>>>>
    #
    # if uplink_port.find(",") != -1:
    #     uplink_port = uplink_port.replace(",", "")
    # if uplink_port.find(".") != -1:
    #     uplink_port = uplink_port.replace(".", "")
    # if uplink_port.find("V") != -1:
    #     uplink_port = uplink_port.replace("V", "")
    #
    # unique_numbers.remove(uplink_port)
    #
    # # преобразуем в строку
    # downlink_port = ",".join(unique_numbers)
    # print("UPLINK:", uplink_port)
    # print("DOWNLINK:", downlink_port)
    # with open('110_log.txt', 'a') as line:
    #     line.writelines("UPLINK: " + uplink_port + '\n')
    #     line.writelines("DOWNLINK: " + downlink_port + '\n')                                  <<<<<<<<<<<<<<<<<<<<<<

    print(uplink_port_mac, '<<<')

    if uplink_port_mac.find(",") != -1:
        uplink_port_mac = uplink_port_mac.replace(",", "")
    if uplink_port_mac.find(".") != -1:
        uplink_port_mac = uplink_port_mac.replace(".", "")
    if uplink_port_mac.find("V") != -1:
        uplink_port_mac = uplink_port_mac.replace("V", "")
    if uplink_port_mac.find("W") != -1:
        uplink_port_mac = uplink_port_mac.replace("W", "")
        uplink_port_mac = uplink_port_mac[:-1]
    if uplink_port_mac.find(")") != -1:
        uplink_port_mac = uplink_port_mac.replace(")", "")
    if uplink_port_mac.find("°") != -1:
        uplink_port_mac = uplink_port_mac.replace("°", "")

    unique_numbers.remove(uplink_port_mac)

    index_dwn_p = 0
    for dwn_p in unique_numbers:
        if "2326TP" in uplink_port_mac_description:
            if int(dwn_p) <= 2:
                dwn_p = int(dwn_p) + 24
                unique_numbers[index_dwn_p] = str(dwn_p)
                index_dwn_p += 1
            else:
                unique_numbers[index_dwn_p] = str(dwn_p)
                index_dwn_p += 1
        elif "2352" in uplink_port_mac_description:
            if int(dwn_p) <= 4:
                dwn_p = int(dwn_p) + 48
                unique_numbers[index_dwn_p] = str(dwn_p)
                index_dwn_p += 1
            else:
                unique_numbers[index_dwn_p] = str(dwn_p)
                index_dwn_p += 1

    print("МОДЕЛЬ:", uplink_port_mac_description)
    print("ДЕСКРИПШН:", unique_numbers)

    # преобразуем в строку
    downlink_port = ",".join(unique_numbers)
    if "2326TP" in uplink_port_mac_description:  # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Обработка порта Хуавей
        uplink_port_mac = str(24 + int(uplink_port_mac))

    elif "2352P" in uplink_port_mac_description:
        uplink_port_mac = str(48 + int(uplink_port_mac))

    print("UPLINK:", uplink_port_mac)
    print("DOWNLINK:", downlink_port)
    with open('110_log.txt', 'a') as line:
        line.writelines("UPLINK: " + uplink_port_mac + '\n')
        line.writelines("DOWNLINK: " + downlink_port + '\n')

    # ОПРЕДЕЛЯЕМ UP/DOWN ПОРТА ***************************************************************************************

    # pix = pa.pixel(int(x) + 55, int(y))
    # if pix[0] == 255:
    #     break
    #
    # #
    #
    # end_line = "#" * 30 + "\n"
    # with open("log.txt", "a") as file:
    #     file.write(end_line)
    # print()  # разделительная полоса

    # print('END', '#' * 30, "\n")

    ##################################################################################################################
    #                                                                                                                #
    #                                                  РЕДАКТИРОВАТЬ                                                 #
    #                                                                                                                #
    ##################################################################################################################
    # Ищем на странице пункт РЕДАКТИРОВАТЬ. Если не находим, скролим вверх.
    # В полях UPLINK и DOWNLINK прописываем соответствующие порты. Жмем клавишу "Enter".

    sleep(0.5)
    while True:
        edit = pa.locateCenterOnScreen("image\\110_edit.png", confidence=0.7)
        if edit is None:
            pa.scroll(1000)
            sleep(0.5)
        else:
            pa.moveTo(edit.x, edit.y)
            sleep(1)
            pa.click(edit.x, edit.y)
            break

    sleep(2)

    uplink = pa.locateCenterOnScreen("image\\110_uplink.png", confidence=0.8)
    pa.tripleClick(uplink.x + 100, uplink.y)
    # pa.typewrite(uplink_port)                                                                 <<<<<<<<<<<<<<<<<<<<<<
    pa.typewrite(uplink_port_mac)

    downlink = pa.locateCenterOnScreen("image\\110_downlink.png", confidence=0.8)
    pa.tripleClick(downlink.x + 100, downlink.y)
    pa.typewrite(downlink_port)

    pa.press('enter')
    sleep(2)

    ##################################################################################################################
    #                                                                                                                #
    #                                                     МАК-АДРЕСА                                                 #
    #                                                                                                                #
    ##################################################################################################################

    while True:
        mac_address = pa.locateCenterOnScreen("image\\110_mac-address.png", confidence=0.7)
        if mac_address is None:
            pa.scroll(-1000)
            sleep(1)
        else:
            pa.moveTo(mac_address.x, mac_address.y)
            sleep(1)
            pa.click(mac_address.x, mac_address.y)
            break

    # sleep(6)

    delete_mac = None
    while True:
        b = pa.locateCenterOnScreen("image\\110_delete_mac.png", confidence=0.7)
        if b is not None:
            delete_mac = b
            break
        else:
            sleep(2)
            print("Жду надпись 'Удалить записи' ...")

    pa.moveTo(delete_mac.x, delete_mac.y)
    sleep(1)
    pa.click(delete_mac.x, delete_mac.y)
    sleep(1)
    pa.click(1070, 150)
    sleep(1)

    link_main = pa.locateCenterOnScreen("image\\110_userside.png", confidence=0.7)
    pa.moveTo(link_main.x, link_main.y)
    sleep(1)
    pa.click(link_main.x, link_main.y)

    with open('log.txt', 'a') as line:
        line.writelines("#################################################" + '\n' + '\n')

    print('END', '#' * 30, "\n")

    # shutil.rmtree('temp_img\\')
    # break
