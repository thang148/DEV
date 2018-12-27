import Typography from '@material-ui/core/Typography';
import gql from 'graphql-tag';
import React from 'react';
import { Mutation } from 'react-apollo';

import __ from '../lang/vi';

const SUBMISSION = gql`
  mutation Submission($contestId: ID!, $note: String) {
    createSubmission(contestId: $contestId, note: $note) {
      s3 {
        url
        fields
      }
      error {
        error
        message
      }
    }
  }
`;

class Submission extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      form: {
        file: null,
        note: '',
      },
      submitBtn: {
        submitBtnDisabled: false,
        submitBtnName: __.common.SubmissionSubmit,
      },
      error: null,
    };

    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.fileRef = React.createRef();
  }

  setSubmitState(sending = false) {
    this.setState({
      submitBtn: {
        submitBtnDisabled: sending,
        submitBtnName: sending
          ? __.common.SubmissionSubmitting
          : __.common.SubmissionSubmit,
      },
    });
  }

  handleInputChange({ target }) {
    const value = target.type === 'file' ? target.files[0] : target.value;
    const { form } = this.state;
    form[[target.name]] = value;
    this.setState({ form });
  }

  async handleSubmit(event, createSubmission) {
    event.preventDefault();

    this.setState({ error: null });
    this.setSubmitState(true);

    const { contestId = 1 } = this.props;
    const {
      form: { note },
    } = this.state;

    try {
      const { data } = await createSubmission({
        variables: {
          contestId,
          note,
        },
      });
      const { s3 } = data.createSubmission;
      if (!s3) {
        this.setSubmitState(false);
      } else {
        const formData = new FormData();
        const fields = {
          ...JSON.parse(s3.fields),
          file: this.fileRef.current.files[0],
        };
        Object.keys(fields).forEach((key) => {
          formData.append(key, fields[key]);
        });
        await fetch(s3.url, {
          method: 'POST',
          body: formData,
        });
        this.setSubmitState(false);
      }
    } catch (error) {
      this.setState({ error });
      this.setSubmitState(false);
    }
  }

  render() {
    const { form, submitBtn, error } = this.state;
    return (
      <Mutation mutation={SUBMISSION}>
        {(createSubmission, { data }) => (
          <div className="form-submmission">
            <h2 className="text-center">{__.common.Submission}</h2>
            <form
              onSubmit={(e) => {
                this.handleSubmit(e, createSubmission);
              }}
            >
              <div className="form-group">
                <label htmlFor="file">{__.common.SubmissionFile}</label>
                <input
                  type="file"
                  id="file"
                  name="file"
                  className="form-control"
                  placeholder={__.common.SubmissionFile}
                  required
                  onChange={this.handleInputChange}
                  ref={this.fileRef}
                />
              </div>
              <div className="form-group">
                <label htmlFor="note">{__.common.SubmissionNote}</label>
                <textarea
                  id="note"
                  name="note"
                  className="form-control"
                  rows="3"
                  placeholder={__.common.SubmissionNote}
                  value={form.note}
                  onChange={this.handleInputChange}
                />
              </div>
              <div className="form-group">
                <button
                  type="submit"
                  className="btn btn-primary w-10"
                  disabled={submitBtn.submitBtnDisabled}
                >
                  {submitBtn.submitBtnName}
                </button>
              </div>
            </form>
            {error || (data && data.createSubmission.error) ? (
              <Typography color="error">
                {(error ? error.error : data.createSubmission.error.message) ||
                  __.common.SubmissionSubmitFail}
              </Typography>
            ) : null}
          </div>
        )}
      </Mutation>
    );
  }
}

export default Submission;
// export default withData(Submission);
