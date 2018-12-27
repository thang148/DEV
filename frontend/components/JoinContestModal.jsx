import Button from '@material-ui/core/Button';
import Modal from '@material-ui/core/Modal';
import TextField from '@material-ui/core/TextField';
import Typography from '@material-ui/core/Typography';
import gql from 'graphql-tag';
import moment from 'moment';
import PropTypes from 'prop-types';
import React from 'react';
import { Mutation } from 'react-apollo';

moment.locale('vi');
function getModalStyle() {
  const top = 50;
  const left = 50;

  return {
    top: `${top}%`,
    left: `${left}%`,
    transform: `translate(-${top}%, -${left}%)`,
    position: 'absolute',
    width: '500px',
    padding: '8px',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.8,
    shadowRadius: 2,
    backgroundColor: '#ffffff',
  };
}

const CREATE_TEAM = gql`
  mutation JoinContest($contestId: Int!, $teamName: String!) {
    joinContest(contestId: $contestId, teamName: $teamName) {
      team {
        id
        name
      }
      message
      error
    }
  }
`;

export default class JoinContestModel extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      cardTeamName: '',
    };
    this.handleInputChange = this.handleInputChange.bind(this);
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
    const { contestId, handleClose, isOpened } = this.props;
    const { cardTeamName } = this.state;
    return (
      <Mutation mutation={CREATE_TEAM}>
        {(joinContest, { data }) => (
          <Modal
            aria-labelledby="simple-modal-title"
            aria-describedby="simple-modal-description"
            open={isOpened}
            onClose={handleClose}
          >
            <div style={getModalStyle()}>
              <Typography id="modal-title">Tạo nhóm</Typography>
              <TextField
                required
                id="txtTeamName"
                label="Tên nhóm"
                name="cardTeamName"
                margin="normal"
                onChange={this.handleInputChange}
                value={cardTeamName}
              />
              <br />
              <Button
                variant="contained"
                color="primary"
                disabled={!cardTeamName.trim()}
                onClick={(e) => {
                  e.preventDefault();
                  joinContest({
                    variables: {
                      contestId,
                      teamName: cardTeamName,
                    },
                  }).then(({ data: { joinContest: { error } } }) => {
                    if (!error) handleClose();
                  });
                }}
              >
                Xác nhận
              </Button>
              &nbsp;&nbsp;
              <Button
                variant="contained"
                color="secondary"
                onClick={handleClose}
              >
                Hủy
              </Button>
              {data && data.joinContest && data.joinContest.error ? (
                <Typography color="error">Đã có lỗi xảy ra!</Typography>
              ) : null}
            </div>
          </Modal>
        )}
      </Mutation>
    );
  }
}

JoinContestModel.propTypes = {
  contestId: PropTypes.string.isRequired,
  isOpened: PropTypes.bool.isRequired,
  handleClose: PropTypes.func.isRequired,
};
