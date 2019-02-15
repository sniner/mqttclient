import argparse
import logging
import re
import sys

import paho.mqtt.client as mqtt


log = logging.getLogger()


def on_connect(client, userdata, flags, rc):
    if rc != 0:
        log.error("Connection refused, code "+str(rc))
        exit(1)

    log.info("Connected with result code "+str(rc))

    if callable(userdata):
        userdata(client)



def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
    except:
        payload = msg.payload
    print(msg.topic + ":" + str(payload))



def on_disconnect(client, userdata, rc):
    if rc != 0:
        log.warn("Connection lost, trying to reconnect!")
        client.reconnect()



def listener(*topics, host="localhost", port=1883):
    def action(client):
        if topics:
            for topic in topics:
                log.info("Subscribing to topic '"+topic+"'")
                client.subscribe(topic)
        else:
            log.info("Subscribing to all topics")
            client.subscribe('#')

    client = mqtt.Client(userdata=action)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    client.connect(host, port)

    try:
        client.loop_forever()
    except:
        pass
    finally:
        client.disconnect()



def publisher(*pairs, retain=False, qos=0, host="localhost", port=1883, trim=False):
    def action(client):
        for pair in pairs:
            try:
                topic, value = pair.split(':', 1)
                if trim:
                    topic = topic.strip()
                    value = value.strip()
            except Exception as err:
                log.info("Ignoring '"+pair+"': "+str(err))
            else:
                log.info("Publishing: "+str(topic)+":"+str(value))
                client.publish(topic, value, retain=retain, qos=qos)
        client.disconnect()

    client = mqtt.Client(userdata=action)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    client.connect(host, port)

    try:
        client.loop_forever()
    except Exception as err:
        log.error("Publishing interrupted: "+str(err))


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=None)
    parser.add_argument('--host', type=str, default='localhost',
            help='Address of MQTT host')
    parser.add_argument('--port', type=int, default=1883,
            help='MQTT port')
    parser.add_argument('--verbose', action="store_true",
            help='Show all messages')

    subparsers = parser.add_subparsers()

    sub = subparsers.add_parser('subscribe', aliases=['sub', 'listen'],
            description='Subscribe to topics and show messages comming in')
    sub.set_defaults(func=listener)
    sub.add_argument('topics', type=str, nargs='*',
            help='Topics to subscribe to')
    sub.add_argument('--all', action="store_true",
            help='Subscribe to all topics')

    pub = subparsers.add_parser('publish', aliases=['pub'],
            description='Publish values to topics')
    pub.set_defaults(func=publisher)
    pub.add_argument('data', type=str, nargs='*',
            help='Topics/values to publish: "topic:value"')
    pub.add_argument('--retain', action="store_true",
            help='Retain')
    pub.add_argument('--qos', type=int, default=0, choices=(0, 1, 2),
            help='Quality of service')
    pub.add_argument('--trim', action="store_true",
            help='Trim whitespace on topics and values')

    return parser


def main():
    parser = arg_parser()
    args = parser.parse_args()

    log = logging.basicConfig(
            format="%(asctime)-15s %(levelname)-8s %(message)s",
            level=logging.DEBUG if args.verbose else logging.WARNING
    )

    if args.func==listener:
        if args.all:
            args.topics = ['#']
        elif not args.topics:
            lines = [line.strip() for line in sys.stdin.readlines()]
            args.topics = [line for line in lines if line]
        listener(*args.topics, host=args.host, port=args.port)
    elif args.func==publisher:
        if not args.data:
            lines = [line.strip() for line in sys.stdin.readlines()]
            args.data = [line for line in lines if re.match('[^:]+:', line)]
        publisher(*args.data, retain=args.retain, qos=args.qos, trim=args.trim,
                host=args.host, port=args.port)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
