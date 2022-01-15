# -*- coding: utf-8 -*-

#!/bin/bash
VERSION="$(echo `cat VERSION` | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"


docker build -t localhost:32000/app-backend:${VERSION} .

docker push localhost:32000/app-backend:${VERSION}