POX_distribute_version
======================
This is a distribute controller based on POX.
I add some codes to achive communication between POXs.

###Protcol

This protocol is a original protocal made by licheng.
Many packes of it is just a class.
Version1.0 is pretty simple. I will continue to make it better.

###lib_ewbridge
\#TODO:Defined the packets of OpenEWbridge Protocal.

###OpenFlow_EWbridge

\#TODO:Protocal packets handler for manipulating packets.

###communication

Distributed_server and distributed_client function.

\#TODO:start server controller or client controller.

###Install
First of all,you need to install scapy.
Because I use the scapy to encapulate the packets.

and then:

Replace the boot.py by this file or add some codes like what I have done.

You need to copy the communication.py ,lib_ewbridge.py and OpenFlow_EWbridge.py into pox/messenger category.

###Getting started

Start a POX as server controller,and set IP/PORT information of server's information in client controller.
Just make sure that make a socket connection between them.

Start the Cient controller(POX).
