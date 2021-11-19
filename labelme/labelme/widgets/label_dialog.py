import re

from qtpy import QT_VERSION
from qtpy import QtCore
from qtpy import QtGui
from qtpy import QtWidgets

from labelme.logger import logger
import labelme.utils

QT5 = QT_VERSION[0] == "5"


# TODO(unknown):
# - Calculate optimal position so as not to go out of screen area.


class LabelQLineEdit(QtWidgets.QLineEdit):
    def setListWidget(self, list_widget):
        self.list_widget = list_widget

    def keyPressEvent(self, e):
        if e.key() in [QtCore.Qt.Key_Up, QtCore.Qt.Key_Down]:
            self.list_widget.keyPressEvent(e)
        else:
            super(LabelQLineEdit, self).keyPressEvent(e)


class LabelDialog(QtWidgets.QDialog):

    def __init__(
            self,
            text="Enter object label",
            parent=None,
            labels=None,
            sort_labels=True,
            show_text_field=True,
            completion="startswith",
            fit_to_content=None,
            flags=None,
    ):
        if fit_to_content is None:
            fit_to_content = {"row": False, "column": True}
        self._fit_to_content = fit_to_content

        super(LabelDialog, self).__init__(parent)
        self.combobox_first = QtWidgets.QComboBox()
        combobox_first_items = ["road", "space"]
        self.combobox_first.addItems(combobox_first_items)
        self.combobox_first.currentTextChanged.connect(self.changedComboboxFirst)

        self.combobox_second = QtWidgets.QComboBox()
        combobox_second_items = ["flatness", "walkway", "paved_state", "block_state", "block_kind",
                                 "outcurb", "restspace", "sidegap", "sewer", "brailleblock", "continuity", "ramp",
                                 "bicycleroad", "planecrosswalk", "bump", "weed", "floor",
                                 "flowerbed", "parkspace", "enterrail", "fireshutter"]
        self.combobox_second.addItems(combobox_second_items)
        self.combobox_second.currentTextChanged.connect(self.changedComboboxSecond)

        self.combobox_third = QtWidgets.QComboBox()
        combobox_third_items = ["flatness_A", "flatness_B", "flatness_C", "flatness_D", "flatness_E"]
        self.combobox_third.addItems(combobox_third_items)
        self.combobox_third.currentTextChanged.connect(self.changedCombobox)

        self.edit = LabelQLineEdit()
        self.edit.setPlaceholderText(text)
        self.edit.setValidator(labelme.utils.labelValidator())
        self.edit.editingFinished.connect(self.postProcess)
        if flags:
            self.edit.textChanged.connect(self.updateFlags)
        self.edit_group_id = QtWidgets.QLineEdit()
        self.edit_group_id.setPlaceholderText("Group ID")
        self.edit_group_id.setValidator(
            QtGui.QRegExpValidator(QtCore.QRegExp(r"\d*"), None)
        )
        layout = QtWidgets.QVBoxLayout()
        if show_text_field:
            layout_edit = QtWidgets.QHBoxLayout()
            layout_edit.addWidget(self.edit, 6)
            layout_edit.addWidget(self.edit_group_id, 2)
            layout_edit2 = QtWidgets.QHBoxLayout()
            layout_edit2.addWidget(self.combobox_first, 2)
            layout_edit2.addWidget(self.combobox_second, 3)
            layout_edit2.addWidget(self.combobox_third, 3)
            layout.addLayout(layout_edit)
            layout.addLayout(layout_edit2)
        # buttons
        self.buttonBox = bb = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal,
            self,
            )
        bb.button(bb.Ok).setIcon(labelme.utils.newIcon("done"))
        bb.button(bb.Cancel).setIcon(labelme.utils.newIcon("undo"))
        bb.accepted.connect(self.validate)
        bb.rejected.connect(self.reject)
        layout.addWidget(bb)
        # label_list
        self.labelList = QtWidgets.QListWidget()
        if self._fit_to_content["row"]:
            self.labelList.setHorizontalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff
            )
        if self._fit_to_content["column"]:
            self.labelList.setVerticalScrollBarPolicy(
                QtCore.Qt.ScrollBarAlwaysOff
            )
        self._sort_labels = sort_labels
        if labels:
            self.labelList.addItems(labels)
        if self._sort_labels:
            self.labelList.sortItems()
        else:
            self.labelList.setDragDropMode(
                QtWidgets.QAbstractItemView.InternalMove
            )
        self.labelList.currentItemChanged.connect(self.labelSelected)
        self.labelList.itemDoubleClicked.connect(self.labelDoubleClicked)
        self.edit.setListWidget(self.labelList)
        layout.addWidget(self.labelList)
        # label_flags
        if flags is None:
            flags = {}
        self._flags = flags
        self.flagsLayout = QtWidgets.QVBoxLayout()
        self.resetFlags()
        layout.addItem(self.flagsLayout)
        self.edit.textChanged.connect(self.updateFlags)
        self.setLayout(layout)
        # completion
        completer = QtWidgets.QCompleter()
        if not QT5 and completion != "startswith":
            logger.warn(
                "completion other than 'startswith' is only "
                "supported with Qt5. Using 'startswith'"
            )
            completion = "startswith"
        if completion == "startswith":
            completer.setCompletionMode(QtWidgets.QCompleter.InlineCompletion)
            # Default settings.
            # completer.setFilterMode(QtCore.Qt.MatchStartsWith)
        elif completion == "contains":
            completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
            completer.setFilterMode(QtCore.Qt.MatchContains)
        else:
            raise ValueError("Unsupported completion: {}".format(completion))
        completer.setModel(self.labelList.model())
        self.edit.setCompleter(completer)

    def changedComboboxFirst(self, value):
        self.combobox_second.clear()
        combobox_second_items = []

        if value == "road":
            if self.createMode == "polygon":
                combobox_second_items = ["flatness", "walkway", "paved_state", "block_state", "block_kind", "outcurb", "restspace", "sidegap", "sewer", "brailleblock", "continuity", "ramp", "bicycleroad", "planecrosswalk", "bump", "weed", "floor", "flowerbed", "parkspace", "enterrail", "fireshutter"]
            elif self.createMode == "rectangle":
                combobox_second_items = ["sewer", "steepramp", "tierbump", "stone"]

        elif value == "space":
            if self.createMode == "polygon":
                combobox_second_items = ["stair", "stair_broken", "wall", "resting_place_roof", "reception_desk", "lift_button"]
            elif self.createMode == "rectangle":
                combobox_second_items = ["window", "pillar", "lift", "door", "lift_door", "protect_wall", "handle", "lift_button", "direction_sign", "sign_disabled", "braille_sign", "chair", "chair_back", "chair_handle", "number_ticket_machine", "beverage_vending_machine", "beverage_desk", "trash_can", "mailbox"]

        self.combobox_second.addItems(combobox_second_items)

    def changedComboboxSecond(self, value):
        self.combobox_third.clear()
        combobox_third_items = []

        if value == "flatness":
            combobox_third_items = ["flatness_A", "flatness_B", "flatness_C", "flatness_D", "flatness_E"]
        elif value == "walkway":
            combobox_third_items = ["walkway_paved", "walkway_block"]
        elif value == "paved_state":
            combobox_third_items = ["paved_state_broken", "paved_state_normal"]
        elif value == "block_state":
            combobox_third_items = ["block_state_broken", "block_state_normal"]
        elif value == "block_kind":
            combobox_third_items = ["block_kind_bad", "block_kind_good"]
        elif value == "outcurb":
            combobox_third_items = ["outcurb_rectangle", "outcurb_slide", "outcurb_rectangle_broken", "outcurb_slide_broken"]
        elif value == "restspace":
            combobox_third_items = ["restspace"]
        elif value == "sidegap":
            combobox_third_items = ["sidegap_in", "sidegap_out"]
        elif value == "sewer":
            combobox_third_items = ["sewer_cross", "sewer_line"]
        elif value == "brailleblock":
            combobox_third_items = ["brailleblock_dot", "brailleblock_line", "brailleblock_dot_broken",
                                    "brailleblock_line_broken"]
        elif value == "continuity":
            combobox_third_items = ["continuity_tree", "continuity_manhole "]
        elif value == "ramp":
            combobox_third_items = ["ramp_yes", "ramp_no"]
        elif value == "bicycleroad":
            combobox_third_items = ["bicycleroad_broken", "bicycleroad_normal"]
        elif value == "planecrosswalk":
            combobox_third_items = ["planecrosswalk_broken", "planecrosswalk_normal"]
        elif value == "steepramp":
            combobox_third_items = ["steepramp"]
        elif value == "bump":
            combobox_third_items = ["bump_slow", "bump_zigzag"]
        elif value == "weed":
            combobox_third_items = ["weed"]
        elif value == "floor":
            combobox_third_items = ["floor_normal", "floor_broken"]
        elif value == "flowerbed":
            combobox_third_items = ["flowerbed"]
        elif value == "parkspace":
            combobox_third_items = ["parkspace"]
        elif value == "tierbump":
            combobox_third_items = ["tierbump"]
        elif value == "stone":
            combobox_third_items = ["stone"]
        elif value == "enterrail":
            combobox_third_items = ["enterrail"]
        elif value == "fireshutter":
            combobox_third_items = ["fireshutter"]

        elif value == "stair":
            combobox_third_items = ["stair_normal"]
        elif value == "stair_broken":
            combobox_third_items = ["stair_broken"]
        elif value == "wall":
            combobox_third_items = ["wall"]
        elif value == "window":
            combobox_third_items = ["window_sliding", "window_casement"]
        elif value == "pillar":
            combobox_third_items = ["pillar"]
        elif value == "lift":
            combobox_third_items = ["lift"]
        elif value == "door":
            combobox_third_items = ["door_normal", "door_rotation"]
        elif value == "lift_door":
            combobox_third_items = ["lift_door"]
        elif value == "resting_place_roof":
            combobox_third_items = ["resting_place_roof"]
        elif value == "reception_desk":
            combobox_third_items = ["reception_desk"]
        elif value == "protect_wall":
            combobox_third_items = ["protect_wall_protective", "protect_wall_guardrail", "protect_wall_kickplate"]
        elif value == "handle":
            combobox_third_items = ["handle_vertical", "handle_lever", "handle_circular"]
        elif value == "lift_button":
            combobox_third_items = ["lift_button_normal", "lift_button_openarea", "lift_button_layer",
                                    "lift_button_emergency"]
        elif value == "direction_sign":
            combobox_third_items = ["direction_sign_left", "direction_sign_right",
                                    "direction_sign_straight", "direction_sign_exit"]
        elif value == "sign_disabled":
            combobox_third_items = ["sign_disabled_toilet", "sign_disabled_parking",
                                    "sign_disabled_elevator", "sign_disabled_ramp", "sign_disabled_callbell"]
        elif value == "braille_sign":
            combobox_third_items = ["braille_sign"]
        elif value == "chair":
            combobox_third_items = ["chair_multi", "chair_one", "chair_circular"]
        elif value == "chair_back":
            combobox_third_items = ["chair_back"]
        elif value == "chair_handle":
            combobox_third_items = ["chair_handle"]
        elif value == "number_ticket_machine":
            combobox_third_items = ["number_ticket_machine"]
        elif value == "beverage_vending_machine":
            combobox_third_items = ["beverage_vending_machine"]
        elif value == "beverage_desk":
            combobox_third_items = ["beverage_desk"]
        elif value == "trash_can":
            combobox_third_items = ["trash_can"]
        elif value == "mailbox":
            combobox_third_items = ["mailbox"]

        self.combobox_third.addItems(combobox_third_items)

    def changedCombobox(self, value):
        self.edit.setText(value)

    def addLabelHistory(self, label):
        if self.labelList.findItems(label, QtCore.Qt.MatchExactly):
            return
        self.labelList.addItem(label)
        if self._sort_labels:
            self.labelList.sortItems()

    def labelSelected(self, item):
        self.edit.setText(item.text())

    def validate(self):
        text = self.edit.text()
        if hasattr(text, "strip"):
            text = text.strip()
        else:
            text = text.trimmed()
        if text:
            self.accept()

    def labelDoubleClicked(self, item):
        self.validate()

    def postProcess(self):
        text = self.edit.text()
        if hasattr(text, "strip"):
            text = text.strip()
        else:
            text = text.trimmed()
        self.edit.setText(text)

    def updateFlags(self, label_new):
        # keep state of shared flags
        flags_old = self.getFlags()

        flags_new = {}
        for pattern, keys in self._flags.items():
            if re.match(pattern, label_new):
                for key in keys:
                    flags_new[key] = flags_old.get(key, False)
        self.setFlags(flags_new)

    def deleteFlags(self):
        for i in reversed(range(self.flagsLayout.count())):
            item = self.flagsLayout.itemAt(i).widget()
            self.flagsLayout.removeWidget(item)
            item.setParent(None)

    def resetFlags(self, label=""):
        flags = {}
        for pattern, keys in self._flags.items():
            if re.match(pattern, label):
                for key in keys:
                    flags[key] = False
        self.setFlags(flags)

    def setFlags(self, flags):
        self.deleteFlags()
        for key in flags:
            item = QtWidgets.QCheckBox(key, self)
            item.setChecked(flags[key])
            self.flagsLayout.addWidget(item)
            item.show()

    def getFlags(self):
        flags = {}
        for i in range(self.flagsLayout.count()):
            item = self.flagsLayout.itemAt(i).widget()
            flags[item.text()] = item.isChecked()
        return flags

    def getGroupId(self):
        group_id = self.edit_group_id.text()
        if group_id:
            return int(group_id)
        return None

    def popUp(self, text=None, move=True, flags=None, group_id=None, createMode=None):
        self.createMode = createMode
        self.changedComboboxFirst(str(self.combobox_first.currentText()))
        if self._fit_to_content["row"]:
            self.labelList.setMinimumHeight(
                self.labelList.sizeHintForRow(0) * self.labelList.count() + 2
            )
        if self._fit_to_content["column"]:
            self.labelList.setMinimumWidth(
                self.labelList.sizeHintForColumn(0) + 2
            )
        # if text is None, the previous label in self.edit is kept
        if text is None:
            text = self.edit.text()
        if flags:
            self.setFlags(flags)
        else:
            self.resetFlags(text)
        self.edit.setText(text)
        self.edit.setSelection(0, len(text))
        if group_id is None:
            self.edit_group_id.clear()
        else:
            self.edit_group_id.setText(str(group_id))
        items = self.labelList.findItems(text, QtCore.Qt.MatchFixedString)
        if items:
            if len(items) != 1:
                logger.warning("Label list has duplicate '{}'".format(text))
            self.labelList.setCurrentItem(items[0])
            row = self.labelList.row(items[0])
            self.edit.completer().setCurrentRow(row)
        self.edit.setFocus(QtCore.Qt.PopupFocusReason)
        if move:
            self.move(QtGui.QCursor.pos())
        if createMode == "blur":
            return "blur", {}, None
        elif self.exec_():
            return self.edit.text(), self.getFlags(), self.getGroupId()
        else:
            return None, None, None