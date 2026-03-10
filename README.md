# AWS Full-Stack Application - Complete Guide for Beginners

## 📋 What You're Building

A complete cloud application with:
- **Frontend**: React app hosted on AWS Amplify
- **Backend**: Flask API running on ECS Fargate (containers)
- **Database**: PostgreSQL on RDS
- **Infrastructure**: Automated with CloudFormation
- **CI/CD**: Automated deployment pipeline

## 🏗️ Architecture Overview

```
User → Amplify Frontend → ALB (Port 80) → ECS Fargate (Backend) → RDS Database
                                ↑
                          GitHub → Pipeline → ECR → ECS
```

## 📚 Step-by-Step Deployment Guide

### Prerequisites
- AWS Account with admin access
- GitHub account
- AWS CLI installed and configured
- Docker installed (you already have this ✓)

### STEP 1: Prepare Your AWS Account (5 minutes)

1. **Install AWS CLI** (if not already):
   ```bash
   brew install awscli
   ```

2. **Configure AWS credentials**:
   ```bash
   aws configure
   ```
   Enter:
   - AWS Access Key ID
   - AWS Secret Access Key
   - Default region: `us-east-1`
   - Default output format: `json`

3. **Verify connection**:
   ```bash
   aws sts get-caller-identity
   ```

### STEP 2: Push Code to GitHub (5 minutes)

1. **Create a new repository** on GitHub named `aws-fullstack-demo`

2. **Push your code**:
   ```bash
   cd ~/aws-fullstack-demo
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote set-url origin https://github.com/YOUR_USERNAME/aws-fullstack-demo.git
   git push -u origin main
   ```

### STEP 3: Deploy Infrastructure with CloudFormation (20 minutes)

This creates: VPC, Subnets, ALB, ECS Cluster, RDS, ECR, and Pipeline

```bash
cd ~/aws-fullstack-demo/infrastructure

# Deploy the stack
aws cloudformation create-stack \
  --stack-name fullstack-app \
  --template-body file://cloudformation-template.yaml \
  --parameters \
    ParameterKey=GitHubRepo,ParameterValue=YOUR_USERNAME/aws-fullstack-demo \
    ParameterKey=GitHubBranch,ParameterValue=main \
    ParameterKey=GitHubToken,ParameterValue=YOUR_GITHUB_TOKEN \
  --capabilities CAPABILITY_IAM

# Monitor deployment (takes 15-20 minutes)
aws cloudformation describe-stacks --stack-name fullstack-app --query 'Stacks[0].StackStatus'
```

**How to get GitHub Token:**
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with `repo` and `admin:repo_hook` permissions
3. Copy the token

### STEP 4: Get Backend URL (2 minutes)

After CloudFormation completes:

```bash
# Get the ALB URL
aws cloudformation describe-stacks \
  --stack-name fullstack-app \
  --query 'Stacks[0].Outputs[?OutputKey==`LoadBalancerURL`].OutputValue' \
  --output text
```

Save this URL - you'll need it for the frontend!

### STEP 5: Deploy Frontend to Amplify (10 minutes)

1. **Update frontend with backend URL**:
   ```bash
   cd ~/aws-fullstack-demo/frontend
   # Edit src/config.js and add your ALB URL
   ```

2. **Deploy to Amplify**:
   - Go to AWS Console → AWS Amplify
   - Click "New app" → "Host web app"
   - Connect your GitHub repository
   - Select `aws-fullstack-demo` repo and `main` branch
   - Build settings: Auto-detected (React)
   - Click "Save and deploy"

3. **Wait for deployment** (5-7 minutes)
   - Amplify will build and deploy automatically
   - You'll get a URL like: `https://main.xxxxx.amplifyapp.com`

### STEP 6: Test Your Application (5 minutes)

1. **Test Backend Health**:
   ```bash
   curl http://YOUR_ALB_URL/health
   ```
   Should return: `{"status": "healthy", "database": "connected"}`

2. **Test Frontend**:
   - Open your Amplify URL in browser
   - Should see the React app
   - Click "Test Backend" button
   - Should display data from backend

### STEP 7: Verify Pipeline (Automatic)

Every time you push to GitHub:
1. Pipeline automatically triggers
2. Builds new Docker image
3. Pushes to ECR
4. Deploys to ECS
5. Zero downtime deployment

**Test it:**
```bash
# Make a change
cd ~/aws-fullstack-demo/backend
# Edit app.py - change version to "1.1"
git add .
git commit -m "Update version"
git push

# Watch pipeline in AWS Console → CodePipeline
```

## 🔍 Understanding Each Component

### VPC (Virtual Private Cloud)
- Your isolated network in AWS
- 2 Public Subnets: For ALB (internet-facing)
- 2 Private Subnets: For ECS and RDS (secure)

### ALB (Application Load Balancer)
- Receives traffic on port 80
- Routes to ECS containers
- Health checks: `/health` endpoint

### ECS Fargate
- Runs your Docker containers
- No server management needed
- Auto-scales based on traffic

### RDS (Relational Database Service)
- Managed PostgreSQL database
- Automatic backups
- In private subnet (secure)

### ECR (Elastic Container Registry)
- Stores your Docker images
- Private registry

### CodePipeline
- Automates: GitHub → Build → Deploy
- Triggers on every push

## 📝 Environment Variables

Backend uses these (automatically set by CloudFormation):
- `DB_HOST`: RDS endpoint
- `DB_NAME`: Database name
- `DB_USER`: Database username
- `DB_PASSWORD`: Database password (from Secrets Manager)
- `DB_PORT`: 5432

## 🛠️ Useful Commands

**View ECS Tasks:**
```bash
aws ecs list-tasks --cluster fullstack-cluster
```

**View Logs:**
```bash
aws logs tail /ecs/backend-app --follow
```

**Update Backend:**
```bash
# Just push to GitHub - pipeline handles the rest!
git push
```

**Delete Everything:**
```bash
aws cloudformation delete-stack --stack-name fullstack-app
```

## 🐛 Troubleshooting

**Pipeline fails?**
- Check CodePipeline in AWS Console
- Verify GitHub token is valid
- Check CloudWatch logs

**Backend not responding?**
- Check ECS task status: AWS Console → ECS → Clusters
- View logs: CloudWatch → Log groups → /ecs/backend-app

**Database connection fails?**
- Verify security groups allow ECS → RDS
- Check RDS is in "Available" state

**Frontend can't reach backend?**
- Verify CORS is enabled (already in code)
- Check ALB security group allows port 80
- Verify ALB target group is healthy

## 💰 Cost Estimate

- **ECS Fargate**: ~$15-30/month (1 task)
- **RDS**: ~$15-25/month (db.t3.micro)
- **ALB**: ~$16/month
- **Amplify**: ~$0-5/month (free tier)
- **Total**: ~$50-75/month

**To minimize costs:**
- Use free tier where available
- Delete resources when not needed
- Use smaller instance types

## 🎯 Next Steps

1. Add authentication (AWS Cognito)
2. Add more API endpoints
3. Set up custom domain
4. Add monitoring (CloudWatch dashboards)
5. Implement auto-scaling
6. Add HTTPS (ACM certificate)

## 📞 Support

If stuck, check:
- AWS CloudFormation events for errors
- CloudWatch logs for application errors
- ECS task status for container issues

Good luck! 🚀
