# ED QOS Plugins

This is a collection of plug-ins to the [Event Driven QoS](https://github.com/imapex/edqos_app)
application. EDQOS abstracts some of the complexity of the APIC-EM away so that
user applications can focus on interactions with the user, not with the APIC-EM.

## Current plugins
* [awsbutton](awsbutton/README.md) - AWS lambda function code to tie an AWS IoT button to edqos.
* [qosmanagerbot](http://github.com/mbrainar/qosmanagerbot) - A Spark bot that will interface with the ED QOS apps
* [alexa](alexa/README.md) - AWS lambda function code that will allow a user to interface with ED QOS app via an Amazon Echo


## In progress plugins
* [tropo](tropo/README.md) - **NOT WORKING YET** A Tropo script that will allow a user to interface with ED QOS app via text/SMS
* web interface - a web interface that will allow for toggling of relevance levels
