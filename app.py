import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from app_editor import EditorApp
 
def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = EditorApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    sys.exit(app.exec_())  # и запускаем приложение

if __name__=='__main__':
    #print(dir())
    #print(sys.path)
    main()
    