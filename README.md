# mqttclient

Simple MQTT client.


## Usage examples

Publishing:

```
mqtt-client --host HOST pub "test/topic:value"
echo "test/topic:value" | mqtt-client --host HOST pub
echo -e "test/topic1:value1\ntest/topic2:value2" | mqtt-client --host HOST pub
```

Subscribing/monitoring:

```
mqtt-client --host HOST sub --all
mqtt-client --host HOST sub "test/#"
echo "test/#" | mqtt-client --host HOST sub
```

## Licensing

Released under BSD license.
