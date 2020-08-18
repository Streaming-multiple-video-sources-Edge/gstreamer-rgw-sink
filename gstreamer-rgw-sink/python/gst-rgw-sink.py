import gi
import sys
import os
import io
import argparse
import boto3
import botocore
import base64
import threading
import logging
from boto3.s3.transfer import TransferConfig
gi.require_version('Gst', '1.0')
gi.require_version('GstBase', '1.0')
from gi.repository import Gst, GObject, GstBase


# Initializes Gstreamer, it's variables, paths
GObject.threads_init()
Gst.init(None)

#default variables
DEFAULT_BUCKET = "my-bucket"
DEFAULT_COUNT = 0
DEFAULT_KEY = 'mykey'
DEFAULT_PART_SIZE = 5 * 1024 * 1024 #5mb
DEFAULT_LIMIT_SIZE= 107374182400 # 100gb

DEFAULT_ENDPOINT = "replace me"
DEFAULT_ACCESS = "replace me"
DEFAULT_SECRET = "replace me"


FORMATS = "{RGBx,BGRx,xRGB,xBGR,RGBA,BGRA,ARGB,ABGR,RGB,BGR}"

def upload_part(self,data):
    upload_id = self.thr_args['UploadId']
    part = self.s3.upload_part(Bucket=self.bucket, Key=self.key, PartNumber=self.count+1, UploadId=upload_id, Body=data.getvalue())

    lock = self.thr_args['Lock']
    if lock.acquire():
        self.thr_args['PartInfo']['Parts'].append({'PartNumber': self.count+1, 'ETag': part['ETag']})
        lock.release()

    print("ETag ********* " + part['ETag'])
    logging.info("%d: -><- Part ID %d is ending", self.count+1, self.count+1)
    return

def handle_part(self,data):
    print(">> Uploading part: " + str(self.count + 1))
    upload_part(self,data)


#sink element
class CephRGW(GstBase.BaseSink):

    #plugin name
    GST_PLUGIN_NAME = 'cephrgwsink'
    __gtype_name__ = 'cephrgwsink'

    #plugin description
    __gstmetadata__ = ('cephrgwsinkSink', #name
                      'Sink element', #transform
                      'A sink element to store data to ceph rgw storage', #description
                      'Jason Weng, Neeha Kompala') #authors

    #to make pad templates visible for plugin, define gsttemplates field
    __gsttemplates__  = Gst.PadTemplate.new("sink",
                        Gst.PadDirection.SINK,
                        Gst.PadPresence.ALWAYS,
                        Gst.Caps.from_string(f"video/x-raw,format={FORMATS}"))

    #object properties
    __gproperties__ = {
        "endpointurl": (GObject.TYPE_STRING,
                     "Endpoint url",
                     "A property that contains str",
                     DEFAULT_ENDPOINT,  # default
                     GObject.ParamFlags.READWRITE
                     ),

        "accesskey": (GObject.TYPE_STRING,
                     "Access key",
                     "Access key for ceph rgw",
                     DEFAULT_ACCESS,  # default
                     GObject.ParamFlags.READWRITE
                     ),

        "secretkey": (GObject.TYPE_STRING,
                     "Secret key",
                     "Secret key for ceph rgw",
                     DEFAULT_SECRET,  # default
                     GObject.ParamFlags.READWRITE
                     ),

        "bucket": (GObject.TYPE_STRING,
                     "Bucket",
                     "Bucket for ceph rgw",
                     DEFAULT_BUCKET,  # default
                     GObject.ParamFlags.READWRITE
                     ),

        "partsize": (GObject.TYPE_INT64,
                     "Part size",
                     "Size of buffer upload to ceph",
                     DEFAULT_PART_SIZE, #min
                     1000000000000000, #max
                     DEFAULT_PART_SIZE,  # default
                     GObject.ParamFlags.READWRITE
                     ),
       
        "key": (GObject.TYPE_STRING,
                     "key",
                     "key for ceph rgw",
                     DEFAULT_KEY,  # default
                     GObject.ParamFlags.READWRITE
                     ),
        
        "limitsize": (GObject.TYPE_INT64,
                     "Max limit size",
                     "Size of maximum  upload to ceph",
                     DEFAULT_PART_SIZE, #min
                     DEFAULT_LIMIT_SIZE, #max
                     DEFAULT_LIMIT_SIZE,  # default
                     GObject.ParamFlags.READWRITE
                     ),
        
      }
      
      
      
    def __init__(self, *args):
        GstBase.BaseSink.__init__(self, *args)

        self.endpoint_url = DEFAULT_ENDPOINT
        self.access_key = DEFAULT_ACCESS
        self.secret_key = DEFAULT_SECRET
        self.bucket = DEFAULT_BUCKET
        self.part_size = DEFAULT_PART_SIZE
        self.key = DEFAULT_KEY
        self.limitsize = DEFAULT_LIMIT_SIZE
        self.count = 0
        self.buffer = []
        self.currsize = 0

        self.temp = io.BytesIO()
        self.thr_args = {}
        self.s3 = None
        self.s3r = None
        self.mpu = None
        self.threads = list()
        self.thr_lock = threading.Lock()

    def do_get_property(self, prop: GObject.GParamSpec):
        if prop.name == 'endpointurl':
            return self.endpoint_url
        elif prop.name == 'accesskey':
            return self.access_key
        elif prop.name == 'secretkey':
            return self.secret_key
        elif prop.name == 'bucket':
            return self.bucket
        elif prop.name == 'partsize':
            return self.part_size
        elif prop.name == 'key':
            return self.key
        elif prop.name == 'limitsize':
            return self.limitsize
        else:
            raise AttributeError('unknown property %s' % prop.name)
            
    def do_set_property(self, prop: GObject.GParamSpec, value):
        if prop.name == 'endpointurl':
            self.endpoint_url = value
        elif prop.name == 'accesskey':
            self.access_key = value
        elif prop.name == 'secretkey':
            self.secret_key = value
        elif prop.name == 'bucket':
            self.bucket = value 
        elif prop.name == 'partsize':
            self.part_size = value
        elif prop.name == 'key':
            self.key = value
        elif prop.name == 'limitsize':
            self.limitsize = value
        else:
            raise AttributeError('unknown property %s' % prop.name)


    def do_start (self):
        # Initialize the connection with Ceph RADOS GW
        self.s3 = boto3.client(service_name = 's3', use_ssl = False, verify = False, endpoint_url = self.endpoint_url,
                            aws_access_key_id = base64.decodebytes(bytes(self.access_key,'utf-8')).decode('utf-8'),
                            aws_secret_access_key = base64.decodebytes(bytes(self.secret_key,'utf-8')).decode('utf-8'),)
        self.s3r = boto3.resource(service_name = 's3', use_ssl = False, verify = False, endpoint_url = self.endpoint_url,
                            aws_access_key_id = base64.decodebytes(bytes(self.access_key,'utf-8')).decode('utf-8'),
                            aws_secret_access_key = base64.decodebytes(bytes(self.secret_key,'utf-8')).decode('utf-8'),)

        response = self.s3.list_buckets()
        # Get a list of all bucket names from the response
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        # Print out the bucket list
        print("Initial bucket List: %s" % buckets)

        if self.bucket not in buckets:
            print('Creating bucket -  ' + self.bucket)
            self.s3.create_bucket(Bucket=self.bucket)

        #Get all buckets
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        # Print out the bucket list
        print("Updated bucket List: %s" % buckets)
        
        self.mpu = self.s3.create_multipart_upload(Bucket=self.bucket, Key=self.key)
        self.thr_args ={'PartInfo': { 'Parts': []},
                    'UploadId': self.mpu['UploadId'],
                    'BucketName': self.bucket,
                    'FileName': self.key,
                    'Lock': self.thr_lock}

        return True
    
    def do_render(self, buffer):
        try:
            #mapping buffer input 
            (result, mapinfo) = buffer.map(Gst.MapFlags.READ)
            assert result

            try:
                data = io.BytesIO(mapinfo.data)

                self.temp.write(data.read())          
                if self.temp.getbuffer().nbytes > self.part_size:
                    self.currsize = self.currsize + self.temp.getbuffer().nbytes
                    print(self.currsize)
                    if(self.currsize > self.limitsize):
                        return Gst.FlowReturn.EOS
                    handle_part(self, self.temp)
                    self.count = self.count + 1
                    self.temp = io.BytesIO()
            finally:
                buffer.unmap(mapinfo)

        except Exception as e:
            logging.error(e)
        return Gst.FlowReturn.OK
      
      
    def do_stop(self):
        handle_part(self,self.temp)
        for i in range(len(self.buffer)):
            print("Size buff: " + str(sys.getsizeof(self.buffer[i])))

        part_info = self.thr_args['PartInfo']

        for p in part_info['Parts']:
            print("DEBUG: PartNumber=%d" % (p['PartNumber']))
            print("DEBUG: ETag=%s" % (p['ETag']))

        print("+ Finishing up multi-part uploads")
        self.s3.complete_multipart_upload( Bucket=self.bucket, Key=self.key, UploadId=self.mpu['UploadId'], MultipartUpload=self.thr_args['PartInfo'] )
        print("+++++++++++++ Uploads complete! +++++++++++++")
        


# Required for registering plugin dynamically
GObject.type_register(CephRGW)
__gstelementfactory__ = (CephRGW.GST_PLUGIN_NAME, Gst.Rank.NONE, CephRGW)
