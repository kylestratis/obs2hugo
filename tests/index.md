---
frozen: true
---

+++
categories = ['ham radio', 'aprs', 'sdr']
date = '2022-07-16'
description = 'A tutorial for receiving APRS traffic with a software-defined radio and forwarding it to the Internet'
draft = true
keywords = ['ham radio', 'aprs', 'sdr', 'software defined radio', 'mac', 'xastir', 'rtlsdr']
title = "Get Started with APRS with RTLSDR and Xastir on Mac"
+++

# Get Started with APRS with RTLSDR and Xastir on Mac

Recently, a good friend of mine discovered the joys of amateur radio and, knowing that I'm a licensed ham, started asking questions. I haven't touched a radio in years, but an itch that needed scratching awakened in me.

Radio has always been magical to me: hyperlocal (mostly), unpredictable operating conditions, and harnessig nature's power just to chat. Having been raised on the Internet, I'm not one for voice communication, so I've been exploring the digital amateur radio modes. 

APRS (**A**utomated **P**acket **R**eporting **S**ystem) is one such mode and is used for reporting real-time data, such as the GPS coordinates of a mobile station.

APRS is also one of the more accessible modes to get started with, even without being a licensed amateur radio operator. Without being licensed, you can:
- See the locations of mobile stations on the move
- See the locations of fixed stations forwarding data to the Internet (iGates)
- Forward packets that you pick up to the Internet
 
If you visit [APRS.fi](https://aprs.fi), you can see all the stations and information that volunteer iGate operators are passing from the air to the Internet.

 Thanks to the explosion of [RTLSDRs](https://wiki.radioreference.com/index.php/RTL-SDR), getting started with a digital mode like APRS is cheaper than ever. Any RTL-SDR and antenna should work, but I personally use the [Nooelec NESDR Smart v4](https://amzn.to/3j5igby) (ref link).
 
 In this article, you will learn how to use a low-cost RTLSDR radio along with the open-source Xastir software to listen to APRS communications around you and to link what you hear to the Internet, turning your station into an iGate.

### Installation
Installation of Xastir on MacOS requires a few steps:
- Installing the prerequisites
- Getting the Xastir source code
- Configuring the build
- Building the code

Now, this sounds daunting, but this guide and some additional resources will help you through any problems that may come up.

#### Installing the Prerequisites
> [!NOTE]
> These instructions are slightly modified from the [official Xastir documentation](https://xastir.org/index.php/Homebrew).

The first things you'll need to install or make sure you have installed are:
- XCode
- Homebrew
- XQuartz

Installing XCode and Homebrew, if you haven't already, just takes two shell commands:
 `$ xcode-select --install`
 and
 `$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

XQuartz comes next, which allows you to run X11 Windowing System applications on MacOS. That can be installed [from a DMG file on their website](https://www.xquartz.org/).

After installing these, you'll need to install the toolchain needed to build Xastir as well as the rtsldr and socat software. This can be done via Homebrew in a single command:
```bash
$ brew install gcc openmotif graphicsmagick pcre shapelib libgeotiff proj curl berkeley-db@4 git autoconf automake socat librtlsdr
```

Next, you'll install `multimon-ng`, which will automatically decode the APRS signal (among others, like POCSAG) for you.

##### Installing multimon-ng
Installing `multimon-ng` will be good practice for installing Xastir, as it also requires you to clone down the Git repository and build the application from source. The following commands will pull down the code, build it, and install it:
```bash
$ git clone https://github.com/EliasOenal/multimon-ng
$ cd multimon-ng
$ mkdir build
$ cd build
$ cmake ..
$ make
$ sudo make install
```

#### Getting the Xastir Source Code
If you're familiar with Git, then this should be pretty straightforward for you. If not, don't worry because pulling down external code with Git is a single command and should work out of the box. Navigate to where you want to put the Xastir code, then run:
`git clone https://github.com/Xastir/Xastir.git`

This will put the source code into the `Xastir` directory within your current working directory. Move into the `Xastir` directory and run the boostrap script:
```bash
$ cd Xastir
$ ./boostrap.sh
```
![[t.jpg]]
#### Configuring the Xastir Build
The following commands will create a `build` directory and set up flags that will allow you to have online map caching available:
```bash
$ mkdir -p build
$ cd build
$ ../configure CPPFLAGS="-I/usr/local/opt/berkeley-db@4/include" LDFLAGS="-L/usr/local/opt/berkeley-db@4/lib"
```

#### Building Xastir
Next, run `make` and then `sudo make install` to build the code and install it. You can verify that all has worked thus far by running `xastir &` which will launch XQuartz and Xastir itself.

You've just installed a number of tools and utilities to help you not only use Xastir to map reported APRS positions, but to receive the radio signal from your RTLSDR and decode it for Xastir's use. Before you begin using Xastir, you'll have to configure it and the supporting cast of tools.

![[xastir-configure.png]]

Open the Station menu and fill in your callsign and and GPS coordinates, along with any comments you want to attach to your station.
