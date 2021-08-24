# torque-end-sb-action

A github action which is used in a combination with [torque-start-sb-action](https://github.com/QualiTorque/torque-start-sb-action) and helps to integrate Torque into your CI/CD pipeline

## Usage

```yaml
- uses: QualiTorque/torque-end-sb-action@v0.0.3
  with:
    # The name of the Torque Space your repository is connected to
    space: TestSpace

    # Provide the long term Torque token. You can generate it in Torque > Settings > Integrations
    # or via the REST API.
    torque_token: ${{ secrets.TORQUE_TOKEN }}

    # Provide the ID of the sandbox you want to end
    sandbox_id: ${{ steps.start-sb.outputs.sandbox_id }}
```

## Examples

The following example demonstrates how to use this action in combination with [torque-start-sb-action](https://github.com/QualiTorque/torque-start-sb-action) to run tests against some flask web application deployed inside a Torque sandbox:

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
    - name: Start Torque Sandbox
      id: start-sandbox
      uses: QualiTorque/torque-start-sb-action@v0.0.3
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
        echo "Running tests against sandbox with id: ${{ steps.start-sandbox.outputs.sandbox_id }}
        shortcuts=${{ steps.start-sandbox.sandbox_shortcuts }}
        readarray -t shortcuts <<< "$(jq '. | .flask-app[]' <<< '${{ steps.start-sandbox.sandbox_shortcuts }}')"
        for shortcut in ${shortcuts[@]}; do
            "Do something with this ${shortcut}."
        done

    - name: Stop sandbox
      uses: QualiTorque/torque-end-sb-action@v0.0.3
      with:
        space: Demo
        sandbox_id: ${{ steps.start-sandbox.outputs.sandbox_id }}
        torque_token: ${{ secrets.TORQUE_TOKEN }} 
```
