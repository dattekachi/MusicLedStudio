import { Divider, MenuItem, Select } from '@mui/material'
import { SettingsRow } from './SettingsComponents'
import useStore from '../../store/useStore'

const ExpertFeatures = () => {
  const setFeatures = useStore((state) => state.setFeatures)
  const showFeatures = useStore((state) => state.showFeatures)
  const features = useStore((state) => state.features)

  const effectDescriptions = useStore((state) => state.ui.effectDescriptions)
  const setEffectDescriptions = useStore(
    (state) => state.ui.setEffectDescriptions
  )
  return (
    <>
      {showFeatures.cloud && (
        <SettingsRow
          title="Music Led Cloud"
          checked={features.cloud}
          onChange={() => setFeatures('cloud', !features.cloud)}
        />
      )}
      {showFeatures.webaudio && (
        <SettingsRow
          title="WebAudio"
          checked={features.webaudio}
          onChange={() => setFeatures('webaudio', !features.webaudio)}
        />
      )}
      <SettingsRow
        title="Sao chép sang"
        checked={features.streamto}
        onChange={() => setFeatures('streamto', !features.streamto)}
      />
      <SettingsRow
        title="Chuyển tiếp"
        checked={features.transitions}
        onChange={() => setFeatures('transitions', !features.transitions)}
        step="eight"
      />
      <SettingsRow title="Hiện mô tả hiệu ứng">
        <Select
          disableUnderline
          value={effectDescriptions}
          onChange={(e) =>
            setEffectDescriptions(e.target.value as 'Auto' | 'Show' | 'Hide')
          }
        >
          <MenuItem value="Auto">Auto</MenuItem>
          <MenuItem value="Show">Hiện</MenuItem>
          <MenuItem value="Hide">Ẩn</MenuItem>
        </Select>
      </SettingsRow>
      <Divider sx={{ m: '0.5rem 0 0.25rem 0' }} />
      <SettingsRow
        title="Tần số"
        checked={features.frequencies}
        onChange={() => setFeatures('frequencies', !features.frequencies)}
      />
      <SettingsRow
        title="Trình phát Spotify (cũ)"
        checked={features.spotify}
        onChange={() => setFeatures('spotify', !features.spotify)}
      />

      <SettingsRow
        title="Nền động sóng"
        checked={features.waves}
        onChange={() => setFeatures('waves', !features.waves)}
      />
    </>
  )
}

export default ExpertFeatures
