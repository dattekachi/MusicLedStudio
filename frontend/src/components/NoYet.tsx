import { Card, CardHeader } from '@mui/material'
import { Info } from '@mui/icons-material'
import PropTypes from 'prop-types'

interface NoYetProps {
  type?: string
}

const NoYet: React.FC<NoYetProps> = ({ type }): JSX.Element => (
  <Card>
    <CardHeader
      avatar={<Info />}
      title={`Không có ${type} nào`}
      subheader={`Bạn có thể thêm ${type} bằng cách sử dụng nút hình dấu cộng bên dưới`}
    />
  </Card>
)

NoYet.propTypes = {
  type: PropTypes.string
}

NoYet.defaultProps = {
  type: 'Thing'
}

export default NoYet
