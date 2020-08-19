
from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

# with open('HISTORY.md') as history_file:
#     HISTORY = history_file.read()

setup_args = dict(
    name='gstreamer-rgw-sink',
    version='0.0.4',
    description='Gstreamer sink plugin to rgw ceph object storage',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    author='Neeha Kompala & Jason Weng',
    author_email='jweng2017@gmail.com',
    keywords=['Gstreamer', 'Ceph Object Storage', 'RGW', 'Python 3'],
    url='https://github.com/Streaming-multiple-video-sources-Edge/gstreamer-rgw-sink.git',
    download_url='https://github.com/Streaming-multiple-video-sources-Edge/gstreamer-rgw-sink/archive/v0.0.4.tar.gz',
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",    
        "Intended Audience :: Developers",      
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",   
        "Programming Language :: Python :: 3",     
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    python_requires='>=3.6',
)

install_requires = [
    'boto3',
    'botocore',
    'PyGObject>=3.34.0',
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
