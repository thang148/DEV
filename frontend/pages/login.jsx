import React from 'react';
import Link from 'next/link';

import Layout from '../components/Layout';
import __ from '../lang/vi';
import withData from '../gql-lib/apollo';

const Login = () => (
  <Layout title="Index">
    <div className="form-login shadow">
      <h2 className="text-center">{__.common.SignIn}</h2>
      <div className="signin-button mt-4">
        <Link href="/account/authenticate/google">
          <a className="btn btn-outline-primary">
            <i className="fab fa-google-plus-g" />
          </a>
        </Link>
        <Link href="/account/authenticate/google">
          <a className="btn btn-outline-primary">
            <i className="fab fa-facebook-f" />
          </a>
        </Link>
        <Link href="/account/authenticate/google">
          <a className="btn btn-outline-primary">
            <i className="fab fa-github" />
          </a>
        </Link>
      </div>
      <hr />
      <form>
        <div className="form-group">
          <label htmlFor="email" className="sr-only">
            {__.common.EmailAddress}
          </label>
          <input
            type="email"
            id="email"
            className="form-control"
            placeholder={__.common.EmailAddress}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="password" className="sr-only">
            {__.common.Password}
          </label>
          <input
            type="password"
            id="password"
            className="form-control"
            placeholder={__.common.Password}
            required
          />
        </div>
        <div className="form-group form-check">
          <label className="form-check-label" htmlFor="rememberMe">
            <input
              type="checkbox"
              id="rememberMe"
              className="form-check-input"
            />
            {__.common.RememberMe}
          </label>
          <Link href="/forgot_password">
            <a className="float-right">{__.common.ForgotPassword}</a>
          </Link>
        </div>
        <div className="form-group">
          <button type="submit" className="btn btn-primary w-100">
            {__.common.SignIn}
          </button>
        </div>
      </form>
    </div>
  </Layout>
);

export default withData(Login);
