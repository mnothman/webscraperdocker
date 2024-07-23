# Use the official Fedora image
FROM fedora:latest

# Set the ChromeDriver version
ENV CHROMEDRIVER_VERSION=120.0.6099.71

# Set the working directory inside the container
WORKDIR /app

# Install necessary packages
RUN dnf -y update && \
    dnf -y install wget unzip curl gnupg2 && \
    dnf clean all

# Download Google Chrome RPM
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm

# Install Google Chrome
RUN dnf -y install ./google-chrome-stable_current_x86_64.rpm && \
    rm ./google-chrome-stable_current_x86_64.rpm && \
    dnf clean all

# Download and install ChromeDriver
RUN wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip && rm chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/bin/chromedriver && \
    chmod +x /usr/bin/chromedriver

# Install the Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set environment variables for Selenium
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROME_DRIVER=/usr/bin/chromedriver

# Set the default command to run the scraper
CMD ["python", "scraper.py"]
