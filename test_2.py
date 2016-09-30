#coding:utf8
import wx


class ExamplePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.quote = wx.StaticText(self, label="Your quote :", pos=(20, 30))

        # A multiline TextCtrl - This is here to show how the events work in this program, don't pay too much attention to it
        self.logger = wx.TextCtrl(self, pos=(300,20), size=(200,300), style=wx.TE_MULTILINE | wx.TE_READONLY)

        # A button
        self.button =wx.Button(self, label="Save", pos=(200, 325))
        self.Bind(wx.EVT_BUTTON, self.OnClick,self.button)

        # the edit control - one line version.
        self.lblname = wx.StaticText(self, label="Your name :", pos=(20,60))
        self.editname = wx.TextCtrl(self, value="Enter here your name", pos=(150, 60), size=(140, -1))
        # value后接默认显示内容, size参数分别为长度,宽度.宽度为-1时自动分配大小
        self.Bind(wx.EVT_TEXT, self.EvtText, self.editname)  # 用于记录日志,文本改变就记录
        self.Bind(wx.EVT_CHAR, self.EvtChar, self.editname)  # 任意键盘按键被按下就记录

        # the combobox Control
        self.sampleList = ['friends', 'advertising', 'web search', 'Yellow Pages']
        self.lblhear = wx.StaticText(self, label="How did you hear from us ?", pos=(20, 90))
        self.edithear = wx.ComboBox(self, pos=(195, 90), size=(95, -1), choices=self.sampleList, style=wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.edithear)  # wx.EVT_COMBOBOX会在改变选项时写入日志
        self.Bind(wx.EVT_TEXT, self.EvtText,self.edithear)

        # Checkbox
        self.insure = wx.CheckBox(self, label="Do you want Insured Shipment ?", pos=(20,180))
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, self.insure)

        # Radio Boxes
        radioList = ['blue', 'red', 'yellow', 'orange', 'green', 'purple', 'navy blue', 'black', 'gray']
        rb = wx.RadioBox(self, label="What color would you like ?", pos=(20, 210), choices=radioList,  majorDimension=3,
                         style=wx.RA_SPECIFY_COLS)
        # RadioBox参数 标题,位置,选项列表,每排个数,选择方式.
        self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox, rb)  # 每次改变一次选择,RADIOBOX便会将改变信息写入日志.

    def EvtRadioBox(self, event):
        self.logger.AppendText('EvtRadioBox: %d\n' % event.GetInt())

    def EvtComboBox(self, event):
        self.logger.AppendText('EvtComboBox: %s\n' % event.GetString())

    def OnClick(self, event):
        self.logger.AppendText(" Click on object with Id %d\n" % event.GetId())

    def EvtText(self, event):
        self.logger.AppendText('EvtText: %s\n' % event.GetString())

    def EvtChar(self, event):
        self.logger.AppendText('EvtChar: %d\n' % event.GetKeyCode())
        event.Skip()

    def EvtCheckBox(self, event):
        self.logger.AppendText('EvtCheckBox: %d\n' % event.Checked())


app = wx.App(False)
frame = wx.Frame(None)
panel = ExamplePanel(frame)
frame.Show()
app.MainLoop()