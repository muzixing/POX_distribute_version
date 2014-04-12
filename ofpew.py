import errno
import socket
import lib_ewbridge as ofpew

import Queue
import time
"""
Author: muzi
Date: 2014/4/12
TODO: handle the OpenFlow EWbridge messages

"""
#TODO:store the info.
network = {}
nodes = {}
ports = {}
links = {}
flow_paths = {}


def update_handler(data):
    #manipulate the messenge
    update_msg = ofpew.ofpew_update(data[0:4])
    data = data[4:]                  
    for x in xrange(update_msg.network_number):
        offset = 0
        network_view = ofpew.ofpew_network_view(data[0:16])
        network[x] = network_veiw               #store the network_view

        #offset = 16+network_view.node_number*28+network_veiw.link_number*48 +network_view.port_number*36 +network_view.flow_path_number*60
        offset = 16
        data = data[offset:]

        #we need to make sure the offset of network object.

        for i in xrange(network_view.node_number):
            #store the nodes of this network
            node_t =  ofpew.ofpew_node(data[(i-1)*28:i*28]) 
            #node_t.show()
            nodes[node_t.datapath_id] = node_t

        offset = 28*network_view.node_number
        data = data[offset:]

        for k in xrange(network_view.port_number):
            #store the ports of this network
            port_t =  ofpew.ofpew_port(data[(k-1)*36:k*36]) 
            #port_t.show()
            ports[port_t.id] = port_t

        offset = 36*network_view.port_number
        data = data[offset:]
        for j in xrange(network_view.link_number):
            #store the links of this network
            link_t =  ofpew.ofpew_link(data[(j-1)*48:k*48]) 
            #link_t.show()
            links[link_t.id] = link_t

        offset = 48*network_view.link_number
        data = data[offset:]
        for y in xrange(network_view.flow_path_number):
            #store the flwo_paths of this network
            flow_path_t =  ofpew.ofpew_flow_path(data[(y-1)*60:k*60]) 
            #flow_path_t.show()
            flow_paths[flow_path_t.id] = flow_path_t

        offset = 60* network_view.flow_path_number
        data = data[offset:]

    return None

def notification_handler(data):
    print "***OFPEW_NOTIFICATION:"+data
    return None

def down_handler(data):
    print "***OFPEW_DOWN.***"
    return None

def refresh_handler(data):
    #send the topo which is changed.
    update_msg = ofpew.ofpew_update(network_number = 1)
    network_msg = ofpew.ofpew_network_view(node_number = 2, port_number = 4,link_number = 1, flow_path_number = 1)
    node_msg_1 = ofpew.ofpew_node(datapath_id = 1)
    node_msg_2 = ofpew.ofpew_node(datapath_id = 2)

    port_msg_1 = ofpew.ofpew_port(port_id = 1,node_id = 1)
    port_msg_2 = ofpew.ofpew_port(port_id = 2,node_id = 2)
    port_msg_3 = ofpew.ofpew_port(port_id = 3,node_id = 1)
    port_msg_4 = ofpew.ofpew_port(port_id = 4,node_id = 2)

    link_msg = ofpew.ofpew_link(link_id = 1,src_node_id = 1, src_port_id = 1,dst_node_id = 2, dst_port_id = 2)

    flow_path_msg = ofpew.ofpew_flow_path(flow_path_id = 1, src_in_port_id =3,src_node_id =1, src_out_port_id = 1,
                                            dst_node_id = 2,dst_in_port_id = 2 ,dst_out_port_id = 4)

    #we encapsulate the packet.
    msg = update_msg/network_msg/node_msg_1/node_msg_2/port_msg_1/port_msg_2/port_msg_3/port_msg_4/link_msg/flow_path_msg

    return msg


def echo_handler():#send echo request.
    msg = ofpew.ofpew_header(type = 2,length = 8)#send the ofpew_echo_request period.
    return msg
def echo_request_handler(data):
    msg = ofpew.ofpew_header(type = 3,length = 8)
    return msg

def vendor_handler(data):
    print "***OFPEW_VENDOR:"+data 
    return None

def error_handler(data):
    print "***OFPEW_ERROR:"+data
    return None

##################### manipulate the msg  ################################
def msg_handler(data):
    rmsg = ofpew.ofpew_header(data[0:8])
    body = data[8:]
    if rmsg.type == 0:
        print "OFEWPT_HELLO"
        return update_handler(data)
        
    elif rmsg.type == 1:
        print "OFPEW_ERROR"
        return error_handler(data)
    elif rmsg.type == 2:
        print "OFPEW_ECHO_REQUEST"
        return echo_request_handler(data)
    
    elif rmsg.type == 3:
        print "OFPEW_ECHO_REPLY"
        #send echo request periodic.
        return None
    elif rmsg.type == 4:
        return vendor_handler(data)

    elif rmsg.type == 5:
        #read and store messenge.
        return update_handler(data)

    elif rmsg.type == 6:
        return notification_handler(data)

    elif rmsg.type == 7:
        return refresh_handler(data)

    elif rmsg.type == 8:
        return down_handler(data)    

def send_echo_request():   
    if (int(time.time) % 5 )== 0:
        return echo_handler()
