#!/usr/bin/python
import logging
import sys

import smpplib.gsm
import smpplib.client
import smpplib.consts

############################################################################
# EXAMPLE SCRIPT FOR TROOPERS 2017 SMPP LISTENER                           #
#		www.troopers.de                                            #
# FOR QUESTIONS, PLS Contact Hendrik Schmidt, hschmidt@ernw.de             #
############################################################################


_MYSERVICE=20001 #functional number of your service

#Enable Logging
logging.basicConfig(filename="YourESME.log",level='DEBUG')

#YOUR CODE
def handle_incoming_sms(pdu):
    logging.info(pdu.source_addr + " -> " + pdu.destination_addr + " send msg " + pdu.short_message)
    #YOUR CODE
    #...
    #...
    # Send SMS Back
    send_message(_MYSERVICE,pdu.source_addr,"Successfully received SMS with content " + pdu.short_message)



#######################
def send_message(src,dest, string):
    parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts(string)

    logging.info('Sending SMS "%s" to %s' % (string, dest))
    for part in parts:
        pdu = client.send_message(
            source_addr_ton=smpplib.consts.SMPP_TON_INTL,
            source_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
            source_addr=src,
            dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
            dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
            destination_addr=dest,
            short_message=part,
            data_coding=encoding_flag,
            #esm_class=msg_type_flag,
            esm_class=smpplib.consts.SMPP_MSGMODE_FORWARD,
            registered_delivery=False,
    )


client = smpplib.client.Client('127.0.0.1', 2775)

# Print Output and Start Handler
client.set_message_sent_handler(
    lambda pdu: logging.info('sent {} {}\n'.format(pdu.sequence, pdu.message_id)))
client.set_message_received_handler(handle_incoming_sms)

client.connect()

client.bind_transceiver(system_id='YourESME', password='123456')
print "MYSERVICE: Successfully bound SMPP"

client.listen()
