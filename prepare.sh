#!/bin/bash

. /usr/local/rpm-specs/setup_env.sh

yum install -y openssl-devel zlib-devel bzip2-devel \
  python34-devel python-sphinx

build_package botan2
