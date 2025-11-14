import { h } from 'vue'
import { NInput, NSelect, NDatePicker } from 'naive-ui'

export function renderQueryItem(config, model) {
  const key = config.key
  const value = model[key]

  const commonProps = {
    value,
    'onUpdate:value': (val) => {
      model[key] = val
    },
    placeholder: config.placeholder || ''
  }

  switch (config.type) {
    case 'input':
      return h(NInput, commonProps)
    case 'select':
      return h(NSelect, {
        ...commonProps,
        options: config.options || []
      })
    case 'multiselect':
      return h(NSelect, {
        ...commonProps,
        multiple: true,
        options: config.options || []
      })
    case 'daterange':
      return h(NDatePicker, {
        ...commonProps,
        type: 'daterange'
      })
    default:
      return null
  }
}
