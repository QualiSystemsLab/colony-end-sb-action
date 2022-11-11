# torque-end-environment

A github action which is used in a combination with [torque-start-environment](https://github.com/QualiTorque/torque-start-environment) and helps to integrate Torque into your CI/CD pipeline

## Usage

```yaml
- uses: QualiTorque/torque-end-environment@v1
  with:
    # The name of the Torque Space your repository is connected to
    space: TestSpace

    # Provide the long term Torque token. You can generate it in Torque > Settings > Integrations
    # or via the REST API.
    torque_token: ${{ secrets.TORQUE_TOKEN }}

    # Provide the ID of the environment you want to end
    environment_id: ${{ steps.start-env.outputs.environment_id }}

    # [Optional] Provide the url string. In rare cases you migth want to override the main
    # Torque server address 'https://portal.qtorque.io'. 
    torque_url: "https://portal.qtorque.io"
```

## Examples

The following example demonstrates how to use this action in combination with [torque-start-environment](https://github.com/QualiTorque/torque-start-environment) to run tests against some flask web application deployed inside a Torque environment:

```yaml
name: CI
on:
  pull_request:
    branches:
      - master

jobs:
  build-and-publish:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v1
    - name: Make artifact
      id: build
      run: |
        mkdir -p workspace
        tar -zcf workspace/flaskapp.latest.tar.gz -C src/ .
    - name: Upload
      uses: aws-actions/configure-aws-credentials@v1
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1
        run: aws s3 copy ./workspace/flaskapp.latest.tar.gz s3://myartifacts/latest
        
  test-with-torque:
    needs: build-and-publish
    runs-on: ubuntu-latest
    
    steps:
    - name: Start Torque Environment
      id: start-environment
      uses: QualiTorque/torque-start-environment@v1
      with:
        space: Demo
        blueprint_name: WebApp
        torque_token: ${{ secrets.TORQUE_TOKEN }}
        duration: 120
        timeout: 30
        artifacts: 'flask-app=latest/flaskapp.lates.tar.gz'
        inputs: 'PORT=8080,AWS_INSTANCE_TYPE=m5.large'
    
    - name: Testing
      id: test-app
      run: |
        echo "Running tests against environment with id: ${{ steps.start-environment.outputs.environment_id }}"
        echo "Do something with environment details json: ${{ steps.start-environment.outputs.environment_details }}"

    - name: Stop environment
      uses: QualiTorque/torque-end-environment@v1
      with:
        space: Demo
        environment_id: ${{ steps.start-environment.outputs.environment_id }}
        torque_token: ${{ secrets.TORQUE_TOKEN }} 
```
