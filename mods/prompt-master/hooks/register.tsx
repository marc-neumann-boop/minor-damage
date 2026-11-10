import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register } from 'claude-code'

import type { Status } from '../types'

const status = atom({ plugin: 'prompt-master', key: 'status' } as const, 'idle' as Status)
const previous = atom({ plugin: 'prompt-master', key: 'previous' } as const, null as string | null)

const SYSTEM = `You are Prompt Master, an expert prompt engineer. Rewrite the user's draft prompt for an AI coding assistant (Claude Code) so it gets a better result.

Rules:
- Keep the user's intent, scope, facts, names, file paths, code and constraints exactly. Never invent requirements.
- Make it clear and specific: state the goal, relevant context, concrete requirements, constraints, and what "done" looks like (expected output / format) when they can be inferred.
- Use short paragraphs or bullet points when that helps; keep simple asks short.
- Write in the same language as the draft, from the user's point of view ("I want...", "Please...").
- Output ONLY the rewritten prompt. No preamble, no quotes, no explanation.`

// Rewrites `text` and puts the result in the prompt box for review.
async function rewrite($: EngineInterface, text: string): Promise<string> {
  const draft = text.trim()
  if (draft === '') {
    $.ui.toast('Prompt Master: type a prompt first')
    return 'Type a prompt first.'
  }
  if ((await read($, status)) === 'busy') return 'Already rewriting.'

  await update($, status, () => 'busy')
  try {
    const r = await $.model.complete({
      model: 'sonnet',
      system: SYSTEM,
      prompt: `<draft>\n${draft}\n</draft>`,
      maxTokens: 2048,
      timeoutMs: 60000,
    })
    if (!r.isAnswered) {
      $.ui.toast(`Prompt Master failed: ${r.reason}`)
      return `Rewrite failed: ${r.reason}`
    }
    const better = r.text.trim().replace(/^<draft>\s*|\s*<\/draft>$/g, '')
    await update($, previous, () => draft)
    await $.prompt.fill({ text: better, mode: 'replace' })
    $.ui.toast('Prompt Master: rewritten — review and press Enter')
    return 'Rewritten prompt is in the box.'
  } finally {
    await update($, status, () => 'idle')
  }
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({
      name: 'promptmaster',
      description: 'Rewrite a prompt into a better one (uses the text after the command, or your draft)',
    })
    return next(e)
  })

  on('command.run', { command: 'promptmaster' }, async ($, e) => {
    const text = e.args.trim() || (await $.prompt.read()).text
    return { text: await rewrite($, text) }
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    if (e.props.hasSurvey || e.props.isWorking) return next(e)

    const { Box, Button, Text } = $.ui.resolve(e)
    const isBusy = (await read($, status)) === 'busy'
    const undo = await read($, previous)

    return (
      <Box>
        {isBusy ? (
          <Text dimColor>✨ Prompt Master is rewriting…</Text>
        ) : (
          <Button
            key="pm"
            label="✨ Prompt Master"
            onPress={async () => {
              const box = await $.prompt.read()
              await rewrite($, box.text)
            }}
          />
        )}
        {!isBusy && undo !== null && (
          <Button
            key="undo"
            label="↩ Undo"
            onPress={async () => {
              await $.prompt.fill({ text: undo, mode: 'replace' })
              await update($, previous, () => null)
            }}
          />
        )}
      </Box>
    )
  })

  // Once sent, the undo snapshot is stale.
  on('prompt.submit', async ($, e, next) => {
    await update($, previous, () => null)
    return next(e)
  })
}
