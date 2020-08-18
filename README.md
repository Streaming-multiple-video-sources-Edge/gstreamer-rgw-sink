Gstreamer ceph rgw sink plugin. 
Streams video from a src to ceph object storage. 

# Pip install
```
pip install gstreamer-rgw-sink
```

# Developer install 
```
git clone https://github.com/Streaming-multiple-video-sources-Edge/gstreamer-rgw-sink.git
```

If you are NOT running ubuntu:
```
    podman run -ti --privileged --net=host -v `pwd`:/work docker.io/jweng1/gst-base-image:v1
    cd work
    cd gstreamer-rgw-sink

    python3 -m venv venv
    source venv/bin/activate
    pip install -U wheel pip setuptools
    pip install -r requirements.txt

    export GST_PLUGIN_PATH=$GST_PLUGIN_PATH:$PWD/venv/lib/gstreamer-1.0/:$PWD/gst/
    gst-inspect-1.0 python
 ```
If you are running ubuntu:
```
    cd gstreamer-rgw-sink

    python3 -m venv venv
    source venv/bin/activate
    pip install -U wheel pip setuptools
    pip install -r requirements.txt

    export GST_PLUGIN_PATH=$GST_PLUGIN_PATH:$PWD/venv/lib/gstreamer-1.0/:$PWD/gst/
    gst-inspect-1.0 python
```


# Example pipeline 
```
gst-launch-1.0 -v souphttpsrc location=https://youtubelink.com ! cephrgwsink cephrgwsink endpointurl=replaceME accesskey=replaceME secretkey=replaceME bucket=replaceME partsize=replaceME key=replaceME limitsize=replaceME
```





