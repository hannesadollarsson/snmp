#!/usr/bin/python
from pysnmp.entity import engine, config
from pysnmp.carrier.asynsock.dgram import udp
from pysnmp.entity.rfc3413 import cmdgen

# Create SNMP engine
snmpEngine = engine.SnmpEngine()

# Authentication and privacy settings
config.addV3User(
	snmpEngine, 'nms',
	config.usmHMACSHAAuthProtocol, 'SECRET',
	config.usmAesCfb128Protocol, 'SECRET'
)

config.addTargetParams(snmpEngine, 'my-creds', 'nms', 'authPriv')

# select tansport
config.addSocketTransport(
	snmpEngine,
	udp.domainName,
	udp.UdpSocketTransport().openClientMode()
)

# add host
config.addTargetAddr(
	snmpEngine, 'ROUTER',
	udp.domainName, ('1.1.1.1', 161),
	'my-creds'
)	

def cbFun(sendRequestHandle, errorIndication, errorStatus, errorIndex, varBindTable, cbCtx):
	if errorIndication:
		print(errorIndication)
	elif errorStatus:
		print('%s at %s' % (
			errorStatus.prettypPrint(),
			errorIndex and varBindTable[-1] [int (errorIndex)-1] or '?'
			)
		)
	else:
		for oid, val in varBindTable:
			print ('%s = %s' % (oid.prettyPrint(), val.prettyPrint()))

cmdgen.GetCommandGenerator().sendReq(
	snmpEngine,
	'ROUTER',
	( ((1,3,6,1,4,1,9,9,147,1,2,1,1,1,3,7), None), ),
	cbFun
)
snmpEngine.transportDispatcher.runDispatcher()