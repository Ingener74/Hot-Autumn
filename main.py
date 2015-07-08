# encoding: utf8
import sys
from PySide.QtCore import Qt, QTimer, QSettings
from PySide.QtGui import QApplication, QWidget, QMessageBox
from StringIO import StringIO
import numpy as np
import paramiko as paramiko
from res.monitor import Ui_Monitor

import matplotlib

matplotlib.rcParams['backend.qt4'] = 'PySide'
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

USER = 'griffon'
PASS = 'CvfhnUtqvp'

COMPANY = 'ShnaiderSoft'
APPNAME = 'Monitor'


# noinspection PyPep8Naming
def getMonitorData(host):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=USER, password=PASS)
        stdin, stdout, stderr = client.exec_command('cat /tmp/monitor.log')
        data = stdout.read() + stderr.read()
        client.close()
        return data
    except paramiko.BadHostKeyException, e:
        print e
    except paramiko.AuthenticationException, e:
        print e
    except paramiko.SSHException, e:
        print e
    return None


GRAPH_RSS = 1
GRAPH_VRAM = 4
GRAPH_TOTAL = 6

# noinspection PyTypeChecker
def getGraph(host, graph):
    try:
        data = getMonitorData(host)

        data = data.replace(':', '')
        data = data.replace(';', '')

        data = StringIO(data)

        data = np.loadtxt(data, dtype={
            'names': ('rss_', 'rss', 'vram_', 'gtt_', 'vram', 'total_', 'total'),
            'formats': ('S3', 'i4', 'S4', 'S3', 'i4', 'S5', 'i4')
        })

        count = len(data)

        minutes = count * 5. / 60.

        x = np.arange(0, minutes, minutes / count)
        y = [i[graph] for i in data]

        assert len(x) == len(y)

        return x, y

    except TypeError, e:
        print e
        print (None, None)
    except ValueError, e:
        print e
        print (None, None)


class PlotWidget(FigureCanvas):
    def __init__(self, title, xlabel, ylabel):
        FigureCanvas.__init__(self, Figure())
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.axis = self.figure.add_subplot(111)

    def plot(self, x, y):
        self.axis.clear()
        self.axis.plot(x, y)
        font = {'family': 'Courier New'}
        self.axis.set_title(self.title, font)
        self.axis.set_xlabel(self.xlabel, font)
        self.axis.set_ylabel(self.ylabel, font)
        self.draw()

    def savePlot(self, pngFileName):
        self.figure.savefig(pngFileName)


# noinspection PyPep8Naming
class MonitorWindow(QWidget, Ui_Monitor):
    def __init__(self, app, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)

        settings = QSettings(QSettings.IniFormat, QSettings.UserScope, COMPANY, APPNAME)
        self.host.setText(settings.value('hostname', '127.0.0.1'))

        self.updateTimer = QTimer(self)
        self.updateTimer.timeout.connect(self.onTimeout)

        self.app = app

        self.updateMonitorButton.clicked.connect(self.start)

        self.plotWidget = PlotWidget(u'Graph rss_pages', u'Time, min', u'rss_pages value')
        self.verticalLayout.insertWidget(2, self.plotWidget)

        self.host_name = None

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    # noinspection PyCallByClass,PyCallByClass,PyUnusedLocal
    def start(self):
        try:
            x, y = getGraph(self.host.text(), GRAPH_RSS)
            if None == x or None == y:
                return
            self.plotWidget.plot(x, y)

            self.updateTimer.start(1000)

        except UnicodeError, e:
            QMessageBox.warning(self, u'Ошибка', u'Проверь IP адрес')

    def onTimeout(self):
        try:
            x, y = getGraph(self.host.text(), GRAPH_RSS)
            if None == x or None == y:
                return
            self.plotWidget.plot(x, y)
        except UnicodeError, e:
            print e

    def closeEvent(self, e):
        settings = QSettings(QSettings.IniFormat, QSettings.UserScope, COMPANY, APPNAME)
        settings.setValue('hostname', self.host.text())

        self.plotWidget.savePlot('test.png')


if __name__ == '__main__':
    # noinspection PyCallByClass,PyTypeChecker
    QApplication.setStyle(u'plastique')
    app = QApplication(sys.argv)

    window = MonitorWindow(app)
    window.show()

    sys.exit(app.exec_())
