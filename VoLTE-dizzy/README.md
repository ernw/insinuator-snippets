The .dizz files create malformed SIP messages to fuzz an IMS, which manages Multimedia services of LTE networks such as voice calls and text messages.

The generated SIP messages simulate those exchanged with OpenIMS, which is an open source simulation of an IMS environment.
The files faultyIP.txt, integer.txt and method.txt are contain payloads to attack parameters that usually take IP addresses, integers and SIP methods respectively. They might not be as effective as dizzy standard payloads but they save time.

Any suggestions to modify dizz files or the payload files are welcome :)

For more information about the attacks, please visit the blogpost https://www.insinuator.net/2016/02/denial-of-service-attacks-on-volte/
