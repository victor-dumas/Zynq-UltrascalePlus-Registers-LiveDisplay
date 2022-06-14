###############################################################################
# Project      :
# Reference    :
# Design       :
# Title        : COM_SOC
###############################################################################
# File         : COM_SOC.py
# Author       : NSA
# Company      :
# Created      : 27/03/2021
# Last update  :
# Platform     :
###############################################################################
# Description  :   Module Comm allows to communicate with SOC using devmem_server protocol
###############################################################################
from component import Component
import logging
import socket

class Comm(Component):

    def __init__(   self,
                    log_name='comm',
                    hostname='192.168.51.202',
                    # Server port to access registers with mmap and address (0xa0010000)
                    port_tcp_register = 4001,                     
                    timeout = 10,
                ):

        super().__init__(log_name, log_level = logging.INFO)
        # Connection to the tcp server
        try:
            self.sock_reg = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.log.info('Debut Connexion vers {}:{}'.format(hostname, port_tcp_register))
            self.sock_reg.connect((hostname, port_tcp_register))
            self.log.info('Connection etabli vers {}:{}'.format(hostname, port_tcp_register))
        except ConnectionRefusedError as exception_retournee:
            self.log.error("Error :{}".format(exception_retournee))
            exit()

    # Write data to addr at offset
    def regwr(self, base_addr, offset_reg, data):
        addr = base_addr + offset_reg

        cmd = "W{:09X}{:08X}\n".format(addr, data)
        self.log.debug("regwr> cmd={}".format(cmd))
        self.sock_reg.send(cmd.encode('utf-8'))

        #La reponse est du type WAAAAAAAAA
        answer= self.sock_reg.recv(1024).decode()
        self.log.debug( "regwr> reception de {}".format(answer))

        addr_receive = int(answer[1:1+9], 16)
        self.log.debug("regwr> addr_receive={}".format(addr_receive))
        if (addr_receive != addr):
            self.log.critical("regwr> addr_receive={}".format(addr_receive))
        else:
            self.log.debug("regwr> ok")


    def regmd(self, base_addr, offset_reg, val, mask):
        rdval = self.regrd(base_addr, offset_reg)
        self.regwr(base_addr, offset_reg , (rdval & (~mask)) | (val & mask))

    def regrd(self, base_addr, offset_reg):
        addr = base_addr + offset_reg

        cmd = "R{:09X}\n".format(addr)
        self.log.debug("regrd> cmd={}".format(cmd))
        self.sock_reg.send(cmd.encode('utf-8'))

        answer= self.sock_reg.recv(1024).decode()
        self.log.debug( "regrd> reception de {}".format(answer))

        # Answer format: RAAAAAAAAADDDDDDDD
        addr_receive = int(answer[1:1+9], 16)
        data_receive = int(answer[10:10+8], 16)
        self.log.debug("regrd> addr_receive={} data_receive={}".format(addr_receive, data_receive))
        if (addr_receive != addr):
            self.log.critical("regrd> addr_receive={} addr={}".format(addr_receive, addr))
        else:
            self.log.debug("regrd> [{:#011x}]={:#010x}".format(addr, data_receive))
            return data_receive

    def close(self):
        self.log.info('close')
        self.sock_reg.close()
        #socket.close(self.sock_reg.fileno())

###############################################################################
# Class test
###############################################################################
if __name__ == '__main__':
    com_soc = Comm()

    for addr in (0x1000, 0x1004):
        reg = com_soc.regrd(base_addr = 0x90000000, offset_reg = addr )
        print("@{:#06x}={:#010x}".format(addr, reg))

    com_soc.regwr(base_addr= 0x90000000, offset_reg= 0x1000, data = 0x12345678 )
