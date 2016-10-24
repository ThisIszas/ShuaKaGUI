# -*-coding:utf-8-*-
# http://blog.csdn.net/g975291783/article/details/38351983
import wx
import shuaka


class MyFrame(wx.Frame):
    def __init__(self, parent, title, size):
        wx.Frame.__init__(self, parent, title=title, size=size)


class BasePanel(wx.Panel):
    def __init__(self, parent):
        self.count = []
        self.time2 = 0
        wx.Panel.__init__(self, parent)

        self.quote = wx.StaticText(self, label=" Hi, it's really nice that you can use this small program. ",
                                   pos=(0, 20))
        self.logger = wx.TextCtrl(self, pos=(5, 180), size=(465, 240), style=wx.MULTIPLE | wx.TE_READONLY)

        self.confirm_button = wx.Button(self, label=u"确定", pos=(160, 86))
        self.Bind(wx.EVT_BUTTON, self.confirm_button_fun, self.confirm_button)

        self.user_name = wx.StaticText(self, label=u"用户名:", pos=(5, 65))
        self.edit_name = wx.TextCtrl(self, value=u"在此输入用户名", pos=(48,60))

        self.password_label = wx.StaticText(self, label=u"密 码", pos=(5, 95))
        self.password = wx.TextCtrl(self, value=u"", pos=(48, 90), style=wx.TE_PASSWORD)

    def inquiry_panel(self, event):
        self.choice = [u'早操刷卡次数', u'体育课刷卡次数', u'平时刷卡次数']
        self.lal_choice = wx.StaticText(self, label=u'选择要进行的操作', pos=(5, 125))
        self.edit_choice = wx.ComboBox(self, pos=(5, 145), size=(95, -1), choices=self.choice, style=wx.CB_DROPDOWN)
        self.choice_confirm = wx.Button(self, label=u"确定", pos=(106, 142))
        self.select_detail = wx.Button(self, label=u"查询详细", pos=(196, 142))
        self.Bind(wx.EVT_BUTTON, self.choice_confirm_buttons, self.choice_confirm)
        self.Bind(wx.EVT_BUTTON, self.show_detail, self.select_detail)

    def confirm_button_fun(self, event):
        self.logger.AppendText(u'用户名和密码已输入\n')
        tr_uesrname = self.edit_name.GetRange(0, 10)
        tr_password = self.password.GetRange(0, 16)
        flag = shuaka.get_info(tr_uesrname, tr_password)
        if flag == "error101":
            self.logger.AppendText(u"账号或密码错误,请重新输入.\n")
            return 0
        self.logger.AppendText(u"验证成功,请稍等.\n\n")
        name = flag
        self.logger.AppendText(u'姓名:' + name + u'     学号:' + tr_uesrname + '\n\n')
        if self.time2 == 0:
            self.inquiry_panel(self)
        self.time2 += 1

    def choice_confirm_buttons(self, event):
        word = self.edit_choice.GetSelection()
        value = self.edit_choice.GetItems()[word]
        if value == u'早操刷卡次数':
            zao_cap_url = 'http://172.16.51.37/personQueryZC_personalDetailQuery.html'
            self.count = shuaka.zaocao(zao_cap_url, 0)
            self.logger.AppendText(u'\n早操刷卡有效次数为:' + str(self.count[1]) + u" 无效次数为:" + \
                                   str(self.count[0]-self.count[1]) + u" 总数为:" + str(self.count[0]) + '\n\n')

        elif value == u'体育课刷卡次数':
            club_sk_url = "http://172.16.51.37/personJLBQueryZC_personalJLBDetailQuery.html"
            self.count = shuaka.shangke(club_sk_url, 0)
            self.logger.AppendText(u'\n体育课刷卡有效次数为:' + str(self.count[1]) + u" 无效次数为:" + \
                                   str(self.count[0]-self.count[1]) + u" 总数为:" + str(self.count[0]) + '\n\n')

        elif value == u'平时刷卡次数':
            stsuzhi_sk_url = "http://172.16.51.37/attendanceSTTZ_list.html"
            zizhuxuexi_sk_url = "http://172.16.51.37/attendanceZZXX_list.html"
            count_1 = shuaka.pingshishuaka_1(stsuzhi_sk_url, 0)
            count_2 = shuaka.pingshishuaka_2(zizhuxuexi_sk_url, 0)
            count = count_1[0] + count_2[0]
            self.logger.AppendText(u'\n身体素质拓展刷卡有效次数为:' + str(count_1[1]) + u" 无效次数为:" + \
                                   str(count_1[0] - count_1[1]) + '\n')
            self.logger.AppendText(u'自主学习刷卡有效次数为:' + str(count_2[1]) + u" 无效次数为:" + \
                                   str(count_2[0] - count_2[1]) + '\n')
            self.logger.AppendText(u'总有效次数为:' + str(count_1[1] + count_2[1]) + u' 总次数为:' + str(count) \
                                   + u' 总无效次数为:' + str(count-count_1[1]-count_2[1])+'\n\n')

    def show_detail(self, event):
        word = self.edit_choice.GetSelection()
        value = self.edit_choice.GetItems()[word]
        deatils = []
        all = []
        if value == u'早操刷卡次数':
            zao_cap_url = "http://172.16.51.37/personQueryZC_personalDetailQuery.html"
            deatils = shuaka.show_detail(zao_cap_url)
            self.logger.AppendText('\n')
            for each in deatils:
                for each_2 in each:
                    self.logger.AppendText(each_2 + " ")
                self.logger.AppendText('\n')
        elif value == u'体育课刷卡次数':
            club_sk_url = "http://172.16.51.37/personJLBQueryZC_personalJLBDetailQuery.html"
            deatils = shuaka.show_detail(club_sk_url)
            self.logger.AppendText('\n')
            for each in deatils:
                for each_2 in each:
                    self.logger.AppendText(each_2 + " ")
                self.logger.AppendText('\n')
        elif value == u'平时刷卡次数':
            stsuzhi_sk_url = "http://172.16.51.37/attendanceSTTZ_list.html"
            zizhuxuexi_sk_url = "http://172.16.51.37/attendanceZZXX_list.html"
            self.logger.AppendText(u"身体素质拓展:" + '\n')
            deatils = shuaka.show_detail(stsuzhi_sk_url)
            deatils_2 = shuaka.show_detail(zizhuxuexi_sk_url)
            for each in deatils:
                for each_2 in each:
                    self.logger.AppendText(each_2 + " ")
                self.logger.AppendText('\n')
            self.logger.AppendText(u'自主学习:' + '\n')
            for each in deatils_2:
                for each_2 in each:
                    self.logger.AppendText(each_2 + " ")
                self.logger.AppendText('\n')

    def evt_text(self, event):
        self.logger.AppendText('EvtText: %s\n' % event.GetString())

    def evt_char(self, event):
        self.logger.AppendText('EvtChar: %d\n' % event.GetKeyCode())
        event.Skip()

    def evt_combo_box(self, event):
        self.logger.AppendText(u'操作项目为: %s\n' % event.GetString())
        return event.GetString()

app = wx.App(False)
frame = MyFrame(None, u'好好学习,天天刷卡', (490,470))
panel = BasePanel(frame)
frame.Show()
app.MainLoop()
