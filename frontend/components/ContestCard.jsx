import Button from '@material-ui/core/Button';
import moment from 'moment';
import PropTypes from 'prop-types';
import React from 'react';

import { Link } from '../common/routes';
import format from '../config/format';
import helpers from '../helpers';
import __ from '../lang/vi';
import JoinContestModal from './JoinContestModal';

moment.locale('vi');

const style = {
  ContestImage: {
    height: '140px',
    width: '140px',
    minWidth: '140px',
  },
};
const Tag = ({ tag }) => {
  const url = `/tags/${helpers.string.clear(tag.name)}`;
  return (
    <Link href={url}>
      <a>{tag.name}</a>
    </Link>
  );
};
Tag.propTypes = {
  tag: PropTypes.shape({
    name: PropTypes.string,
  }).isRequired,
};

// const styles = theme => ({
//   button: {
//     margin: theme.spacing.unit,
//   },
//   paper: {
//     position: 'absolute',
//     width: theme.spacing.unit * 50,
//     backgroundColor: theme.palette.background.paper,
//     boxShadow: theme.shadows[5],
//     padding: theme.spacing.unit * 4,
//   },
// });

class ContestCard extends React.Component {
  constructor(props) {
    super(props);
    this.handleShow = this.handleShow.bind(this);
    this.handleClose = this.handleClose.bind(this);

    this.state = {
      show: false,
    };

    this.handleInputChange = this.handleInputChange.bind(this);
  }

  handleClose() {
    this.setState({ show: false });
  }

  handleShow() {
    // console.log('mở ra');
    this.setState({ show: true });
  }

  handleInputChange(event) {
    const { target } = event;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    const { name } = target;
    this.setState({
      [name]: value,
    });
  }

  render() {
    const { contest } = this.props;
    const { show } = this.state;

    return (
      <div className="p-3 mb-3 bg-wh rounded effect-hover contest d-flex justify-content-between">
        <img
          style={style.CompetitionImage}
          className="mr-3"
          src={contest.avatar}
          alt=""
        />
        <div className="w-100" style={{ overflow: 'hidden' }}>
          <div>
            <Link route="contest" params={{ id: contest.id }}>
              <a>
                <h4 className="d-inline mr-3">
                  {helpers.string.capitalize(contest.title)}
                </h4>
              </a>
            </Link>
            <Link href="/company/id=10">
              <a>{contest.company}</a>
            </Link>
          </div>
          <p className="block-with-text">{contest.description}</p>
          <div>
            <span>{moment(contest.start).format(format.DATE_DEFAULT)}</span>
            {' - '}
            <span>{moment(contest.end).format(format.DATE_DEFAULT)}</span>
            <span>{moment(contest.end).fromNow()}</span>
          </div>
          {/* {contest.tags && (
            <div>
              <i className="fas fa-tags mr-2" style={{ color: '#00000075' }} />
              {contest.tags.map(
                (item, index) => (index === 0 ? (
                  <Tag key={item.id} tag={item} />
                ) : (
                  <React.Fragment key={item.id}>
                    <span> , </span>
                    <Tag tag={item} />
                  </React.Fragment>
                )),
              )}
            </div>
          )} */}
        </div>
        <div
          className="d-flex flex-column text-right"
          style={{
            width: '13rem',
          }}
        >
          <div>{`${contest.prize},000,000${__.common.CurrencySymbol}`}</div>
          <div>{`${contest.teams.total} ${__.common.teams}`}</div>

          {!contest.myTeam && [
            <Button
              variant="contained"
              color="primary"
              onClick={this.handleShow}
              key="joinButton"
            >
              {__.common.JoinContestButton}
            </Button>,
            <JoinContestModal
              contestId={contest.id}
              handleClose={this.handleClose}
              isOpened={show}
              key="joinModal"
            />,
          ]}
        </div>
      </div>
    );
  }
}

ContestCard.propTypes = {
  contest: PropTypes.shape({
    name: PropTypes.string,
    company: PropTypes.string,
    description: PropTypes.string,
  }).isRequired,
};

export default ContestCard;
