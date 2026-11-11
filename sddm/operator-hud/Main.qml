import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

// Operator HUD SDDM / Qt6. Authentication is delegated to SDDM's PAM backend.
// Deliberately no user enumeration, no auto-login and no password logging.
Rectangle {
    id: root
    width: 1280
    height: 720
    color: config.background

    property bool busy: false
    property string errorText: ""
    property int sessionIndex: sessionChoice.currentIndex

    function submitLogin() {
        if (busy || username.text.trim().length === 0 || password.text.length === 0)
            return
        busy = true
        errorText = ""
        sddm.login(username.text.trim(), password.text, sessionIndex)
    }

    Connections {
        target: sddm
        function onLoginFailed() {
            busy = false
            password.text = ""
            errorText = "Autenticación incorrecta"
            password.forceActiveFocus()
        }
        function onLoginSucceeded() {
            password.text = ""
        }
        function onInformationMessage(message) {
            // No passwords or secrets are printed or persisted.
            errorText = message
        }
    }

    Rectangle {
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        width: Math.max(6, parent.width * 0.004)
        color: config.accent
    }

    Column {
        anchors.left: parent.left
        anchors.leftMargin: Math.max(45, parent.width * 0.10)
        anchors.verticalCenter: parent.verticalCenter
        spacing: 18
        visible: root.width > 1000

        Text {
            text: "OPERATOR HUD"
            color: config.accent
            font.family: "monospace"
            font.pixelSize: 22
            font.bold: true
            font.letterSpacing: 4
        }
        Text {
            text: "SECURE\nACCESS"
            color: config.foreground
            font.family: "sans-serif"
            font.pixelSize: 72
            font.bold: true
            lineHeight: 0.96
        }
        Text {
            text: "ARCH LINUX  /  QTILE  /  X11"
            color: config.muted
            font.family: "monospace"
            font.pixelSize: 18
        }
    }

    Rectangle {
        id: loginPanel
        anchors.right: parent.right
        anchors.rightMargin: Math.max(20, parent.width * 0.09)
        anchors.verticalCenter: parent.verticalCenter
        width: Math.min(420, parent.width - 40)
        height: 475
        radius: 16
        color: config.panel
        border.color: config.border
        border.width: 1

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 32
            spacing: 13

            Text {
                text: "INICIAR SESIÓN"
                color: config.foreground
                font.family: "sans-serif"
                font.bold: true
                font.pixelSize: 24
            }
            Text {
                text: "Introduce tus credenciales"
                color: config.muted
                font.pixelSize: 14
            }
            Item { Layout.preferredHeight: 4 }

            TextField {
                id: username
                Layout.fillWidth: true
                Layout.preferredHeight: 48
                placeholderText: "Usuario"
                font.pixelSize: 15
                selectByMouse: true
                KeyNavigation.tab: password
                onAccepted: password.forceActiveFocus()
                enabled: !root.busy
                Component.onCompleted: forceActiveFocus()
            }

            TextField {
                id: password
                Layout.fillWidth: true
                Layout.preferredHeight: 48
                placeholderText: "Contraseña"
                echoMode: TextInput.Password
                font.pixelSize: 15
                selectByMouse: false
                KeyNavigation.tab: sessionChoice
                onAccepted: root.submitLogin()
                enabled: !root.busy
            }

            ComboBox {
                id: sessionChoice
                Layout.fillWidth: true
                Layout.preferredHeight: 44
                model: sessionModel
                textRole: "name"
                currentIndex: sessionModel.lastIndex >= 0 ? sessionModel.lastIndex : 0
                enabled: !root.busy
            }

            Text {
                Layout.fillWidth: true
                text: root.errorText
                color: config.error
                wrapMode: Text.WordWrap
                font.pixelSize: 13
                visible: root.errorText.length > 0
            }

            Button {
                id: signIn
                Layout.fillWidth: true
                Layout.preferredHeight: 48
                text: root.busy ? "AUTENTICANDO…" : "ACCEDER"
                enabled: !root.busy && username.text.trim().length > 0 && password.text.length > 0
                onClicked: root.submitLogin()
            }
            Item { Layout.fillHeight: true }

            RowLayout {
                Layout.fillWidth: true
                Button {
                    text: "REINICIAR"
                    visible: sddm.canReboot
                    enabled: !root.busy
                    onClicked: sddm.reboot()
                }
                Item { Layout.fillWidth: true }
                Button {
                    text: "APAGAR"
                    visible: sddm.canPowerOff
                    enabled: !root.busy
                    onClicked: sddm.powerOff()
                }
            }
        }
    }

    Text {
        anchors.left: parent.left
        anchors.bottom: parent.bottom
        anchors.margins: 26
        color: config.muted
        font.family: "monospace"
        font.pixelSize: 12
        text: "AUTH: SDDM / PAM   ·   GESTIÓN DE SESIÓN: LOGIND"
    }
}
