const axios = require('axios');
const faker = require('faker');
const camelcaseKeys = require('camelcase-keys');
const debug = require('debug')('aivivn:resolvers');
const moment = require('moment');
const lodash = require('lodash');

faker.locale = 'vi';
const BACKEND_HOST = process.env.BACKEND_HOST || 'http://localhost:5000';

const POSITIONS = ['Developer', 'Project Manager', 'Designer', 'Tester'];

function fakeUser(id, username = '') {
  faker.seed(id);
  const medalRange = { min: 0, max: 200 };
  const medals = [
    faker.random.number(medalRange),
    faker.random.number(medalRange),
    faker.random.number(medalRange),
  ];
  return {
    id:
      id +
      faker.random.number({
        min: 0,
        max: 1000,
      }),
    email: faker.internet.email(),
    username: username !== '' ? username : faker.internet.userName(),
    fullName: faker.name.findName(),
    avatar: `https://picsum.photos/200/200/?image=${faker.random.number({
      min: 800,
      max: 1000,
    })}`,
    rank: id,
    createdAt: moment(faker.date.past()).format(),
    updatedAt: moment(faker.date.past()).format(),
    medals,
    contests: faker.random.number({
      min: lodash.sum(medals),
      max: lodash.sum(medals) + 10,
    }),
    bestContestRank: faker.random.number({ min: 0, max: 200 }),
    job: {
      title:
        POSITIONS[faker.random.number({ min: 0, max: POSITIONS.length - 1 })],
      company: faker.company.companyName(),
    },
    address: faker.address.state(),
  };
}

// function fakeTeam() {
//   const members = [];
//   return {
//     name: faker.lorem.words(3),
//     members,
//     score:
//       faker.random.number({
//         max: 1000,
//       }) / 1000,
//   };
// }

// function fakeTeams() {
//   const total = faker.random.number({
//     min: 10,
//     max: 100,
//   });
//   const items = [];
//   for (let i = 0; i < total; i += 1) {
//     items.push(fakeTeam());
//   }
//   return {
//     total,
//     items,
//   };
// }

// function fakeMembers() {
//   const members = [];
//   const total = faker.random.number({
//     min: 1,
//     max: 5,
//   });
//   for (let i = 0; i < total; i += 1) {
//     const member = fakeMember(i);
//     members.push(member);
//   }

//   return members;
// }
// function fakeTeam(id) {
//   const members = fakeMembers();
//   return {
//     id,
//     name: faker.lorem.words(3),
//     members,
//     score:
//       faker.random.number({
//         max: 1000,
//       }) / 1000,
//     change: faker.random.number({
//       min: -45,
//       max: 45,
//     }),
//     entries: faker.random.number({
//       min: 0,
//       max: 30,
//     }),
//     last: faker.date.past(0),
//   };
// }

// function fakeTeams() {
//   const total = faker.random.number({
//     min: 10,
//     max: 100,
//   });
//   const items = [];
//   for (let i = 0; i < total; i += 1) {
//     items.push(fakeTeam(i));
//   }
//   return {
//     total,
//     items,
//   };
// }

function fakeContest(id) {
  faker.seed(19223 + parseInt(id, 10));
  return {
    id,
    name: faker.lorem.words(5),
    overview: faker.lorem.sentences(50),
    description: faker.lorem.sentences(10),
    fullDescription: faker.lorem.paragraphs(20, '<br/>'),
    evaluation: faker.lorem.paragraphs(10, '<br/>'),
    prizes: faker.lorem.paragraphs(5, '<br/>'),
    timeline: faker.lorem.paragraphs(5, '<br/>'),
    start: moment(faker.date.past()).format(),
    end: moment(faker.date.future()).format(),
    tags: [1, 2].map(() => ({
      id: faker.random.number({
        min: 1,
        max: 1000,
      }),
      name: faker.lorem.word(),
    })),
    avatar: `https://picsum.photos/200/200/?image=${faker.random.number({
      min: 800,
      max: 1000,
    })}`,
    company: faker.company.companyName(),
    prize: faker.random.number({
      min: 1,
      max: 200,
    }),
    data: {
      name: faker.system.fileName(),
      link: faker.internet.url(),
    },
  };
}

function authorizationHeader(accessToken) {
  return { Authorization: `Bearer ${accessToken}` };
}

module.exports = {
  Query: {
    contest(_, { id }, { accessToken }) {
      return axios
        .get(`${BACKEND_HOST}/contests/${id}`, {
          headers: authorizationHeader(accessToken),
        })
        .then(({ data }) => ({
          ...fakeContest(id),
          ...camelcaseKeys(data),
        }))
        .catch((error) => {
          debug('contests error', error.response.data);
          return [];
        });
    },

    users(_, { take, skip }) {
      const users = [];
      for (let i = 0; i < (take || 10); i += 1) {
        users.push(fakeUser(skip + i));
      }
      return users;
    },

    user(_, { username }, { accessToken }) {
      return axios
        .get(`${BACKEND_HOST}/users/${username}`, {
          headers: authorizationHeader(accessToken),
        })
        .then(({ data }) => ({
          ...fakeUser(data.id, username),
          ...camelcaseKeys(data),
        }))
        .catch((error) => {
          debug('me error', error.response.data);
          return null;
        });
    },

    contests(_, { take, skip }) {
      return axios
        .get(`${BACKEND_HOST}/contests`, {
          params: { limit: take, offset: skip },
        })
        .then(({ data }) => camelcaseKeys(data))
        .catch((error) => {
          debug('contests error', error.response.data);
          return [];
        });
    },

    me(ctx, args, { accessToken }) {
      return axios
        .get(`${BACKEND_HOST}/me`, {
          headers: authorizationHeader(accessToken),
        })
        .then(({ data }) => camelcaseKeys(data))
        .catch((error) => {
          debug('me error', error.response.data);
          return null;
        });
    },
  },

  Contest: {
    description(contest) {
      faker.seed(contest.id + 1000);
      return faker.lorem.sentences(10);
    },

    fullDescription(contest) {
      faker.seed(contest.id + 1000);
      return faker.lorem.paragraphs(20, '<br/>');
    },

    teams(contest, { take, skip }, { accessToken }) {
      debug('teams', take, skip, accessToken, contest.id, contest.numTeams);
      return axios
        .get(`${BACKEND_HOST}/contests/${contest.id}/teams`, {
          headers: authorizationHeader(accessToken),
          params: { limit: take, offset: skip },
        })
        .then(({ data }) => ({
          total: contest.numTeams,
          items: camelcaseKeys(data, { deep: true }),
        }))
        .catch((error) => {
          debug('teams error', error.response.data);
          return [];
        });
    },

    data() {
      return {
        name: faker.system.fileName(),
        link: faker.internet.url(),
      };
    },

    myTeam(contest, _, { accessToken }) {
      debug('my team', accessToken, contest.id);
      return axios
        .get(`${BACKEND_HOST}/contests/${contest.id}/teams/my-team`, {
          headers: authorizationHeader(accessToken),
        })
        .then(({ data }) => camelcaseKeys(data))
        .catch((error) => {
          debug('my team error', accessToken, error.response.data);
          return null;
        });
    },
  },

  Team: {
    // members(team) {
    //   const memberList = [];
    //   if (team === undefined || team === null) {
    //     return memberList;
    //   }
    //   for (let i = 0; i < team.members.length; i += 1) {
    //     memberList.push(team.members[i]);
    //   }
    //   return memberList;
    // },
  },

  TeamMember: {
    avatar() {
      return `https://picsum.photos/200/200/?image=${faker.random.number({
        min: 800,
        max: 1000,
      })}`;
    },

    user(member, _, { accessToken }) {
      debug('team member user', accessToken, member);
      return axios
        .get(`${BACKEND_HOST}/users/${member.userId}`, {
          headers: authorizationHeader(accessToken),
        })
        .then(({ data }) => camelcaseKeys(data))
        .catch((error) => {
          debug('team member user error', accessToken, error.response.data);
          return null;
        });
    },
  },

  User: {
    // avatar(user) {
    //   faker.seed(user.id);
    //   return `https://picsum.photos/200/200/?image=${faker.random.number({
    //     min: 800,
    //     max: 1000,
    //   })}`;
    // },
  },

  Mutation: {
    login(_, args, context) {
      const { email, password } = args;
      const { login } = context;
      return axios
        .post(`${BACKEND_HOST}/users/login`, {
          username: email,
          password,
        })
        .then(({ data }) => {
          login(data.access_token);
          return {
            user: {
              email: 'test',
              fullname: 'test',
            },
          };
        })
        .catch(() => ({
          error: { message: 'Incorrect Email / Password!' },
        }));
    },
    register(_, args) {
      const { username, email, password } = args;
      return axios
        .post(`${BACKEND_HOST}/users`, {
          username,
          email,
          password,
        })
        .then(({ data }) => {
          return {
            user: {
              id: data.user_id,
            },
          };
        })
        .catch(() => ({
          error: { message: 'Username/Email existed!' },
        }));
    },
    joinContest(_, { contestId, teamName }, { accessToken }) {
      debug(`contestid la: ${contestId} , team name la: ${teamName}`);
      return axios
        .post(
          `${BACKEND_HOST}/contests/${contestId}/teams`,
          { name: teamName },
          {
            headers: authorizationHeader(accessToken),
          },
        )
        .then(({ data }) => camelcaseKeys({ team: data }))
        .catch((error) => {
          debug('join contest', error.response.data);
          return camelcaseKeys(error.response.data.data);
        });
    },

    async createSubmission(_, { contestId, note }, { accessToken }) {
      try {
        debug('submission', contestId, note);
        const endpoint = `${BACKEND_HOST}/contests/${contestId}/my-team/submissions`;
        const { data } = await axios.post(
          endpoint,
          { note },
          { headers: authorizationHeader(accessToken) },
        );
        data.fields = JSON.stringify(data.fields);
        return { s3: data };
      } catch (error) {
        debug(error.response.data);
        return { error: error.response.data };
      }
    },
  },
};
