
from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='gstreamer-rgw-sink',
    version='0.0.1',
    description='Gstreamer sink plugin to rgw ceph object storage',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='',
    author='Neeha Kompala & Jason Weng'
    author_email='nkompala@redhat.com', 'jweng2017@gmail.com'
    keywords=['Gstreamer', 'Ceph Object Storage', 'RGW', 'Python 3'],
    url='https://github.com/Streaming-multiple-video-sources-Edge/gstreamer-rgw-sink.git',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved",
        "Operating System :: POSIX :: Linux",
        "Natural Language :: English",
        "Topic :: Software Development", 
    ],
    python_requires='>=3.6',
)

install_requires = [
    'boto3',
    'botocore',
    
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
