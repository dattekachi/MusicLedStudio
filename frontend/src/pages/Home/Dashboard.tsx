/* eslint-disable @typescript-eslint/indent */
/* eslint-disable no-console */
/* eslint-disable @typescript-eslint/no-unused-vars */
/* eslint-disable no-promise-executor-return */
/* eslint-disable no-plusplus */
/* eslint-disable no-await-in-loop */
import { useEffect, useState } from 'react'
import {
  Box,
  Typography,
  useTheme,
  Stack,
  CircularProgress as CircularProgress5,
  Tooltip,
  useMediaQuery
} from '@mui/material'
import { useNavigate } from 'react-router-dom'
import { DeleteForever } from '@mui/icons-material'
import useStore from '../../store/useStore'
import { deleteFrontendConfig, sleep } from '../../utils/helpers'
import Gauge from './Gauge'
import BladeIcon from '../../components/Icons/BladeIcon/BladeIcon'
import Popover from '../../components/Popover/Popover'
import TourHome from '../../components/Tours/TourHome'
import MGraph from '../../components/MGraph'

const Dashboard = () => {
  const theme = useTheme()
  const navigate = useNavigate()
  const scanForDevices = useStore((state) => state.scanForDevices)

  const devices = useStore((state) => state.devices)
  const virtuals = useStore((state) => state.virtuals)
  const scenes = useStore((state) => state.scenes)
  const smallHeight = useMediaQuery(
    '(max-height: 680px) and (min-width: 480px)'
  )
  const xSmallHeight = useMediaQuery('(max-height: 580px)')

  const config = useStore((state) => state.config)
  const getDevices = useStore((state) => state.getDevices)
  const getVirtuals = useStore((state) => state.getVirtuals)

  const getScenes = useStore((state) => state.getScenes)
  const [scanning, setScanning] = useState(-1)

  const pixelTotal = Object.keys(devices)
    .map((d) => devices[d].config.pixel_count)
    .reduce((a, b) => a + b, 0)

  const devicesOnline = Object.keys(devices).filter((d) => devices[d].online)
  const virtualsReal = Object.keys(virtuals).filter(
    (d) => !virtuals[d].is_device
  )

  const pixelTotalOnline = Object.keys(devices)
    .map((d) => devices[d].online && devices[d].config.pixel_count)
    .reduce((a, b) => a + b, 0)

  const getSystemConfig = useStore((state) => state.getSystemConfig)
  const setSystemConfig = useStore((state) => state.setSystemConfig)

  const onSystemSettingsChange = (setting: string, value: any) => {
    setSystemConfig({ [setting]: value }).then(() => getSystemConfig())
  }
  const handleScan = () => {
    setScanning(0)
    scanForDevices()
      .then(async () => {
        for (let sec = 1; sec <= 30; sec++) {
          if (scanning === -1) break
          await sleep(1000).then(() => {
            getDevices()
            getVirtuals()
            if (scanning !== -1) setScanning(sec)
          })
        }
      })
      .then(() => {
        setScanning(-1)
      })
  }

  useEffect(() => {
    getScenes()
  }, [])

  return (
    <div className="Content">
      <Stack spacing={[0, 0, 2, 2, 2]} alignItems="center">
        {!xSmallHeight && (
          <>
            <Stack spacing={2} direction="row" className="hideTablet">
              <Gauge
                value={pixelTotal > 0 ? 100 : 0}
                unit="Tổng số LED"
                total={pixelTotal}
                current={pixelTotal}
              />
              <Gauge
                value={Object.keys(devices).length > 0 ? 100 : 0}
                unit="Thiết bị"
                total={Object.keys(devices).length}
                current={Object.keys(devices).length}
                onClick={() => navigate('/Devices')}
              />
              <Gauge
                value={virtualsReal.length > 0 ? 100 : 1}
                unit="Đèn ảo"
                total={Object.keys(virtuals).length}
                current={virtualsReal.length}
                onClick={() => navigate('/Devices')}
              />
              <Gauge
                unit="Cấu hình riêng"
                total={
                  config.user_presets &&
                  Object.values(config.user_presets)?.length
                    ? Object.values(config.user_presets)
                        .map((e: any) => Object.keys(e).length)
                        .reduce((a: number, b: number) => a + b, 0)
                    : 0
                }
                current={
                  config.user_presets &&
                  Object.values(config.user_presets).length
                    ? Object.values(config.user_presets)
                        .map((e: any) => Object.keys(e).length)
                        .reduce((a: number, b: number) => a + b, 0)
                    : 0
                }
              />
            </Stack>
            <Stack spacing={2} direction="row" className="hideTablet">
              <Gauge
                unit="Tổng LED hoạt động"
                total={pixelTotal}
                current={pixelTotalOnline}
              />
              <Gauge
                unit="Thiết bị hoạt động"
                total={Object.keys(devices).length}
                current={Object.keys(devicesOnline).length}
                onClick={() => navigate('/Devices')}
              />
              <Gauge
                unit="Cảnh"
                total={Object.keys(scenes).length}
                current={Object.keys(scenes).length}
                onClick={() => navigate('/Scenes')}
              />
              <Gauge
                unit="Màu tùy chỉnh"
                total={
                  ((config.user_colors &&
                    Object.keys(config.user_colors)?.length) ||
                    0) +
                  ((config.user_gradients &&
                    Object.keys(config.user_gradients)?.length) ||
                    0)
                }
                current={
                  ((config.user_colors &&
                    Object.keys(config.user_colors)?.length) ||
                    0) +
                  ((config.user_gradients &&
                    Object.keys(config.user_gradients)?.length) ||
                    0)
                }
              />
            </Stack>
          </>
        )}

        <div style={{ height: '2rem' }} />
        <div
          style={{
            margin: 'auto',
            width: '70%',
            padding: '30px',
            background: '#333',
            display: 'flex',
            justifyContent: 'center',
            borderRadius: '1%',
            alignItems: 'center',
            flexDirection: 'column'
          }}
        >
          <p style={{ fontSize: '30px' }}>MUSIC LED STUDIO </p> <br /> Phần mềm
          điều khiển led nháy theo nhạc <br /> <br /> Website:
          bit.ly/led-ambilight <br /> Fanpage: facebook.com/thesetup.store{' '}
          <br /> Zalo/Sđt hỗ trợ: 0328.593.543 <br />
          <div style={{ height: '1rem' }} />
          <Stack spacing={2} direction={smallHeight ? 'row' : 'column'}>
            <Stack spacing={2} direction="row">
              <Tooltip title="Tìm led Ambilight Wifi">
                <Box sx={{ m: 0, position: 'relative', zIndex: 0 }}>
                  <Popover
                    type="fab"
                    text="Create Segments?"
                    noIcon
                    onConfirm={() => {
                      onSystemSettingsChange('create_segments', true)
                      handleScan()
                    }}
                    onCancel={() => {
                      onSystemSettingsChange('create_segments', false)
                      handleScan()
                    }}
                  >
                    {scanning > -1 ? (
                      <Typography
                        variant="caption"
                        style={{ fontSize: 10 }}
                        component="div"
                      >
                        {`${Math.round((scanning / 30) * 100)}%`}
                      </Typography>
                    ) : (
                      <BladeIcon name="wled" />
                    )}
                    {scanning > -1 && (
                      <CircularProgress5
                        size={68}
                        sx={{
                          color: theme.palette.primary.main,
                          position: 'absolute',
                          top: -6,
                          left: -6,
                          zIndex: 1
                        }}
                      />
                    )}
                  </Popover>
                </Box>
              </Tooltip>

              <Tooltip title="Xóa dữ liệu">
                <span style={{ margin: 0, zIndex: 0 }}>
                  <Popover
                    type="fab"
                    color="primary"
                    style={{ margin: '8px' }}
                    icon={<DeleteForever />}
                    text="Delete frontend data?"
                    onConfirm={() => {
                      deleteFrontendConfig()
                    }}
                  />
                </span>
              </Tooltip>
              <Tooltip title="Trợ lý hướng dẫn">
                <span style={{ margin: 0, zIndex: 0 }}>
                  <TourHome className="step-one" variant="fab" />
                </span>
              </Tooltip>
            </Stack>
          </Stack>
        </div>
      </Stack>
      {config.dev_mode && <MGraph />}
    </div>
  )
}

export default Dashboard
