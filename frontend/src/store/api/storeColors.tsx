/* eslint-disable no-return-await */
/* eslint-disable no-param-reassign */
/* eslint-disable import/no-cycle */
import { produce } from 'immer'
import { Mls } from '../../api/mls'
import type { IStore } from '../useStore'

const storeColors = (set: any) => ({
  colors: {
    colors: {
      user: {} as Record<string, string>,
      builtin: {} as Record<string, string>
    },
    gradients: {
      user: {} as Record<string, string>,
      builtin: {} as Record<string, string>
    }
  },
  getColors: async () => {
    const resp = await Mls('/api/colors', set)
    if (resp) {
      set(
        produce((s: IStore) => {
          s.colors = resp
        }),
        false,
        'gotColors'
      )
    }
  },
  // HERE API DOC
  addColor: async (config: Record<string, string>) =>
    await Mls(
      '/api/colors',
      'POST',
      { ...config } // { 'name': 'string' }
    ),
  deleteColors: async (colorkey: string[]) =>
    await Mls('/api/colors', 'DELETE', {
      data: colorkey
    })
})

export default storeColors
