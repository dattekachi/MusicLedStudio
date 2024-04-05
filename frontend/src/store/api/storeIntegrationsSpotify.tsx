/* eslint-disable import/no-cycle */
/* eslint-disable no-param-reassign */
import { produce } from 'immer'
import { Mls } from '../../api/mls'
import type { IStore } from '../useStore'

const storeIntegrationsSpotify = (set: any) => ({
  getSpTriggers: async () => {
    const resp = await Mls('/api/integrations', set, 'GET')
    // const res = await resp.json()
    if (resp) {
      set(
        produce((state: IStore) => {
          state.spotify.spotify = resp.spotify
        }),
        false,
        'spotify/getTriggers'
      )
    }
  },
  addSpSongTrigger: async ({
    scene_id,
    song_id,
    song_name,
    song_position
  }: any) => {
    await Mls('/api/integrations/spotify/spotify', 'POST', {
      scene_id,
      song_id,
      song_name,
      song_position
    })
  },
  editSpSongTrigger: async ({
    scene_id,
    song_id,
    song_name,
    song_position
  }: any) => {
    await Mls('/api/integrations/spotify/spotify', 'PUT', {
      scene_id,
      song_id,
      song_name,
      song_position
    })
  },
  toggleSpTrigger: (SpotifyId: string, config: any) =>
    Mls(`/api/integrations/spotify/${SpotifyId}`, 'PUT', config),
  deleteSpTrigger: async (config: any) => {
    await Mls('/api/integrations/spotify/spotify', 'DELETE', config)
    // set(state=>state.getIntegrations())
  }
})

export default storeIntegrationsSpotify
