# encoding: utf8
import sys
from StringIO import StringIO

from PySide.QtCore import Qt, QTimer, QSettings
from PySide.QtGui import QApplication, QWidget, QMessageBox

import numpy as np
import paramiko as paramiko

matplotlib.rcParams['backend.qt4'] = 'PySide'
import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from res.monitor import Ui_HotAutumn

"""
Как обновить внешний вид при его изменнии:
pyside-uic res/monitor.ui -o res/monitor.py

Установка зависимостей:
sudo apt-get install python-pyside python-paramiko python-matplotlib

Испозование:
python HotAutumn.py
"""

USER = '...'
PASS = '...'

COMPANY = 'Venus.Games'
APPNAME = 'HotAutumn'


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

graphs = [GRAPH_RSS, GRAPH_VRAM, GRAPH_TOTAL]

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
class MonitorWindow(QWidget, Ui_HotAutumn):
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

        self.graphType.currentIndexChanged.connect(self.onGraphTypeChanged)
        self.plotType = self.getPlotType()

        self.host_name = None

    def onGraphTypeChanged(self):
        self.plotType = self.getPlotType()

    def getPlotType(self):
        return graphs[self.graphType.currentIndex()]

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    # noinspection PyCallByClass,PyCallByClass,PyUnusedLocal
    def start(self):
        try:
            x, y = getGraph(self.host.text(), self.plotType)
            if None == x or None == y:
                return
            self.plotWidget.plot(x, y)

            self.updateTimer.start(1000)

        except UnicodeError, e:
            QMessageBox.warning(self, u'Ошибка', u'Проверь IP адрес')

    def onTimeout(self):
        try:
            x, y = getGraph(self.host.text(), self.plotType)
            if None == x or None == y:
                return
            self.plotWidget.plot(x, y)
        except UnicodeError, e:
            print e

    def closeEvent(self, e):
        settings = QSettings(QSettings.IniFormat, QSettings.UserScope, COMPANY, APPNAME)
        settings.setValue('hostname', self.host.text())

        # self.plotWidget.savePlot('test.png')


if __name__ == '__main__':
    # noinspection PyCallByClass,PyTypeChecker
    QApplication.setStyle(u'plastique')
    app = QApplication(sys.argv)

    window = MonitorWindow(app)
    window.show()

    sys.exit(app.exec_())
