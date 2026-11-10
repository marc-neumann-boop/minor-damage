import { expect, test } from 'claude-code/testing'

const BAND = {
  plugin: 'prompt-master',
  component: 'AbovePrompt',
  props: { hasSurvey: false, isCollapsed: false, isWorking: false, maxRows: 10, scroll: { offset: 0, bodyRows: 10 } },
} as const

test('one click rewrites the draft into the box', async ($, on) => {
  let filled = ''
  on('prompt.read', () => ({ value: { text: 'fix bug login', cursor: 13 } }))
  on('model.complete', () => ({
    value: { isAnswered: true, text: 'Please fix the login bug.', usage: { input_tokens: 1, output_tokens: 1 } },
  }))
  on('prompt.fill', (_, e) => {
    filled = e.text
    return { isFilled: true }
  })
  on('ui.toast', () => ({ value: undefined }))

  const ui = await $.ui.mount({ ...BAND, surface: 'desktop' } as never)
  const button = await ui.find({ type: 'Button', label: /Prompt Master/ })
  expect(button).toBeTruthy()
  await $.ui.press({ plugin: 'prompt-master', key: 'pm', surface: 'desktop' })
  expect(filled).toBe('Please fix the login bug.')
  await ui.unmount()
})
