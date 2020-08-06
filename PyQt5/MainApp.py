import LoginWindow
import sys
if __name__ == "__main__":
    app = LoginWindow.QApplication(sys.argv)
    wind = LoginWindow.LoginWindow()
    wind.show()
    sys.exit(app.exec_())