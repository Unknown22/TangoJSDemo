index_file_source = '''<!DOCTYPE html>

<html>

  <head>
    <meta charset="UTF-8">

    <script src="node_modules/ecma-proposal-object-values-entries/polyfill.js"></script>

    <script src="node_modules/html-imports-firefox-patch/patch.js"></script>
    <script src="node_modules/webcomponents.js/HTMLImports.js"></script>

    <script src="node_modules/moment/min/moment.min.js"></script>
    <script src="node_modules/chart.js/dist/Chart.js"></script>

    <script src="node_modules/tangojs-core/lib/tangojs-core.js"></script>
    <script src="node_modules/tangojs-connector-local/lib/tangojs-connector-local.js"></script>
    <script src="node_modules/tangojs-connector-local/lib/demo-model.js"></script>
    <script src="node_modules/tangojs-web-components/dist/tangojs-web-components.js"></script>

    <script type="text/javascript">
      (function (window) {
        'use strict'
        const model = window.tangojsLocalDemoModel.createModel()
        const conn = new window.tangojs.connector.local.LocalConnector(model)
        window.tangojs.core.setConnector(conn)
      })(window)
    </script>

    <style>
      form div label {
        min-width: 250px;
        display: block;
        float: left;
      }
    </style>

    <link rel="import" href="dist/components/html-led-element.html">
    <link rel="import" href="dist/components/html-tree-element.html">

    <link rel="import" href="node_modules/tangojs-web-components/dist/components/tangojs-label.html">
    <link rel="import" href="node_modules/tangojs-web-components/dist/components/tangojs-line-edit.html">
    <link rel="import" href="node_modules/tangojs-web-components/dist/components/tangojs-command-button.html">
    <link rel="import" href="node_modules/tangojs-web-components/dist/components/tangojs-state-led.html">
    <link rel="import" href="node_modules/tangojs-web-components/dist/components/tangojs-trend.html">
    <link rel="import" href="node_modules/tangojs-web-components/dist/components/tangojs-form.html">
    <link rel="import" href="node_modules/tangojs-web-components/dist/components/tangojs-device-tree.html">

  </head>

  <body>

    <form>

      <div>
        <label>tangojs-label</label>
        <tangojs-label
          model="tangojs/test/dev1/sine_trend"
          poll-period="500"
          show-name
          show-unit
          show-quality>
        </tangojs-label>
      </div>

      <div>
        <label>tangojs-line-edit</label>
        <tangojs-line-edit
          model="tangojs/test/dev1/scalar"
          poll-period="1000"
          show-name
          show-unit
          show-quality>
        </tangojs-line-edit>
      </div>

      <div>
        <label>tangojs-line-edit</label>
        <tangojs-line-edit
          model="tangojs/test/dev1/boolean"
          poll-period="1000"
          show-name
          show-unit
          show-quality>
        </tangojs-line-edit>
      </div>


      <div>
        <label>tangojs-command-button</label>
        <tangojs-command-button
          model="tangojs/test/dev1/double_arg"
          parameters="2">
          Double Me!
        </tangojs-command-button>
      </div>

      <div>
        <label>x-led</label>
        <x-led color="#FFFF00" on></x-led>
      </div>

      <div>
        <label>tangojs-state-led</label>
        <tangojs-state-led
          model="tangojs/test/dev1"
          poll-period="1000"
          show-name
          show-led>
        </tangojs-state-led>
      </div>

      <div>
        <label>tangojs-command-button</label>
        <tangojs-command-button model="tangojs/test/dev1/goto_on">
          state: ON
        </tangojs-command-button>
        <tangojs-command-button model="tangojs/test/dev1/goto_off">
          state: OFF
        </tangojs-command-button>
        <tangojs-command-button model="tangojs/test/dev1/goto_fault">
          state: FAULT
        </tangojs-command-button>
        <tangojs-command-button model="tangojs/test/dev1/goto_alarm">
          state: ALARM
        </tangojs-command-button>
      </div>

      <div>
        <label>tangojs-trend</label>
        <tangojs-trend
          style="display: inline-block; width: 500px; height: 400px;"
          model="tangojs/test/dev1/sine_trend,tangojs/test/dev1/scalar"
          poll-period="1000"
          data-limit="15">
        </tangojs-trend>
      </div>

      <div>
        <label>tangojs-form</label>
        <tangojs-form
          style="display: inline-block; width: 600px;"
          model="tangojs/test/dev1,tangojs/test/dev1/sine_trend,tangojs/test/dev1/scalar,
            tangojs/test/dev1/goto_fault"
          poll-period="1000">
        </tangojs-form>
      </div>

      <div>
        <label>x-tree</label>
        <x-tree checkboxes></x-tree>
      </div>

      <div>
        <label>tangojs-device-tree</label>
        <tangojs-device-tree></tangojs-device-tree>
      </div>

    </form>

    <script type="text/javascript">
      (function (window) {

        const cmdBtn = window.document.querySelector('tangojs-command-button')

        cmdBtn.addEventListener('tangojs-command-result', (event) => {
          const value = event.detail.deviceData.value
          alert(`command: ${cmdBtn.model}(${cmdBtn.parameters}) = ${value}`)
        })

        window.document.querySelector('x-tree').model = [
          ['root1', [
            ['child11', 'value1'],
            'child12'
          ]],
          ['root2', []]
        ]

        window.document.querySelector('tangojs-device-tree').addEventListener(
          'selected',
          (event) => {
            console.log('EVENT', event)
          }
        )

        setTimeout(() => {

          const trend = document.createElement('tangojs-trend')
          trend.model = ["tangojs/test/dev1/sine_trend", "tangojs/test/dev1/scalar"]
          trend.pollPeriod = 1000
          trend.dataLimit = 15

          const div = document.createElement('div')
          div.appendChild(trend)

          document.querySelector('form').appendChild(trend)

          setTimeout(() => {
            const t = trend
            Object.assign(t.style, {
              display: 'inline-block',
              width: '700px',
              height: '400px'
            })

          }, 2000)

        }, 2000)

      })(window)
    </script>

  </body>

</html>'''