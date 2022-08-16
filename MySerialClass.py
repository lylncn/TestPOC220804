import threading
import time
import serial
import numpy as np


class MySerialClass(object):

    def __init__(self, Com, BaudRate, Parity, DataBits, StopBits):
        self.cnt = 0
        self.ReadThread = None
        self.WriteThread = None
        self.ser = None
        self.sam = None

        self.Com = Com
        self.BaudRate = BaudRate
        self.Parity = Parity
        self.DataBits = DataBits
        self.StopBits = StopBits
        self.sendString = 'test RS485'
        self.recArray = None
        self.numSend = 0
        self.uartState = False
        self.newData = b''
        self.lastData = b''
        self.frameData = None
        self.frameDataUpdate = 0
        self.FRAME_LEN = 18
        self.serialWriteThreadExit = False
        self.serialReadThreadExit = False
        self.serialThreadBegin()
        # self.serialOpen()

    def serialOpen(self):
        # 配置串口，尝试打开串口
        try:
            self.ser = serial.Serial(port=self.Com, baudrate=self.BaudRate, bytesize=self.DataBits, parity=self.Parity,
                                     stopbits=self.StopBits, timeout=None)
            return self.ser
        except Exception as e:
            print(e)
            self.ser = None
            return None
            '''
                    if not self.ser == None:
                        try:
                            self.ser.open()
                            # self.uartState = True
                        except Exception as e:
                            self.ser.close()
                            print('2', e)
            '''
        # self.ser.uartState = True

    def serialWrite(self):

        sendbuf = bytes([0xaa, 0xaa, 2, 3, 4, 5, 6, 0x4d, 0x56, 9, 100, 34, 13, 14])
        while self.ser.isOpen():
            try:
                # self.ser.write(self.sendString.encode('utf-8'))
                self.ser.write(sendbuf)
                time.sleep(0.01)
                # print('write is:', sendbuf)
                self.numSend += 1

            except Exception as e:
                print(e)
                if self.ser.isOpen() != True:
                    print("can't open the port", self.Com)
            if self.serialWriteThreadExit:
                break
            time.sleep(0.001)
        self.numSend += 1

    def serialRead(self):

        # 有可能与串口测试部分冲突，需要将此设置为最高级别
        while True:
            # time.sleep()
            count = self.ser.inWaiting()
            if count > 0:
                try:
                    self.newData = self.ser.read(count)
                    self.lastData = self.lastData + self.newData

                except Exception as e:
                    print(e)
                    self.uartState = False
            while len(self.lastData) >= self.FRAME_LEN:
                if self.lastData[0] == 0xaa and self.lastData[1] == 0xaa:
                    self.frameData = self.lastData[0:self.FRAME_LEN]
                    self.frameDataUpdate = 1
                    self.lastData = self.lastData[self.FRAME_LEN:len(self.lastData)]

                    #sam = np.frombuffer(self.frameData, dtype=np.uint16)
                    #print("rec:", sam, end='\n')
                else:
                    self.lastData = self.lastData[1:len(self.lastData)]
            if self.serialReadThreadExit:
                break

    def serialThreadBegin(self):
        # 启动写线程  启动读线程
        if self.serialOpen() is not None:
            self.WriteThread = threading.Thread(target=self.serialWrite)
            self.WriteThread.start()
            self.ReadThread = threading.Thread(target=self.serialRead)
            self.ReadThread.start()
            # self.WriteThread.join()
            # self.ReadThread.join()
            # self.cnt = self.cnt + 1
            # print(self.cnt)
            # join 很重要，因为需要在写之后将串口关闭，再将串口配置成另外一个类型，需要在这个期间只有读写不再开启新的线程，在这两个线程结束之后关闭串口和配置与开启新的串口
            # self.numSend = 0

    def __del__(self):
        self.serialWriteThreadExit = True
        self.serialReadThreadExit = True
        if self.ser.isOpen():
            self.ser.close()
