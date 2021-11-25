#!/usr/bin/env python
# -*-coding:utf8-*-
# !/bin/bash

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Notice
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Tree Setting
# - AlternatingRowColors : depending on situation
# - selectionBehavior   : SelectRows
# - indentation         : 15
# - rootIsDecorated     : Check
# - uniformRowHeights   : Check
# - animated            : Check
# - headerVisible       : True
# - headerDefaultSectionSize    : 200
# - headerMinimumSectionSize    : 125
# - headerStretchLastSection    : Check

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# <1> Header
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Common
import os
path_NextLib_PyEasyTree_tree_py = os.path.dirname(os.path.abspath(__file__))

# System
# from NextLib.cmn import *
from NextLib.qt4 import *

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# <2> Class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TREE_ITEM_CLASS와 TREE_DATA2_CLASS는 저장하는 데이터는 다르지만 위치를 가리킴
class TREE_ITEM_CLASS:
    def __init__(self, item=None):
        # Item
        self.item       = item
        self.childItems = []
        return

class TREE_DATA_CLASS:
    def __init__(self, name="", value=""):
        # Data
        self.name       = name
        self.value      = value
        self.childData  = []

        # bCheck
        self.iCheck     = -1     # -1: None, 0: False, 1:True

        # Widget Type
        self.arrWidgetType = []  # 0:"Text(no editable)", 1:"Edit", 2:"Combo", 3:"Button", 4:"Radio"
        # (ex) column이 2개 일 경우: [0, 0] or ["Text", "Edit"]

        # self.arrWidgetData = []
        return

# ------------------------------------------------------------------------------
class TREE_CLASS:
    def __init__(self):
        # Common
        self.wgTree     = None

        self.allItems   = []
        self.allData    = []
        return

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Main
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # None

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # [1] New/End
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def New(self, wgTree=None):
        if wgTree is None:
            self.wgTree = QTreeWidget()
        else:
            self.wgTree = wgTree

        # Update
        self.Update()

        # Set Type
        self.Set_ListType(1)
        self.Set_Tree_Style()
        self.Set_Tree_Item_Height()
        return

    # Setting
    def Set_Tree_Style(self):   # Set Default Style
        self.wgTree.setAnimated(True)
        return

    def Set_Tree_Item_Height(self, size=23):
        strStyle =  """QTreeView{
                            show-decoration-selected: 1;
                        }
                        QTreeView::item{
                            height: %dpx;
                            border:  1px solid #d9d9d9;
                            border-top-color:   transparent;
                            border-bottom-color:transparent;
                            border-left-color:  transparent;                      
                        }
                        QTreeView::item:hover {
                            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e7effd, stop: 1 #cbdaf1);
                            border: 1px solid #bfcde4;
                        }
                        QTreeView::item:selected {
                            border: 1px solid #567dbc;
                        }
                        QTreeView::item:selected:active{
                            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6ea1f1, stop: 1 #567dbc);
                        }
                        QTreeView::item:selected:!active {
                            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6b9be8, stop: 1 #577fbf);
                        }
                        """ % size
        self.wgTree.setStyleSheet(strStyle)
        return

    def Set_ListType(self, iType=0):
        if iType == 0:
            Connect_itemDoubleClicked_Tree(self.wgTree, DoubleClick_Item_Tree)
        elif iType == 1:
            Connect_itemDoubleClicked_Tree(self.wgTree, DoubleClick_Item_List)
        return

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # [2] Run
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # [@] Functions
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Tree Widget
    def Clear(self):
        if self.wgTree is not None:
            # Delete all
            self.wgTree.clear()

            self.allItems = []
            self.allData = []

            # Update
            self.Update()
        return

    # Update
    def Update(self):
        self.allItems, self.allData = self.Get_AllData_List()
        return

    # --------------------------------------------------------------------------
    # Get Item
    # --------------------------------------------------------------------------
    # Get Item
    def Get_Item(self, pos=[], opt=0):  # 0: Normal, 1: Parent
        num = len(pos)
        if num == 0 or len(self.allItems) <= pos[0]:
            return -1  # False
        #
        if num == 1:
            if opt == 1: return -1  # False
            item = self.allItems[pos[0]].item
        else:
            if num == 2 and opt == 1:
                item = self.allItems[pos[0]].item
            else:
                arrChildItem = self.allItems[pos[0]].childItems
                pos = pos[1:]
                item = self.Get_SubItem(arrChildItem, pos, opt)
        return item

    def Get_SubItem(self, arrChildItem, pos=[], opt=0):
        num = len(pos)
        if num == 0 or len(arrChildItem) <= pos[0]:
            return -1  # False
        #
        if num == 1:
            if opt == 1:
                return -1  # False
            item = arrChildItem[pos[0]].item
        else:
            if num == 2 and opt == 1:
                item = arrChildItem[pos[0]].item
            else:
                childItem = arrChildItem[pos[0]].childItems
                pos = pos[1:]
                item = self.Get_SubItem(childItem, pos, opt)
        return item

    # --------------------------------------------------------------------------
    # Get Position
    # --------------------------------------------------------------------------
    # Get_Item_Pos (v2.0)
    def Get_Pos(self, item):  # Find_ItemList
        arrFind = []
        for jj, dd in enumerate(self.allItems):
            if dd.item == item:
                Add_List(arrFind, jj)
                arrFind.reverse()   # why reverse??
                return arrFind
            else:
                arrFindChild = self.Get_Child_Pos(dd.childItems, item)
                if len(arrFindChild) > 0:
                    Add_List(arrFindChild, jj)
                    arrFindChild.reverse()  # why reverse??
                    return arrFindChild
        arrFind.reverse()   # why reverse??
        return arrFind

    # Get_ChildItem_Pos (v2.0)
    def Get_Child_Pos(self, childItems, item):
        arrFind = []
        for jj, dd in enumerate(childItems):
            if dd.item == item:
                Add_List(arrFind, jj)
                return arrFind
            else:
                arrFindChild = self.Get_Child_Pos(dd.childItems, item)
                if len(arrFindChild) > 0 :
                    Add_List(arrFindChild, jj)
                    return arrFindChild
        return arrFind

    # --------------------------------------------------------------------------
    # Current/Select
    # --------------------------------------------------------------------------
    def Get_Cur_Pos(self):
        item = Get_CurItem(self.wgTree)
        if not item:
            return []
        arrPos = self.Get_Pos(item)
        return arrPos

    def Get_CurItem(self):
        item = self.wgTree.currentItem()
        if item is None:
            item = -1
        return item

    def Get_CurIndex(self):
        item = Get_CurItem(self.wgTree)
        if item != -1:
            return Get_ItemIndex(item)
        return -1

    def Get_CurText(self, column=1):
        arrPos = self.Get_Cur_Pos()
        curText = self.Get_Text(arrPos, column)
        return str(curText)

    def Set_Select(self, pos=[], column=0):
        item = self.Get_Item(pos)
        self.wgTree.setCurrentItem(item, column)
        item.setSelected(True)
        return

    def Get_Selected(self):
        return self.wgTree.selectedItems()

    def Get_Selected_Index(self):
        arrItem = self.wgTree.selectedItems()
        arrIndex = []
        for dd in arrItem:
            arrIndex.append(Get_ParentItemIndex(dd))
        return arrIndex

    # --------------------------------------------------------------------------
    # Item (Check)
    # --------------------------------------------------------------------------
    # (구) Check_Pos_Level
    def Check_Pos(self, pos=[], checkPos=[], bChild=False):  # 서로 같은 등급인지 검사
        if not bChild and len(pos) != len(checkPos):
            return False
        for ii, dd in enumerate(checkPos):
            if ii < len(checkPos):
                if ii >= len(pos):
                    return False
                if dd != "*" and dd != pos[ii]:
                    return False
            else:
                break
        return True

    def Check_Pos_Item(self, item, checkPos=[], bChild=False):
        getPos = self.Get_Pos(item)
        return self.Check_Pos(getPos, checkPos, bChild)

    # --------------------------------------------------------------------------
    # Item (RootItem)
    # --------------------------------------------------------------------------
    def Get_RootNum(self):
        return self.wgTree.topLevelItemCount()

    def Get_Root(self, index):
        treeItem = self.wgTree.topLevelItem(index)
        # 아래 코드는 위와 같은 결과임
        # treeItem = self.wgTree.itemFromIndex(self.wgTree.model().index(index, 0))
        return treeItem

    def Get_RootIndex(self, pos=[]):
        item = self.Get_Item(pos)
        if item == -1:
            return
        index = self.wgTree.indexOfTopLevelItem(item)
        return int(index)

    # --------------------------------------------------------------------------
    # Item (Value)
    # --------------------------------------------------------------------------
    def Set_Text(self, pos=[], column=0, strText="NewNamed"):
        item = self.Get_Item(pos)
        if item == -1:
            return
        if strText:
            item.setText(column, strText)
        return

    def Get_Text(self, pos=[], column=0):
        item = self.Get_Item(pos)
        return "" if item == -1 else str(item.text(column))

    def Get_Check(self, pos=[], column=0):
        item = self.Get_Item(pos)
        iState = item.checkState(column)
        if iState == 0:  # 0: Qt.Unchecked
            return False
        elif iState == 1:  # 1: Qt.Checked
            return False
        elif iState == 2:  # 2: Qt.Checked
            return True
        return

    def Set_Check(self, pos=[], column=0, bChecked=True):
        # Init
        item = self.Get_Item(pos)

        # Check
        if item == -1:
            return

        if bChecked:
            bState = Qt.Checked
        else:
            bState = Qt.Unchecked
        item.setCheckState(column, bState)
        return

    # --------------------------------------------------------------------------
    # Item (Display)
    # --------------------------------------------------------------------------
    # def Show_Item(self, item, bState=True):
    #     item.setHidden(bState)
    #     return
    #
    # def Enable_Item(self, item, bState=True):
    #     item.setDisabled(not bState)
    #     return
    #
    # def Expand_Item(self, item, bState=True):
    #     item.setExpanded(bState)
    #     return

    # --------------------------------------------------------------------------
    def Show(self, pos=[], bState=True):
        item = self.Get_Item(pos)
        if item == -1:
            return
        item.setHidden(not bState)
        return

    def Hide(self, pos=[], bState=True):
        item = self.Get_Item(pos)
        if item == -1:
            return
        item.setHidden(bState)
        return

    def Enable(self, pos=[], bState=True):
        item = self.Get_Item(pos)
        if item == -1:
            return
        item.setDisabled(not bState)
        return

    def Disable(self, pos=[], bState=True):
        item = self.Get_Item(pos)
        if item == -1:
            return
        item.setDisabled(bState)
        return

    def Expand(self, pos=[], bState=True):
        item = self.Get_Item(pos)
        if item == -1:
            return
        item.setExpanded(bState)
        return

    def Collapse(self, pos=[], bState=True):
        item = self.Get_Item(pos)
        if item == -1:
            return
        item.setExpanded(not bState)
        return

    def Set_Widget(self, pos=[], column=1, *widget):
        item = self.Get_Item(pos)
        if item == -1:
            return
        #
        Set_WidgetItem(item, column, *widget)
        return

    def Add_Widget(self, pos=[], column=1, *widget):
        item = self.Get_Item(pos)
        if item == -1:
            return
        #
        Add_WidgetItem(item, column, *widget)
        return

    def Add_Widget_Edit(self, pos=[], column=1, strCur=""):
        item = self.Get_Item(pos)
        wgEdit = QLineEdit()
        wgEdit.setFont(QFont("Ubuntu", 10, 50))
        wgEdit.setFrame(False)
        Set_Text(wgEdit, "")
        Set_WidgetItem(item, column, [wgEdit])
        return wgEdit

    def Add_Widget_Combo(self, pos=[], column=1, arrData=[], strCur=""):
        item = self.Get_Item(pos)
        wgCombo = QComboBox()
        wgCombo.addItems(arrData)
        # wgCombo.setMaximumWidth(200)
        wgCombo.setFont(QFont("Ubuntu", 10, 50))
        Set_CurIndex_Combo(wgCombo, -1)
        if strCur:
            Set_Text_Combo(wgCombo, strCur)
        Set_WidgetItem(item, column, [wgCombo])
        return wgCombo

    def Add_Widget_GroupButton(self, pos=[], column=1, numBtn=1, arrName=["NoName"]):
        item = self.Get_Item(pos)
        arrBtn = []
        for ii in range(numBtn):
            wgBtn = QPushButton(arrName[ii])
            # wgBtn.setMaximumWidth(200)
            arrBtn.append(wgBtn)
            arrBtn[-1].setFont(QFont("Ubuntu", 9, 50))
        Set_WidgetItem(item, column, arrBtn)
        if numBtn == 1:
            return arrBtn[0]
        return arrBtn

    def Del_Widget(self, pos=[], column=1, *widget):
        item = self.Get_Item(pos)
        if item == -1:
            return
        #
        if len(widget) == 0:
            self.wgTree.removeItemWidget(item, column)
        else:
            wgBase = self.wgTree.itemWidget(item, column)
            wgHBox = wgBase.layout()
            for dd in widget:
                wgHBox.removeWidget(dd)
        return

    def Set_Flag(self, pos=[], option=35):
        item = self.Get_Item(pos)
        if item == -1:
            return
        tmpFlag = item.flags() | option
        item.setFlags(item.flags() | tmpFlag)
        return item

    def Set_Icon(self, pos=[], path="", column=0):
        item = self.Get_Item(pos)
        if item == -1:
            return
        icon = Make_Icon(path)
        item.setIcon(column, icon)
        return

    def Set_Font(self, pos=[], column=0, fontName="Ubuntu", size=10, bold=50):  # bold: 0~50~100
        item = self.Get_Item(pos)
        if item == -1:
            return
        item.setFont(column, QFont(fontName, size, bold))
        return

    def Set_Color(self, pos=[], column=0, rgb=(0, 0, 0)):  # rgb=0~255
        item = self.Get_Item(pos)
        if item == -1:
            return
        item.setTextColor(column, QColor(rgb[0], rgb[1], rgb[2]))
        return

    def Set_BkColor(self, pos=[], column=0, rgb=(0, 0, 0)):  # rgb=0~255
        item = self.Get_Item(pos)
        if item == -1:
            return
        item.setBackground(column, QColor(rgb[0], rgb[1], rgb[2]))

    def Set_Alignment(self, pos=[], column=0, alignment=0):  # alignment =0, 1, 2, 4, 8
        item = self.Get_Item(pos)
        if item == -1:
            return
        if alignment == 1 or alignment == "LEFT":
            alignment = Qt.AlignLeft
        elif alignment == 2 or alignment == "RIGHT":
            alignment = Qt.AlignRight
        elif alignment == 4 or alignment == "CENTER":
            alignment = Qt.AlignHCenter
        else:  # AlignJustify
            alignment = Qt.AlignJustify
        item.setTextAlignment(column, alignment)
        return

    # --------------------------------------------------------------------------
    # Load/Save/Paste
    # --------------------------------------------------------------------------
    def Load(self, path=""):
        allData = Load_Pickle(path)
        return allData

    def Save(self, path=""):
        # Reload
        self.Update()
        # Save
        Save_Pickle(path, self.allData)
        return

    def Paste(self, pos=[], path=""):
        loadData = Load_Pickle(path)
        lenPos = len(pos)
        if lenPos == 0:
            return
        newPos = Copy_List(pos)
        for ii, dd in enumerate(loadData):
            # Data
            newPos[-1] = pos[-1] + ii
            addItem = self.Insert(newPos, dd.name)
            addItem.setText(1, dd.value)
            self.PasteChild(newPos, dd.childData)
            # Check
            if dd.iCheck != -1:
                Set_ItemCheck(addItem, 0, dd.bCheck)
            # Set Widget List
            if len(dd.arrWidgetType) > 0:
                Set_WidgetItem(addItem, 1, Set_Widgets_List(dd.arrWidgetType))
        # Reload
        self.Update()
        return

    def PasteChild(self, pos=[], subData=[]):
        if len(subData) > 0:
            for jj, ee in enumerate(subData):
                newPos = Copy_List(pos)
                addItem = self.Add_Sub(pos, ee.name)
                if addItem is None:
                    return
                addItem.setText(1, ee.value)
                newPos.append(jj)
                self.PasteChild(newPos, ee.childData)
                # Check
                if ee.iCheck != -1:
                    Set_ItemCheck(addItem, 0, ee.bCheck)
                # Set Widget List
                if len(ee.arrWidgetType) > 0:
                    Set_WidgetItem(addItem, 1, Set_Widgets_List(ee.arrWidgetType))
        return

    # --------------------------------------------------------------------------
    # Get Data
    # --------------------------------------------------------------------------
    def Get_AllData_List(self):
        allItems   = []
        allData    = []
        numRoot = Get_RootItemNum(self.wgTree)
        for jj in range(numRoot):
            # Common
            rootItem = Get_RootItem(self.wgTree, jj)
            rootPos = self.Get_Pos(rootItem)

            # Item
            allItems.append(TREE_ITEM_CLASS(rootItem))
            allItems[-1].childItems = self.Get_ChildItem_List(rootPos)

            # Data
            rootName    = Get_ItemText(rootItem, 0)
            rootValue   = Get_ItemText(rootItem, 1)
            allData.append(TREE_DATA_CLASS(rootName, rootValue))
            allData[-1].childData = self.Get_ChildData_List(rootPos)

            # Widget Type
            allData[-1].arrWidgetType = Get_Widgets_List(rootItem, 1)
        return allItems, allData

    def Get_ChildItem_List(self, pos=[]):
        currentItem = self.Get_Item(pos, 0)
        if currentItem == -1:
            return []

        allChildItems = []
        numChild = Get_ChildItemNum(currentItem)
        for jj in range(numChild):
            # Item
            childItem = Get_ChildItem(currentItem, jj)
            childPos = self.Get_Pos(childItem)

            allChildItems.append(TREE_ITEM_CLASS(childItem))
            allChildItems[-1].childItems = self.Get_ChildItem_List(childPos)
        return allChildItems

    def Get_ChildData_List(self, pos=[]):
        currentItem = self.Get_Item(pos, 0)
        if currentItem == -1:
            return []

        arrChildData = []
        numChild = Get_ChildItemNum(currentItem)
        for jj in range(numChild):
            # Item
            childItem = Get_ChildItem(currentItem, jj)
            childPos = self.Get_Pos(childItem)

            # Data
            childName   = Get_ItemText(childItem, 0)
            childValue  = Get_ItemText(childItem, 1)
            arrChildData.append(TREE_DATA_CLASS(childName, childValue))
            arrChildData[-1].childData = self.Get_ChildData_List(childPos)

            # Widget Type
            arrChildData[-1].arrWidgetType = Get_Widgets_List(childItem, 1)
        return arrChildData

    # --------------------------------------------------------------------------
    # Add/Insert/Delete
    # --------------------------------------------------------------------------
    # Insert_Root
    def Insert_Root(self, pos=[], strText="", opt2=39):
        # opt : 현재 아이템에 추가할 것인지 하위 아이템에 추가할 것인지 확인, 0:현재, 1:하위
        if len(pos) == 0:
            return
        if len(pos) == 1:
            insItem = Insert_RootItem(self.wgTree, pos[0], opt2=opt2, title=strText)
        else:
            parent = self.Get_Item(pos, 1)
            # if parent == -1 and Get_RootItemNum(self.wgTree)==0: return
            if parent == -1:
                return
            insItem = Insert_SubItem(parent, pos[-1], opt2=opt2, title=strText)
        # Set
        insItem.setSizeHint(1, QSize(-1, 20))
        Set_ItemFont(insItem, 0, size=10, bold=90)
        # Set_ItemColor(insItem, 0, (5, 0, 0))
        # ReDraw
        # self.wgTree.updateGeometries()    >> 화면 위치가 처음으로 움직이므로 권장안함
        # Reload
        self.Update()
        return insItem

    # Insert (v1.2)
    def Insert(self, pos=[], strText="", opt=0, opt2=39, size=10, bold=70):
        # opt : 현재 아이템에 추가할 것인지 하위 아이템에 추가할 것인지 확인, 0:현재, 1:하위
        if len(pos) == 0:
            return
        if len(pos) == 1:
            insItem = Insert_RootItem(self.wgTree, pos[0] + opt, opt2=opt2, title=strText)
        else:
            parent = self.Get_Item(pos, 1)
            # if parent == -1 and Get_RootItemNum(self.wgTree)==0: return
            if parent == -1:
                return
            insItem = Insert_SubItem(parent, pos[-1] + opt, opt2=opt2,title=strText)
        # Set
        insItem.setSizeHint(1, QSize(-1, 20))
        Set_ItemFont(insItem, 0, size=size, bold=bold)
        # Reload
        self.Update()
        return insItem

    def Insert_Sub(self, pos=[], strText="", opt=0, opt2=39):
        if len(pos) == 0:
            return

        parent = self.Get_Item(pos, 0)
        if parent == -1:
            return
        insItem = Insert_SubItem(parent, -1, title=strText, opt=opt, opt2=opt2)
        insItem.setSizeHint(1, QSize(-1, 20))
        # insItem.setTextAlignment(1, Qt.AlignHCenter)
        # Reload
        self.Update()
        return insItem

    # Delete
    def Del(self, pos=[], opt=0):   # opt: 0-self, 1-child
        if len(pos) == 0:
            return
        else:
            item = self.Get_Item(pos, 0)
            if item == -1:
                return
            if opt == 0:
                Delete_Item(item)
            else:
                Delete_SubItem(item, -1)

        # Reload
        self.Update()
        return

    # Paste 함수 사용할 때 필요
    def Add(self, pos=[], strText="", opt2=0):
        addItem = self.Insert(pos, strText, opt2)
        return addItem

    def Add_Sub(self, pos=[], strText="", opt2=0):
        addItem = self.Insert_Sub(pos, strText, opt2=opt2)
        return addItem

    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Not used
    # --------------------------------------------------------------------------
    # Data (Index)
    # def Get_Data_Index(self, pos=[]):
    #     # return 값 : TREE_DATA_CLASS()
    #     if len(pos) == 0:
    #         return
    #     if len(pos) == 1:
    #         return self.data[pos[0]]
    #     else:
    #         return self.Get_ChildData_Index(self.data[pos[0]].childData, pos[1:])
    #
    # def Get_ChildData_Index(self, parentPos, pos=[]):
    #     if len(pos) == 1:
    #         return parentPos[pos[0]]
    #     else:
    #         return self.Get_ChildData_Index(parentPos[pos[0]].childData, pos[1:])
    # --------------------------------------------------------------------------


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# <3> Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Tree (Common)
def New_Tree(wgTree=None):
    if wgTree is None:
        tree = TREE_CLASS()
    else:
        tree = TREE_CLASS(wgTree)
    return tree

# Show
def Clear_Tree(wgTree):
    wgTree.clear()
    return

# Tree (Column)
def Get_CurColumn(wgTree):
    index = wgTree.currentColumn()
    return int(index)

# ------------------------------------------------------------------------------
# Tree (Connect)
# ------------------------------------------------------------------------------
def Connect_Tree(wgTree, signal, func, *argv):
    funcConnect = Get_Func_Connect(wgTree, func, *argv)
    if signal == 0 or signal == "itemClicked":
        wgTree.itemClicked.connect(funcConnect)
    elif signal == 1 or signal == "itemDoubleClicked":
        wgTree.itemDoubleClicked.connect(funcConnect)
    else:
        print("Cannot find signal function")
    return

# 언제 이벤트가 발생하는지 확인이 안됨
# def Connect_itemActivated_Tree(wgTree, func, *argv):  # argv: item, column
#     funcConnect = Get_Func_Connect(wgTree, func, *argv)
#     wgTree.itemActivated.connect(funcConnect)
#     return

def Connect_ItemChanged_Tree(wgTree, func, *argv):  # argv: old item, new item
    funcConnect = Get_Func_Connect(wgTree, func, *argv)
    wgTree.itemChanged.connect(funcConnect)
    return

def Connect_currentItemChanged_Tree(wgTree, func, *argv):  # argv: old item, new item
    funcConnect = Get_Func_Connect(wgTree, func, *argv)
    wgTree.currentItemChanged.connect(funcConnect)
    return

def Connect_itemClicked_Tree(wgTree, func, *argv):  # argv:  item, column
    funcConnect = Get_Func_Connect(wgTree, func, *argv)
    wgTree.itemClicked.connect(funcConnect)
    return

def Connect_itemDoubleClicked_Tree(wgTree, func, *argv):  # argv:  item, column
    funcConnect = Get_Func_Connect(wgTree, func, *argv)
    wgTree.itemDoubleClicked.connect(funcConnect)
    return

def DoubleClick_Item_List(item, column):
    # ItemIsDragEnabled 에 따라서 column 0번의 텍스트가 수정되고 안되고 결정
    # (item을 이동(drag)하지 않는다는 조건으로)
    if Qt.ItemFlag(item.flags()) & Qt.ItemIsDragEnabled == 4:
        if column == 0:
            item.setFlags(item.flags() & (~Qt.ItemIsEditable))
        elif column == 1:
            item.setFlags(item.flags() | Qt.ItemIsEditable)
    else:
        if Qt.ItemFlag(item.flags()) & Qt.ItemIsEditable == 2:
            item.setFlags(item.flags() | Qt.ItemIsEditable)

    # if column == 0:
    #     if Qt.ItemFlag(item.flags()) & Qt.ItemIsEditable == 2:
    #         if Qt.ItemFlag(item.flags()) & Qt.ItemIsDragEnabled == 4:
    #             item.setFlags(item.flags() & (~Qt.ItemIsEditable))
    #         else:
    #             item.setFlags(item.flags() | Qt.ItemIsEditable)
    # elif column == 1:
    #     item.setFlags(item.flags() | Qt.ItemIsEditable)
    return

def DoubleClick_Item_Tree(item, column):
    item.setFlags(item.flags() | Qt.ItemIsEditable)
    return

def Connect_itemEntered_Tree(wgTree, func, *argv):  # argv: item, column
    funcConnect = Get_Func_Connect(wgTree, func, *argv)
    wgTree.itemEntered.connect(funcConnect)
    return

# ------------------------------------------------------------------------------
# Item (Common)
# ------------------------------------------------------------------------------
def Get_TreeWidget(item):
    return item.treeWidget()

# ------------------------------------------------------------------------------
# Item (Add/Insert/Delete)
# ------------------------------------------------------------------------------
# Insert
def Insert_RootItem(wgTree, index=-1, title="New", opt2=39):
    # 참고: 이 함수에서는 강제로 위치를 변경해 줘야함 (itemSelectionChanged 실행 안됨)
    # 39 = 1 + 2 + 4 + 32   # 35 : column 0,1 모두 변경
    # 33 : 1 + 32 - 수정 불가능한 아이템
    """ Qt.NoItemFlags	        0
        Qt.ItemIsSelectable	    1
        Qt.ItemIsEditable	    2
        Qt.ItemIsDragEnabled	4
        Qt.ItemIsDropEnabled	8
        Qt.ItemIsUserCheckable	16
        Qt.ItemIsEnabled	    32
        Qt.ItemIsTristate       64
    """
    totalCount = wgTree.topLevelItemCount()
    rootItem = QTreeWidgetItem()
    rootItem.setFlags(Qt.ItemFlag(opt2))

    if index == -1 or index >= totalCount:
        wgTree.addTopLevelItem(rootItem)
    else:
        wgTree.insertTopLevelItem(index, rootItem)

    # Font
    rootItem.setText(0, title)
    return rootItem

def Insert_SubItem(rootItem, index=-1, title="NewChild", opt=0, opt2=39):
    totalCount = rootItem.childCount()
    #
    childItem = QTreeWidgetItem()
    # childItem.setFlags(childItem.flags() | Qt.ItemIsSelectable | Qt.ItemIsEditable)
    childItem.setFlags(Qt.ItemFlag(opt2))
    if index == -1 or index >= totalCount:
        rootItem.addChild(childItem)
    else:
        rootItem.insertChild(index+opt, childItem)
    #
    childItem.setText(0, title)
    return childItem

# Delete
def Delete_Item(item):
    if item == -1:
        return -1
    wgTree = Get_TreeWidget(item)
    parentItem = Get_ParentItem(item)
    #
    if parentItem == -1 or not parentItem:
        ##### 참고: 이 함수에서 'itemSelectionChanged'함수가 자동 실행되므로
        ####        강제로 현재 위치를 변경하지 말 것
        index = Get_RootItemIndex(item)
        if index == -1:
            wgTree.clear()
        else:
            wgTree.takeTopLevelItem(index)
    else:
        subIndex = parentItem.indexOfChild(item)
        Delete_SubItem(parentItem, subIndex)
    return

def Delete_SubItem(parentItem, index=-1):
    if parentItem == -1:
        return
    if index == -1:
        num = parentItem.childCount()
        for ii in reversed(range(num)):
            childItem = parentItem.child(ii)
            Delete_SubItem(childItem)
            parentItem.removeChild(childItem)
    else:
        parentItem.takeChild(index)
    return

def Delete_CurItem(wgTree):
    item = Get_CurItem(wgTree)
    Delete_Item(item)
    return

# ------------------------------------------------------------------------------
# Item (Current)
# ------------------------------------------------------------------------------
def Get_CurItem(wgTree):
    item = wgTree.currentItem()
    if item is None:
        item = -1
    return item

def Get_CurItemIndex(wgTree):
    item = Get_CurItem(wgTree)
    if item != -1:
        return Get_ItemIndex(item)
    return -1

# ------------------------------------------------------------------------------
# Item (Select)
# ------------------------------------------------------------------------------
def Set_SelectItem(item, column=0):
    wgTree = Get_TreeWidget(item)
    wgTree.setCurrentItem(item, column)
    item.setSelected(True)
    return

def Get_SelectedItems(wgTree):
    arrItem = wgTree.selectedItems()
    return arrItem

def Get_SelectedItems_Index(wgTree):
    arrItem = wgTree.selectedItems()
    arrIndex = []
    for dd in arrItem:
        arrIndex.append(Get_ParentItemIndex(dd))
    return arrIndex

# ------------------------------------------------------------------------------
# Item (Info)
# ------------------------------------------------------------------------------
def Get_ItemIndex(item):    # Parent에 대한 index임
    wgTree = Get_TreeWidget(item)
    index = wgTree.indexFromItem(item).row()
    return int(index)

# Child Item
def Get_ChildItemNum(parentItem):
    return parentItem.childCount()

def Get_ChildItem(parentItem, index):
    if Get_ChildItemNum(parentItem) <= index:
        return -1
    childItem = parentItem.child(index)
    return childItem

def Get_ChildItemIndex(parentItem, childItem):
    return parentItem.indexOfChild(childItem)

# Parent Item
def Get_ParentItemIndex(childItem):
    wgTree = Get_TreeWidget(childItem)
    index = wgTree.indexFromItem(childItem).parent().row()
    return int(index)

def Get_ParentItem(childItem):
    if Get_ParentItemIndex(childItem) == -1:
        return -1
    parentItem = childItem.parent()
    return parentItem

# ------------------------------------------------------------------------------
# Item (RootItem)
# ------------------------------------------------------------------------------
def Get_RootItemNum(wgTree):
    return wgTree.topLevelItemCount()

def Get_RootItem(wgTree, index):
    treeItem = wgTree.topLevelItem(index)
    # 아래 코드는 위와 같은 결과임
    # treeItem = wgTree.itemFromIndex(wgTree.model().index(index, 0))
    return treeItem

def Get_RootItemIndex(item):
    wgTree = item.treeWidget()
    index = wgTree.indexOfTopLevelItem(item)
    return int(index)

# ------------------------------------------------------------------------------
# Item (Value)
# ------------------------------------------------------------------------------
# Text
def Set_ItemText(item, column=0, strText="NewNamed"):
    item.setText(column, strText)
    return

def Get_ItemText(item, column=0):
    return str(item.text(column))

# Check
def Get_ItemCheck(item, column=0):
    iState = item.checkState(column)
    if iState == 0:     # 0: Qt.Unchecked
        return False
    elif iState == 1:   # 1: Qt.Checked
        return False
    elif iState == 2:   # 2: Qt.Checked
        return True
    return

def Set_ItemCheck(item, column=0, bChecked=True):
    if bChecked:
        bState = Qt.Checked
    else:
        bState = Qt.Unchecked
    item.setCheckState(column, bState)
    return

# ------------------------------------------------------------------------------
# Item (Display)
# ------------------------------------------------------------------------------
def Show_Item(item, bState=True):
    item.setHidden(not bState)
    return

def Hide_Item(item, bState=True):
    item.setHidden(bState)
    return

def Enable_Item(item, bState=True):
    item.setDisabled(not bState)
    return

def Disable_Item(item, bState=True):
    item.setDisabled(bState)
    return

def Expand_Item(item, bState=True):
    item.setExpanded(bState)
    return

def Collapse_Item(item, bState=True):
    item.setExpanded(not bState)
    return

def Set_WidgetItem(item, column=1, widget=[]):
    wgTree = Get_TreeWidget(item)

    if len(widget) > 0:
        wgBase = QWidget()
        wgHBox = QHBoxLayout()
        wgHBox.setSpacing(1)
        wgHBox.setMargin(0) # setMargin(1)
        for dd in widget:
            wgHBox.addWidget(dd)
        #
        # wgHBox.addStretch(1)    ###
        wgBase.setLayout(wgHBox)
        wgTree.setItemWidget(item, column, wgBase)
    return

def Add_WidgetItem(item, column=1, widget=[]):
    wgTree = Get_TreeWidget(item)
    if len(widget) > 0:
        wgBase = wgTree.itemWidget(item, column)
        if wgBase is None:
            Set_WidgetItem(item, column, *widget)
        else:
            wgHBox = wgBase.layout()
            for dd in widget:
                wgHBox.addWidget(dd)
            #
            # wgHBox.addStretch(1)
    return

def Del_WidgetItem(item, column=1, widget=[]):
    wgTree = Get_TreeWidget(item)
    if len(widget) == 0:
        wgTree.removeItemWidget(item, column)
    else:
        wgBase = wgTree.itemWidget(item, column)
        wgHBox = wgBase.layout()
        for dd in widget:
            wgHBox.removeWidget(dd)
    return

def Get_WidgetItem(item, column=1, pos=-1):
    wgTree = Get_TreeWidget(item)
    widget = None
    wgBase = wgTree.itemWidget(item, column)
    if wgBase is None:
        return
    wgHBox = wgBase.layout()
    if pos != -1 and pos < wgHBox.count():
        widget = wgHBox.itemAt(pos).widget()
    return widget

def Get_Widgets_List(item, column=1):
    wgTree = Get_TreeWidget(item)
    wgBase = wgTree.itemWidget(item, column)
    arrWidgetType = []
    if wgBase is None:
        return []
    wgHBox = wgBase.layout()
    for dd in range(0, wgHBox.count()):
        wgChild = wgHBox.itemAt(dd).widget()
        if isinstance(wgChild, QLabel):
            arrWidgetType.append(0)
        elif isinstance(wgChild, QLineEdit):
            arrWidgetType.append(1)
        elif isinstance(wgChild, QComboBox):
            arrWidgetType.append(2)
        elif isinstance(wgChild, QPushButton):
            arrWidgetType.append(3)
        elif isinstance(wgChild, QRadioButton):
            arrWidgetType.append(4)
        else:
            arrWidgetType.append(-1)
    return arrWidgetType

def Set_Widgets_List(arrWidgetType):
    arrWidget = []
    for dd in arrWidgetType:
        if dd == 0:
            arrWidget.append(QLabel())
        elif dd == 1:
            arrWidget.append(QLineEdit())
        elif dd == 2:
            arrWidget.append(QComboBox())
        elif dd == 3:
            arrWidget.append(QPushButton())
        elif dd == 4:
            arrWidget.append(QRadioButton())
        else:
            arrWidget.append(QWidget())
    return arrWidget

def Set_ItemFlag(selectItem, option=35):
    tmpFlag = selectItem.flags() | option
    selectItem.setFlags(selectItem.flags() | tmpFlag)
    return selectItem

def Set_ItemIcon(item, path, column=0):
    icon = Make_Icon(path)
    item.setIcon(column, icon)
    return

def Set_ItemFont(item, column=0, fontName="Ubuntu", size=10, bold=50):   # bold: 0~50~100
    item.setFont(column, QFont(fontName, size, bold))
    return

def Set_ItemColor(item, column=0, rgb=(0, 0, 0)):       # rgb=0~255
    item.setTextColor(column, QColor(rgb[0], rgb[1], rgb[2]))
    return

def Set_ItemBkColor(item, column=0, rgb=(0, 0, 0)):     # rgb=0~255
    item.setBackground(column, QColor(rgb[0], rgb[1], rgb[2]))

def Set_ItemAlignment(item, column=0, alignment=0):     # alignment =0, 1, 2, 4, 8
    if alignment == 1 or alignment == "LEFT":
        alignment = Qt.AlignLeft
    elif alignment == 2 or alignment == "RIGHT":
        alignment = Qt.AlignRight
    elif alignment == 4 or alignment == "CENTER":
        alignment = Qt.AlignHCenter
    else:  # AlignJustify
        alignment = Qt.AlignJustify
    item.setTextAlignment(column, alignment)
    return

# ------------------------------------------------------------------------------
# Header
# ------------------------------------------------------------------------------
def Set_Header_Title(wgTree, *args):
    wgTree.setHeaderLabel(args)
    return

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# <4> Run
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
