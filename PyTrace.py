import math
import sys
import random
import time

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from assignment1 import *
from camera import *
from vector import * 


class PaintWidget(QWidget):
	def __init__(self, width, height, parent=None):
		super(PaintWidget, self).__init__(parent=parent)
		self.width = width
		self.height = height

		# setup an image buffer
		self.imgBuffer = QImage(self.width, self.height, QImage.Format_ARGB32_Premultiplied)
		self.imgBuffer.fill(QColor(0, 0, 0))


	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setCompositionMode(QPainter.CompositionMode_Source)
		painter.drawImage(0, 0, self.imgBuffer)


	def sizeHint(self):
		return QSize(self.width, self.height)


class PyTraceMainWindow(QMainWindow):
	def __init__(self, qApp, width, height):
		super(PyTraceMainWindow, self).__init__()

		self.qApp = qApp
		self.width = width
		self.height = height
		self.gfxScene = QGraphicsScene()
	
	def setSphereData(self,sphereList):
		self.sphereList = sphereList

	def setCamera(self, camera):
		self.camera = camera

	def setupUi(self):
		if not self.objectName():
			self.setObjectName(u"PyTrace")
		self.resize(self.width + 25, self.height + 25)
		self.setWindowTitle("CENG488 PyTrace")
		self.setStyleSheet("background-color:black;")
		self.setAutoFillBackground(True)

		# set centralWidget
		self.centralWidget = QWidget(self)
		self.centralWidget.setObjectName(u"CentralWidget")

		# create a layout to hold widgets
		self.horizontalLayout = QHBoxLayout(self.centralWidget)
		self.horizontalLayout.setObjectName(u"horizontalLayout")
		self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

		# setup the gfxScene
		self.gfxScene.setItemIndexMethod(QGraphicsScene.NoIndex)

		# create a paint widget
		self.paintWidget = PaintWidget(self.width, self.height)
		self.paintWidget.setGeometry(QRect(0, 0, self.width, self.height))
		self.paintWidgetItem = self.gfxScene.addWidget(self.paintWidget)
		self.paintWidgetItem.setZValue(0)

		# create a QGraphicsView as the main widget
		self.gfxView = QGraphicsView(self.centralWidget)
		self.gfxView.setObjectName(u"GraphicsView")

		# assign our scene to view
		self.gfxView.setScene(self.gfxScene)
		self.gfxView.setGeometry(QRect(0, 0, self.width, self.height))

		# add widget to layout
		self.horizontalLayout.addWidget(self.gfxView)

		# set central widget
		self.setCentralWidget(self.centralWidget)

		# setup a status bar
		self.statusBar = QStatusBar(self)
		self.statusBar.setObjectName(u"StatusBar")
		self.statusBar.setStyleSheet("background-color:gray;")
		self.setStatusBar(self.statusBar)
		self.statusBar.showMessage("Ready...")

	def castRay(self, hcoord : HCoord):
		camera_hcoord = HCoord(self.camera.posX,self.camera.posY,0,0)
		#Camera -> point , Vector
		ray_vector = hcoord.subtract(camera_hcoord)
		print (ray_vector)
		for sphere_data in self.sphereList:
			#Camera -> sphere center, vector
			sphere = Sphere(sphere_data["radius"], sphere_data["posX"], sphere_data["posY"], sphere_data["posZ"])
			camera_sphere_vector = [sphere.posX - camera.posX, sphere.posY - camera.posY, sphere.posZ - camera.posZ ]
			#t =  dot(camera_sphere_vector, ray_vector) 
			#sphere - self.camera
			
		return 0
	

	def drawRay(self):
		for y in range(0, self.height):
			for x in range(0, self.width):
				color = self.castRay(HCoord(x,y,0,0))
				self.paintWidget.imgBuffer.setPixelColor(x, y, color)
				self.updateBuffer()
			qApp.processEvents()

	def timerBuffer(self):
		print("Updating buffer...")
		randHue = random.random()
		randCol = QColor.fromHslF(randHue, 1.0, 0.3)

		# go through pixels
		for y in range(0, height):
			for x in range(0, width):
				self.paintWidget.imgBuffer.setPixelColor(x, y, randCol)

			# update buffer
			for z in range(0, 100000):
				pass
			self.updateBuffer()
			# don't wait for the task to finish to update the view
			qApp.processEvents()


	def updateBuffer(self):
		self.paintWidget.update()


if __name__ == "__main__":
	# setup a QApplication
	qApp = QApplication(sys.argv)
	qApp.setOrganizationName("CENG488")
	qApp.setOrganizationDomain("cavevfx.com")
	qApp.setApplicationName("PyTrace")

	# initialize scene.json
	rawJson = readJsonFile("scene.json")
	qJson = QJsonDocument(rawJson).toVariant()
	sphereList = qJson["spheres"]
	camera = Camera.fromJsonDocument(qJson["camera"])
	

	# setup main ui 
	width = 900
	height = 900
	mainWindow = PyTraceMainWindow(qApp, width, height) #initializeMainWindow(qApp, qJson["renderSettings"])
	mainWindow.setupUi()
	mainWindow.show()
	mainWindow.setCamera(camera)
	mainWindow.setSphereData(sphereList)

	mainWindow.drawRay()
	# an example of writing to buffer
	"""
	mainTimer = QTimer()
	mainTimer.timeout.connect(mainWindow.timerBuffer)
	mainTimer.start(2000)
	"""
	# enter event loop
	sys.exit(qApp.exec_())