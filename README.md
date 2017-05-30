# TangoJS Demo

Project to run demo of TangoJS.

If you want to know more follow [TangoJS project](http://tangojs.github.io/).

[mTango](https://bitbucket.org/hzgwpn/mtango/wiki/Home) is backend support for
TangoJS.

## Requirements
* Python 3.4.4+
* pip3.4+
* Mozilla Firefox 45+
  * enable [`dom.webcomponents.enabled`](about:config)
  * enable [`layout.css.grid.enabled`](about:config)
  * use
    [HTMLImports polyfill](http://webcomponents.org/polyfills/html-imports/)
  * apply [this patch](https://github.com/mliszcz/html-imports-firefox-patch)
    just before the polyfill is loaded
* Google Chrome 49+
  * enable [experimental-web-platform-features]( chrome://flags/#enable-experimental-web-platform-features )

One of the following operating system:
* Windows 10
* CentOS 7
* Ubuntu 14 or 16 (Tango 8 or Tango 9)


## Getting started

1. Make sure you have Python (minimum 3.4.4 version) installed.

2. Clone this project:
   ```bash
   $ git clone https://github.com/Unknown22/TangoJSDemo.git && cd TangoJSDemo/
   ```

3. Install requirements:
    ```bash
    $ sudo pip3.4 install -r requirements.txt
    ```

4. Run python:

    ```bash
    $ python3.4 -m tangojsdemo
    ```
or    

4. Install package:
    ```bash
    $ sudo python3.4 setup.py install
    ```

5. Run command:

    ```bash
    $ runtangojsdemo
    ```

6. Follow the instructions.

> If browser will open and you see blank tab, try refresh and check requirements

### Build  and install wheel:

1. Clone this project:
   ```bash
   $ git clone https://github.com/Unknown22/TangoJSDemo.git && cd TangoJSDemo/
   ```

2. Build wheel:
    ```bash
    $ sudo python3.4 setup.py sdist bdist_wheel
    ```

3. Enter do dist folder:
    ```bash
    $ cd dist
    ```

4. Install wheel package:
    ```bash
    $ pip install tangojs_demo-0.X.X-py3-none-any.whl
    ```

## Demo

![TangoJS Demo](tangojsdemo/images/demo.png?raw=true)

## License
MIT license
