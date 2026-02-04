#!/bin/bash

# Define the project directory
PROJECT_DIR="$(pwd)"

# Create the run.sh script
echo "Creating run.sh script..."

cat <<'EOL' > "$PROJECT_DIR/run.sh"
#!/bin/bash
set -e

# Activate virtual environment
source venv/bin/activate

# Export environment variables from your project file
set -a
source server/environment
set +a

# Run Django development server
exec gunicorn --bind 0.0.0.0:8020 --chdir server server.wsgi:application

EOL

# Make run.sh executable
chmod +x "$PROJECT_DIR/run.sh"

# Create the systemd service file
echo "Creating ventingapp.service..."

cat <<EOL | sudo tee /etc/systemd/system/ventingapp.service > /dev/null
[Unit]
Description=Ventingapp Django Application
After=network.target

[Service]
Type=simple
User=ec2-user
Group=ec2-user
ExecStart=$PROJECT_DIR/run.sh
WorkingDirectory=$PROJECT_DIR
Restart=always

[Install]
WantedBy=multi-user.target
EOL

# Reload systemd
echo "Reloading systemd..."
sudo systemctl daemon-reload

# Enable service to start at boot
echo "Enabling ventingapp service..."
sudo systemctl enable ventingapp

# Start the service
echo "Starting ventingapp service..."
sudo systemctl start ventingapp

# Show status
sudo systemctl status ventingapp
