from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from Speechrecognizer import stt
from kivy.clock import Clock
import socket

connected = False

class assistant(BoxLayout):
    def socket_send(self,text):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(("10.20.30.102",8000))
        def send(msg):
            m = msg.encode('utf-8') 
            msg_l = len(m)
            send_l = str(msg_l).encode('utf-8')
            send_l += b' '*(64 - len(send_l))
            s.send(send_l)
            s.send(m)
           #s.close()
        send(text)


    def start_listening(self):
        global connected
        if connected == False:
            try:
                self.socket_send('[Movil] Connected')
                self.ids.label01.text = 'Conectado'
                connected = True
                self.ids.button01.icon = 'microphone-off'
            except:
                self.ids.label01.text = 'No se ha podido conectar :('
        elif connected == True:
            if stt.listening:
                self.stop_listening()
                return
            self.ids.button01.icon = 'microphone'

            stt.start()
            Clock.schedule_interval(self.check_state, 1 / 5)
            self.ids.label01.text = 'Escuchando...'
            

    def stop_listening(self):
        self.ids.button01.icon = 'microphone-off'
        stt.stop()
        self.update()
        Clock.unschedule(self.check_state)

    def update(self):
        self.ids.label01.text = str('\n'.join(stt.results))
        self.socket_send(str('\n'.join(stt.results)))
        pass

    def check_state(self, dt):
        #if the recognizer service stops, change UI
        if not stt.listening:
            self.stop_listening()
        pass
       

class MainApp(MDApp):
    def build(self):
        return assistant()
    def on_pause(self):
        return True
    

    

if __name__ == "__main__":
    MainApp().run()
    
