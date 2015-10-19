#!/usr/bin/env python
# encoding: utf-8
import requests
from pyasn1.type import univ
from pyasn1.codec.ber import decoder, encoder
from pyasn1_modules import rfc2459

from ocsp import *

# settings
URL = 'https://yourdomain.tld/OCSP'
PROXIES = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080",
}

# variables
SERIAL_NUMBER = 0
ISSUER_NAME_HASH = '01cb3044531fa8618a68d3c60596ab0555866b09'
ISSUER_KEY_HASH = '31c3791bbaf553d717e0897a2d176c0ab32b9d33'
ALGORITHM = rfc2437.id_sha1
ALGO_PARAMS_HEX = '0500'



def build_payload():
    # initializations
    tbsReq = TBSRequest()
    certid = CertID()
    request = Request()
    requestList = univ.SequenceOf(componentType=Request())
    req = OCSPRequest()
    reqExts = rfc2459.Extensions().subtype(
            explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))
    reqExt = rfc2459.Extension()
    signature = Signature()
    certs = univ.SequenceOf(componentType=rfc2459.Certificate()).subtype(
                    explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)
                    )
    cert = rfc2459.Certificate()
    name = rfc2459.GeneralName()


    # assignments
    certid['hashAlgorithm'] = rfc2459.AlgorithmIdentifier()\
            .setComponentByName('algorithm', ALGORITHM)\
            .setComponentByName('parameters', univ.Any(hexValue=ALGO_PARAMS_HEX))

    certid['issuerNameHash'] = univ.OctetString(hexValue=ISSUER_NAME_HASH)
    certid['issuerKeyHash'] = univ.OctetString(hexValue=ISSUER_KEY_HASH)
    certid['serialNumber'] = rfc2459.CertificateSerialNumber(SERIAL_NUMBER)

    request['reqCert'] = certid

    # optional field
    #request['singleRequestExtension'] = reqExt

    reqExt['extnID'] = univ.ObjectIdentifier('1.3.6.1.5.5.7.48.1.2')
    reqExt['critical'] = univ.Boolean('False')
    reqExt['extnValue'] = univ.Any(hexValue='04120410236e5193af7958f49edcc756ed6c6dd3')

    reqExts[0] = reqExt
    requestList[0] = request

    # optional
    # TODO: fill name?
    #tbsReq['requestorName'] = name
    tbsReq['requestList'] = requestList

    # optional 
    tbsReq['requestExtensions'] = reqExts
    tbsReq['version'] = Version(0).subtype(
            explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))

    # optional
    # TODO fill cert?
    signature['signatureAlgorithm'] = rfc2459.AlgorithmIdentifier()\
            .setComponentByName('algorithm', rfc2437.sha1WithRSAEncryption)
    signature['signature'] = univ.BitString("'010101010101'B")
    certs[0] = cert
    signature['certs'] = certs

    req['tbsRequest'] = tbsReq
    # optional signature
    #req['optionalSignature'] = signature

    return req


def send_payload(payload):
    # encode in ASN.1
    data = encoder.encode(payload)

    # send to server
    response = requests.post(URL,
                             headers={'Content-Type': 'application/ocsp-request'},
                             data=data,
                             proxies=PROXIES)

    return response.content


def decode(data, spec):
    # decode response
    ocspResponse = decoder.decode(data, asn1Spec=spec)

    for r in ocspResponse:
        # is asn.1 decodable?
        if hasattr(r, 'prettyPrint'):
            return r


if __name__ == '__main__':
    from pyasn1 import debug

    payload = build_payload()
    response = send_payload(payload)
    response = decode(response, OCSPResponse())
    print("Status:", response['responseStatus'].prettyPrint())
    #debug.setLogger(debug.Debug('all'))
    response = decode(response['responseBytes']['response'], BasicOCSPResponse())
    print(response.prettyPrint())
