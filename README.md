# Oshinko CLI RPM development

This repository contains the rpm .spec file to create a rpm version of
[oshinko-cli](https://github.com/radanalyticsio/oshinko-cli).


## Building the RPM

Before building the RPM, you must install the `fedora-packager` package:

```
sudo dnf install fedora-packager
```

After that, prepare the RPM workspace by running the following command:

```
rpmdev-setuptree
```

Clone the repo and download the files required to build the RPM:

```
git clone https://github.com/rimolive/oshinko-cli-rpm
cd oshinko-cli-rpm
spectool -g -R oshinko-cli.spec
```

At last, run the build:

```
rpmbuild ba oshinko-cli.spec
```