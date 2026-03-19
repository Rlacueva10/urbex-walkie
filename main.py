name: Build APK

on:
  push:
    branches: [ "main" ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Install dependencies
      run: |
        sudo apt update
        sudo apt install -y python3-pip git zip unzip openjdk-17-jdk
        pip install buildozer cython

    - name: Initialize buildozer
      run: |
        buildozer init

    - name: Configure buildozer
      run: |
        sed -i 's/title = .*/title = UrbexWalkie/' buildozer.spec
        sed -i 's/package.name = .*/package.name = urbexwalkie/' buildozer.spec
        sed -i 's/package.domain = .*/package.domain = org.test/' buildozer.spec
        sed -i 's/requirements = .*/requirements = python3,kivy,pyaudio/' buildozer.spec
        echo "android.permissions = INTERNET,RECORD_AUDIO" >> buildozer.spec

    - name: Build APK
      run: |
        buildozer -v android debug

    - name: Upload APK
      uses: actions/upload-artifact@v4
      with:
        name: apk
        path: bin/*.apk
