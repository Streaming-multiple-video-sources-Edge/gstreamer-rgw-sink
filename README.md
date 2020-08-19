Gstreamer ceph rgw sink plugin. 
Streams video from a src to ceph object storage. 

# Pip install
pip install gstreamer-rgw-sink

# PART 1: Install 
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
    
    pip install gstreamer-rgw-sink 
 ```
If you are running ubuntu:
```
    cd gstreamer-rgw-sink

    python3 -m venv venv
    source venv/bin/activate
    pip install -U wheel pip setuptools
    pip install -r requirements.txt
    
    pip install gstreamer-rgw-sink
    
```

# PART 2: Exporting plugin 
```
   export GST_PLUGIN_PATH=$GST_PLUGIN_PATH:$PWD/venv/lib/gstreamer-1.0/:$PWD/venv/lib/python3.6/site-packages/gstreamer-rgw-sink
```

# PART 3: Inspect plugin
```
      gst-inspect-1.0 python
      
      You should see something like this,
    
      Plugin Details:
      Name                     python
      Description              loader for plugins written in python
      Filename                 /work/gstreamer-rgw-sink/venv/lib/gstreamer-1.0/libgstpython.cpython-36m-x86_64-linux-gnu.so
      Version                  1.14.5
      License                  LGPL
      Source module            gst-python
      Binary package           GStreamer GObject Introspection overrides for Python 
      Origin URL               http://gstreamer.freedesktop.org

      cephrgwsink: cephrgwsinkSink

      1 features:
      +-- 1 elements

```

# Example pipeline 
```
gst-launch-1.0 -v souphttpsrc location=https://youtubelink.com ! cephrgwsink cephrgwsink endpointurl=replaceME accesskey=replaceME secretkey=replaceME bucket=replaceME partsize=replaceME key=replaceME limitsize=replaceME
```





