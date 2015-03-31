# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fo_tag_demo.ui'
#
# Created: Thu Mar 26 19:22:57 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!


"""
Simple UI to test the tagger.
You need Qt to run this.

"""

from PyQt4 import QtCore, QtGui
import sys
import fo_tag

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.tagger = fo_tag.FaroeseTagger()

    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(382, 289)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tag_btn = QtGui.QPushButton(Form)
        self.tag_btn.setObjectName(_fromUtf8("tag_btn"))
        self.verticalLayout.addWidget(self.tag_btn)
        self.input_txt = QtGui.QPlainTextEdit(Form)
        self.input_txt.setObjectName(_fromUtf8("input_txt"))
        self.verticalLayout.addWidget(self.input_txt)
        self.output_txt = QtGui.QPlainTextEdit(Form)
        self.output_txt.setObjectName(_fromUtf8("output_txt"))
        self.output_txt.setFocusPolicy(QtCore.Qt.NoFocus)
        self.verticalLayout.addWidget(self.output_txt)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "fo_tag", None))
        self.tag_btn.setText(_translate("Form", "Tag", None))
        self.tag_btn.clicked.connect(self.tag)

    def tag(self):
        print(self.input_txt.toPlainText())

        taggedSent = self.tagger.tagSent(self.input_txt.toPlainText())
        output = ''

        
        for word, tag in taggedSent:
            output += word+'/'+tag+' '

        self.output_txt.setPlainText(output)




if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = Ui_Form()
    ex.show()
    sys.exit(app.exec_())

