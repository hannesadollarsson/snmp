#!/usr/bin/python
from pysnmp.entity import engine, config
from pysnmp.carrier.asyncsock.dgram import udp
from pysnmp.entity.rfc3413 import cmdgen

# Create SNMP engine
snmpEngine = engine.SnmpEngine()

# Authentication and privacy settings
config.addV3User(
	snmpEngine, 'nms',
	config.usmHMACSHAAuthProtocol, 'Nobia20!3C5',
	config.usmAesCfb128Protocol, 'Nobia20!3C5'
)

config.addTargetParams(snmpEngine, 'my-creds', 'nms', 'authPriv')

# select tansport
config.addSocketTransport(
	snmpEngine,
	udp.domainName
	udp.UdpSocketTransport().openClientMode()
)

# add host
config.addTargetAddr(
	snmpEngine, 'ciscofw01',
	udp.domainName, ('10.10.0.240', 161),
	my-creds
)	

def cbFun(sendRequestHandle, errorIndication, errorStatus, errorIndex, varBindTable, cbCtx):
	if errorIndication:
		print(errorIndication)
	elif errorStatus:
		print('%s at %s', % (
			errorStatus.prettypPrint(),
			errorIndex and varBindTable[-1] [int (errorIndex)-1] or '?'
		)
	else:
		for oid, val in varBindTable:
			print ('%s = %s' % (oid.prettyPrint(), val.prettyPrint()))

cmdgen.GetCommandGenerator().sendReq(
	snmpEngine,
	'ciscofw01',
	( ((1,3,6,1,4,1,9,9,147,1,2,1,1,1,3,7), None), ),
	cbFun
)
snmpEngine.transportDispatcher.runDispatcher()