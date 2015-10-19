#!/usr/bin/env python
# encoding: utf-8
# author: Timo Schmid <tschmid@ernw.de>

from pyasn1.type import univ, namedtype, tag, namedval, base, useful
from pyasn1_modules import rfc2459, rfc2437, rfc2560

# request
class Version(univ.Integer):
    namedValues = namedval.NamedValues(
            ('v1', 0)
            )


class CertID(univ.Sequence):
    componentType = namedtype.NamedTypes(
            namedtype.NamedType('hashAlgorithm', rfc2459.AlgorithmIdentifier()),
            namedtype.NamedType('issuerNameHash', univ.OctetString()),
            namedtype.NamedType('issuerKeyHash', univ.OctetString()),
            namedtype.NamedType('serialNumber', rfc2459.CertificateSerialNumber())
            )


class Request(univ.Sequence):
    componentType = namedtype.NamedTypes(
            namedtype.NamedType('reqCert', CertID()),
            namedtype.OptionalNamedType('singleRequestExtensions', rfc2459.Extensions().subtype(
                explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)
                ))
            )


class TBSRequest(univ.Sequence):
    componentType = namedtype.NamedTypes(
            namedtype.DefaultedNamedType('version', Version(0).subtype(
                explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
            namedtype.OptionalNamedType('requestorName', rfc2459.GeneralName().subtype(
                explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)
                )),
            namedtype.NamedType('requestList', univ.SequenceOf(componentType=Request())),
            namedtype.OptionalNamedType('requestExtensions', rfc2459.Extensions().subtype(
                explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2)
                ))
            )


class Certs(univ.SequenceOf):
    componentType=rfc2459.Certificate()


class Signature(univ.Sequence):
    componentType = namedtype.NamedTypes(
            namedtype.NamedType('signatureAlgorithm', rfc2459.AlgorithmIdentifier()),
            namedtype.NamedType('signature', univ.BitString()),
            namedtype.NamedType('certs', Certs().subtype(
                explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)
                )
)
            )


class OCSPRequest(univ.Sequence):
    componentType = namedtype.NamedTypes(
            namedtype.NamedType('tbsRequest', TBSRequest()),
            namedtype.OptionalNamedType('optionalSignature', Signature().subtype(
                explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)))
            )



# response
class OCSPResponseStatus(univ.Enumerated):
    namedValues = namedval.NamedValues(
        ('successful', 0),
        ('malformedRequest', 1),
        ('internalError', 2),
        ('tryLater', 3),
        #('not-used', 4),
        ('sigRequired', 5),
        ('unauthorized', 6)
    )


class ResponseBytes(univ.Sequence):
    componentType = namedtype.NamedTypes(
            namedtype.NamedType('responseType', univ.ObjectIdentifier()),
            namedtype.NamedType('response', univ.OctetString())
            )


class OCSPResponse(univ.Sequence):
    componentType = namedtype.NamedTypes(
            namedtype.NamedType('responseStatus', OCSPResponseStatus()),
            namedtype.OptionalNamedType('responseBytes', ResponseBytes().subtype(
                explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)
                ))
            )


KeyHash = univ.OctetString
UnknownInfo = univ.Null


class RevokedInfo(univ.Sequence):
    componentType = namedtype.NamedTypes(
            namedtype.NamedType('revocationTime', useful.GeneralizedTime()),
            namedtype.OptionalNamedType('revocationReason', rfc2459.CRLReason().subtype(
                explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)
                ))
            )


class CertStatus(univ.Choice):
    componentType = namedtype.NamedTypes(
            namedtype.NamedType('good', univ.Null().subtype(
                implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)
                )),
            namedtype.NamedType('revoked', RevokedInfo().subtype(
                implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)
                )),
            namedtype.NamedType('unknown', UnknownInfo().subtype(
                implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2)
                ))
            )


class SingleResponse(univ.Sequence):
    componentType = namedtype.NamedTypes(
            namedtype.NamedType('certID', CertID()),
            namedtype.NamedType('certStatus', CertStatus()),
            namedtype.NamedType('thisUpdate', useful.GeneralizedTime()),
            namedtype.OptionalNamedType('nextUpdate', useful.GeneralizedTime().subtype(
                explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)
                )),
            namedtype.OptionalNamedType('singleExtensions', rfc2459.Extensions().subtype(
                explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2)
                ))
            )


class ResponderID(univ.Choice):
    componentType = namedtype.NamedTypes(
            namedtype.NamedType('byName', rfc2459.Name().subtype(
                explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))),
            namedtype.NamedType('byKey', KeyHash().subtype(
                explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))),
            )


class ResponseData(univ.Sequence):
    componentType = namedtype.NamedTypes(
            namedtype.DefaultedNamedType('version', Version(0).subtype(
                explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
            namedtype.NamedType('responderID', ResponderID()),
            namedtype.NamedType('producedAt', useful.GeneralizedTime()),
            namedtype.NamedType('responses', univ.SequenceOf(componentType=SingleResponse())),
            namedtype.OptionalNamedType('responseExtensions', rfc2459.Extensions().subtype(
                explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)
                ))
            )


class BasicOCSPResponse(univ.Sequence):
    componentType = namedtype.NamedTypes(
            namedtype.NamedType('tbsResponseData', ResponseData()),
            namedtype.NamedType('signatureAlgorithm', rfc2459.AlgorithmIdentifier()),
            namedtype.NamedType('signature', univ.BitString()),
            namedtype.OptionalNamedType('certs', Certs().subtype(
                explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)
                ))
            )



if __name__ == '__main__':
    import sys
    from pyasn1 import debug
    from pyasn1.codec.ber import decoder, encoder

    #debug.setLogger(debug.Debug('all'))

    if len(sys.argv) <= 1:
        req = OCSPRequest()
        req['tbsRequest'] = TBSRequest()
        req['tbsRequest']['version'] = Version(0).subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))
        request = Request()
        certid = CertID()
        request['reqCert'] = certid
        certid['hashAlgorithm'] = rfc2459.AlgorithmIdentifier()\
                .setComponentByName('algorithm', rfc2437.id_sha1)\
                .setComponentByName('parameters', univ.Any(hexValue='0500'))
        certid['issuerNameHash'] = univ.OctetString(hexValue='01cb3044531fa8618a68d3c60596ab0555866b09')
        certid['issuerKeyHash'] = univ.OctetString(hexValue='31c3791bbaf553d717e0897a2d176c0ab32b9d33')
        certid['serialNumber'] = rfc2459.CertificateSerialNumber(0)
        req['tbsRequest']['requestList'] = univ.SequenceOf(componentType=Request()).setComponentByPosition(0, request)
        reqExts = rfc2459.Extensions().subtype(
                explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))
        reqExt = rfc2459.Extension()
        reqExt['extnID'] = univ.ObjectIdentifier('1.3.6.1.5.5.7.48.1.2')
        reqExt['critical'] = univ.Boolean('False')
        reqExt['extnValue'] = univ.Any(hexValue='04120410236e5193af7958f49edcc756ed6c6dd3')
        reqExts[0] = reqExt
        req['tbsRequest']['requestExtensions'] = reqExts
        print(req.prettyPrint())

        print(encoder.encode(req))
    else:
        with open(sys.argv[1], 'rb') as fp:
            for t in decoder.decode(fp.read(), asn1Spec=OCSPRequest()):
                if hasattr(t, 'prettyPrint'):
                    print(t.prettyPrint())
                else:
                    print(t)
