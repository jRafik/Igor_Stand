from PyQt5 import QtWidgets, uic
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice
import time
import pygetwindow as gw
import pyautogui
import os
import pyperclip


# Создание приложения
app = QtWidgets.QApplication([])

# Загрузка UI
ui = uic.loadUi("Menu_for_Taburet.ui")
ui.setWindowTitle("LOX")

# Настройки последовательного порта
serial = QSerialPort()
serial.setBaudRate(115200)

# Получение списка доступных портов и добавление их в ComboBox
portList = []
ports = QSerialPortInfo().availablePorts()
for port in ports:
    portList.append(port.portName())
ui.comL.addItems(portList)

#Переменные перемещений
Xposition = 0.0
Yposition = 0.0
Zposition = 0.0


# Функция открытия порта
def onOpen():
    serial.setPortName(ui.comL.currentText())
    if serial.open(QIODevice.ReadWrite):
        ui.textBrowser.append("Порт открыт")
    else:
        ui.textBrowser.append("Не удалось открыть порт")

# Функция закрытия порта
def onClose():
    if serial.isOpen():
        serial.close()
        ui.textBrowser.append("Порт закрыт")

# Функция чтения данных из порта
def onRead():
    rx = serial.readLine()
    rxs = str(rx, 'utf-8').strip()
    ui.textBrowser.append(rxs)  # Добавление данных в textBrowser

# Функция отправки данных в порт
def serialSend():
    if serial.isOpen():
        serial.write(b"x10")  # Отправка байтовой строки
    else:
        ui.textBrowser.append("Порт не открыт")

# Функция отправки текста
def sendText():
    txs = ui.textF.displayText()
    serial.write(txs.encode())

# Функция перемещения по оси X
def moveX():
    x = ui.textX.displayText()
    serial.write(b'x' + x.encode())

# Функция перемещения по оси Y
def moveY():
    y = ui.textY.displayText()
    serial.write(b'y' + y.encode())

# Функция перемещения по оси Z
def moveZ():
    z = ui.textZ.displayText()
    serial.write(b'z' + z.encode())

# Функция длины измерения по X
def Xmeasuring():
    global Xmeas
    Xmeas = float(ui.textXmeas.displayText())

# Функция длины измерения по Y
def Ymeasuring():
    global Ymeas
    Ymeas = float(ui.textYmeas.displayText())

# Функция длины измерения по Z
def Zmeasuring():
    global Zmeas
    Zmeas = float(ui.textZmeas.displayText())

# Функция шага измерения по X
def XMeasuringStep():
    global Xstep
    Xstep = float(ui.textXstep.displayText())

# Функция шага измерения по Y
def YMeasuringStep():
    global Ystep
    Ystep = float(ui.textYstep.displayText())

# Функция шага измерения по Z
def ZMeasuringStep():
    global Zstep
    Zstep = float(ui.textZstep.displayText())

# Функция времни между измерениями
def Time():
    global timeIgor
    timeIgor = float(ui.textTime.displayText())

# Функция для измерения амплитуды колебаний
def amplitude():
    # Находим окно приложения "FFT signal analysis"
    app_window = gw.getWindowsWithTitle("Узкополосный спектр - Demo 1")[0]

    # Делаем окно активным
    app_window.activate()

    # Эмулируем нажатие клавиш "CTRL + N"
    pyautogui.hotkey('ctrl', 'n')
    time.sleep(1)  # Ждем немного перед копированием, чтобы новое окно успело открыться

    # Получаем скопированный текст (предполагается, что он уже находится в буфере обмена)
    copied_text = pyperclip.paste()

    # Создаем папку "Desktop" на рабочем столе, если её нет
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    if not os.path.exists(desktop_path):
        os.makedirs(desktop_path)

    # Путь к файлу "Results.txt" на рабочем столе
    file_path = os.path.join(desktop_path, 'Results.txt')

    # Записываем скопированный текст в файл
    with open(file_path, 'w') as file:
        file.write(copied_text)

    print(f'Текст успешно скопирован в файл {file_path}')

    def process_file():
        # Укажем пути к файлам
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        input_file_path = os.path.join(desktop_path, "Results.txt")
        output_file_path = os.path.join(desktop_path, "Results_2.txt")

        try:
            # Читаем данные из файла
            with open(input_file_path, 'r', encoding='windows-1251') as file:
                lines = file.readlines()

            if not lines:
                print(f"Файл {input_file_path} пуст.")
                return

            if lines[0].strip() == "":
                if len(lines) < 3:
                    print("Недостаточно строк в файле для обработки.")
                    return

                # Формируем новую первую строку
                new_first_line = lines[1].strip() + ";" + lines[2].strip() + ";" + str(Xposition) + ";" + str(Yposition) + ";" + str(Zposition) + ";"
            else:
                if len(lines) < 2:
                    print("Недостаточно строк в файле для обработки.")
                    return

                # Формируем новую первую строку
                new_first_line = lines[0].strip() + ";" + lines[1].strip() + ";" + str(Xposition) + ";" + str(Yposition) + ";" + str(Zposition) + ";"

            # Записываем результат в новый файл
            with open(output_file_path, 'a', encoding='windows-1251') as file:
                file.write(new_first_line + "\n")

            # Сообщаем об успешной записи
            print(f"Результаты записаны в файл: {output_file_path}")

        except FileNotFoundError:
            print(f"Файл {input_file_path} не найден.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

        finally:
            # Удаляем файл "Results.txt"
            try:
                if os.path.exists(input_file_path):
                    os.remove(input_file_path)
                    print(f"Файл {input_file_path} был успешно удален.")
            except Exception as e:
                print(f"Не удалось удалить файл {input_file_path}: {e}")

    if __name__ == "__main__":
        process_file()

# Функция для возврата осей в координаты 0,0,0
def home():
    serial.write(b'h0')

# Функция измерения по плоскости XY (Для Мелихова)
def IgorPidr():
    global Xposition, Yposition
    while Xposition <= Xmeas:
        while Yposition <= Ymeas:
            serial.write(b'y' + str(Yposition).encode())
            if (serial.waitForBytesWritten() == 1):
                time.sleep(timeIgor)
                amplitude()
                Yposition += Ystep
        Xposition += Xstep
        serial.write(b'x' + str(Xposition).encode())
        if (serial.waitForBytesWritten() == 1):
            time.sleep(timeIgor)
            Yposition = 0
    Xposition = 0
    serial.write(b'h0')
    ui.textBrowser.append("Конец измерений")

# Подключение сигналов к слотам
serial.readyRead.connect(onRead)
ui.openB.clicked.connect(onOpen)
ui.closeB.clicked.connect(onClose)
ui.sendB.clicked.connect(sendText)
ui.buttX.clicked.connect(moveX)
ui.buttY.clicked.connect(moveY)
ui.buttZ.clicked.connect(moveZ)
ui.textXmeas.textChanged.connect(Xmeasuring)
ui.textYmeas.textChanged.connect(Ymeasuring)
ui.textZmeas.textChanged.connect(Zmeasuring)
ui.textXstep.textChanged.connect(XMeasuringStep)
ui.textYstep.textChanged.connect(YMeasuringStep)
ui.textZstep.textChanged.connect(ZMeasuringStep)
ui.textTime.textChanged.connect(Time)
ui.startB.clicked.connect(IgorPidr)
ui.homeButton.clicked.connect(home)

# Показ UI и запуск приложения
ui.show()
app.exec()

