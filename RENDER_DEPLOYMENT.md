# Render Deployment Guide for Food Delivery App

This document provides detailed instructions for deploying the Food Delivery App microservices on Render.

## Prerequisites

- GitHub account
- Render account (create one at [render.com](https://render.com) if you don't have one)
- Git installed on your local machine
- Food Delivery App codebase with all necessary files

## Option 1: Deploy Using Render Blueprint (Recommended)

The easiest way to deploy all services is using Render's Blueprint feature with the provided `render.yaml` configuration.

1. **Push your code to GitHub:**
   ```powershell
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Deploy with Blueprint:**
   - Log in to your Render account
   - From the dashboard, click on "New" → "Blueprint"
   - Connect your GitHub repository
   - Select the repository containing the Food Delivery App
   - Click "Apply Blueprint"
   - Render will automatically configure and deploy:
     - PostgreSQL database
     - User Service
     - Restaurant Service
     - Delivery Service

3. **Initialize the database:**
   - After all services are deployed, navigate to your PostgreSQL service in the Render dashboard
   - Go to the "Shell" tab
   - Upload the `init.sql` file
   - Run: `psql -f init.sql`

4. **Verify services:**
   - User Service: https://food-delivery-user-service.onrender.com/docs
   - Restaurant Service: https://food-delivery-restaurant-service.onrender.com/docs
   - Delivery Service: https://food-delivery-delivery-service.onrender.com/docs

## Option 2: Manual Deployment

If you prefer to deploy each service individually:

1. **Create a PostgreSQL database:**
   - From the Render dashboard, click on "New" → "PostgreSQL"
   - Name: food-delivery-db
   - Database: food_delivery
   - User: postgres
   - Region: Choose the region closest to your users
   - Plan: Free (or higher for production)
   - Click "Create Database"
   - Note the "Internal Database URL" for the next steps

2. **Deploy the User Service:**
   - From the Render dashboard, click on "New" → "Web Service"
   - Connect your GitHub repository
   - Name: food-delivery-user-service
   - Root Directory: user_service
   - Environment: Docker
   - Set these environment variables:
     - `DATABASE_URL`: (copy the Internal Database URL from previous step)
     - `RESTAURANT_SERVICE_URL`: https://food-delivery-restaurant-service.onrender.com
     - `DELIVERY_SERVICE_URL`: https://food-delivery-delivery-service.onrender.com
   - Click "Create Web Service"

3. **Deploy the Restaurant Service:**
   - Follow the same steps as the User Service
   - Name: food-delivery-restaurant-service
   - Root Directory: restaurant_service
   - Set these environment variables:
     - `DATABASE_URL`: (copy the Internal Database URL from step 1)
     - `DELIVERY_SERVICE_URL`: https://food-delivery-delivery-service.onrender.com

4. **Deploy the Delivery Service:**
   - Follow the same steps as the other services
   - Name: food-delivery-delivery-service
   - Root Directory: delivery_service
   - Set these environment variables:
     - `DATABASE_URL`: (copy the Internal Database URL from step 1)
     - `RESTAURANT_SERVICE_URL`: https://food-delivery-restaurant-service.onrender.com

5. **Initialize the database:**
   - Follow the same database initialization steps as in Option 1

## Post-Deployment Steps

1. **Test the API endpoints:**
   - Import the Postman collection into Postman
   - Update the environment variables to point to your Render services
   - Test each endpoint to ensure they're working correctly

2. **Monitor your services:**
   - Use Render's built-in logging and metrics to monitor your services
   - Check for any errors in the logs
   - Set up alerts for service disruptions

3. **Scale as needed:**
   - For production use, consider upgrading from the free tier
   - Enable auto-scaling for web services if needed
   - Set up a dedicated PostgreSQL instance for better performance

## Troubleshooting

- **Services fail to start:**
  - Check the logs for error messages
  - Verify environment variables are set correctly
  - Ensure the database is properly initialized

- **Services can't communicate:**
  - Verify the service URLs are correct
  - Check if the services are running
  - Test internal network connectivity

- **Database connection issues:**
  - Check if the database URL is correct
  - Ensure the database is running
  - Verify network connectivity between services and database

## Support

If you encounter issues with the deployment, check Render's documentation at [render.com/docs](https://render.com/docs) or contact their support team.
