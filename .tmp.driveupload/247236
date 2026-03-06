/* globals customElements document */
/* eslint-disable unicorn/prefer-dom-node-text-content */

import {basicSetup, EditorState, EditorView, json} from '../vendor/vendor.bundle.js'
import {ApiBaseElement} from './api-base.js'
import {sanityCodeMirrorTheme} from './codemirror-theme.js'
import {getSharedStyleSheets} from './shared-styles.js'

const {lineWrapping} = EditorView

const template = document.createElement('template')
template.innerHTML = `<div class="border-left y-scroll min-h-0">
  <div>
    <h3 class="config-label mar-t-0 hidden">Filter/Projection</h3>
    <header class='flex space-between'>
        <dl class='flex items-center margin-0 pad-3 slab-stat'>
          <dt class='nowrap'>Filter/Projection</dt>
        </dl>
    </header>
    <div id="rule" name="rule" class="cm-s-dracula"></div>
  </div>
</div>
`

class RulePanel extends ApiBaseElement {
  constructor() {
    super()
    this.attachShadow({mode: 'open'}).appendChild(template.content.cloneNode(true))
  }
  updateRule = () => {
    const {functions, rule, selectedIndex} = this.api.store
    const func = functions.find((func) => func.name === selectedIndex)

    if (func.event) {
      const transaction = rule.state.update({
        changes: {
          from: 0,
          insert: JSON.stringify(func.event, null, 2),
          to: rule.state.doc.length,
        },
      })
      rule.dispatch(transaction)
    }
  }

  async connectedCallback() {
    const sheets = await getSharedStyleSheets()
    this.shadowRoot.adoptedStyleSheets = sheets

    this.rule = this.shadowRoot.querySelector('#rule')

    if (this.api) {
      this.api.subscribe(this.updateRule, ['selectedIndex', 'functions'])
      if (this.api.store.selectedIndex) {
        this.updateRule({selectedIndex: this.api.store.selectedIndex})
      }
    }

    this.api.store.rule = new EditorView({
      doc: '\n\n\n\n',
      extensions: [
        basicSetup,
        json(),
        sanityCodeMirrorTheme,
        EditorState.readOnly.of(true),
        lineWrapping,
      ],
      parent: this.rule,
    })
  }

  disconnectedCallback() {
    if (this.api) {
      this.api.unsubscribe(this.updateResponse)
    }
  }
}

customElements.define('rule-panel', RulePanel)
