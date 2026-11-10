export type Status = 'idle' | 'busy'

declare module 'claude-code' {
  interface PluginState {
    'prompt-master': { status: Status; previous: string | null }
  }
}
