# AIviVN Backend

## Development

```bash
virtualenv venv --python=python3.6
source venv/bin/activate
npm i
npm run lint
npm run test
npm start
```

## Deploy

`stage` can be either `staging` or `production`

```sh
aws ssm put-parameter --name '/aivivn/<stage>/postgres/user' --type String --value <value>
aws ssm put-parameter --name '/aivivn/<stage>/postgres/password' --type String --value <value>
aws ssm put-parameter --name '/aivivn/<stage>/postgres/db' --type String --value <value>
aws ssm put-parameter --name '/aivivn/<stage>/postgres/host' --type String --value <value>
aws ssm put-parameter --name '/aivivn/<stage>/redis/host' --type String --value <value>
aws ssm put-parameter --name '/aivivn/<stage>/redis/password' --type String --value <value>
aws ssm put-parameter --name '/aivivn/<stage>/secret-key' --type String --value <value>
aws ssm put-parameter --name '/aivivn/<stage>/s3-bucket' --type String --value <s3-bucket-for-submissions>
npm run deploy:<stage>
```