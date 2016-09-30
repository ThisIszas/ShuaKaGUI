#coding:utf-8
import wx
import os


class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(200, 200))
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.CreateStatusBar()  # a statusBar in the bottom of the window

        filemenu = wx.Menu()  # create a file menu

        file_open = filemenu.Append(wx.ID_OPEN, '&Open', "Open a file.")
        file_about = filemenu.Append(wx.ID_ABOUT, '&About', 'A information about this program.')
        filemenu.AppendSeparator()  # Add a  separator line to menuBar.
        file_exit = filemenu.Append(wx.ID_EXIT, '&Exit', "Terminate the program")

        menubar = wx.MenuBar()  # create a menuBar
        menubar.Append(filemenu, "&File")
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.onabout, file_about)
        self.Bind(wx.EVT_MENU, self.onexit, file_exit)
        self.Bind(wx.EVT_MENU, self.onopen, file_open)
    # ------------------------------------------------------------------------------------------
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.buttons = []

        for i in range(0, 6):
            self.buttons.append(wx.Button(self, -1, "Button &" + str(i)))
            self.sizer2.Add(self.buttons[i], 1, wx.EXPAND)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.control, 1, wx.EXPAND)  # Add control module to sizer panel
        self.sizer.Add(self.sizer2, 0, wx.EXPAND)  # Add sizer2 to sizer

        self.SetSizer(self.sizer)  # 调用SetSizer()方法告诉你的窗口或框架去使用这个sizer。  38-40为布局模块
        self.SetAutoLayout(1)  # 告诉你的窗口使用sizer去为你的控件计算位置和大小
        self.sizer.Fit(self)  # 用sizer.Fit()告诉sizer去计算所有控件的初始位置和大小
    # ------------------------------------------------------------------------------------------
        self.Show(True)
        # create file menu --> add item to fileMenu --> create menuBar --> add fileMenu to menuBar -->
        # set menuBar

    def onabout(self, event):
        dlg = wx.MessageDialog(self, "A small text editor", "about sample editor", wx.OK)
        dlg.ShowModal()  # show dialog
        dlg.Destroy()  # destroy the message box

    def onexit(self, event):
        dlg = wx.MessageDialog(self, "This program will exit soon", "WARNING!", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        self.Close(True)  # exit the program

    def onopen(self, event):
        self.dirname = ""
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)  # create a dialog
        if dlg.ShowModal() == wx.ID_OK:  # After create a dialog then show it.
            self.dirname = dlg.GetDirectory()
            self.filename = dlg.GetFilename()
            f = open(os.path.join(self.dirname, self.filename), 'r')
            self.control.SetValue(f.read())
            f.close()
        dlg.Destroy()

if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame(None, "small text editor")
    app.MainLoop()
