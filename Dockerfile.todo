# Use the official httpd image as a base
FROM httpd:2.4

# Set the working directory
WORKDIR /usr/local/apache2/htdocs/

# Remove the default welcome page
RUN rm -rf ./*

# Create an HTML file and insert the current date
RUN echo "<html><body><h1>You are welcome To Apotians Class, today's Date is:</h1><p>$(date)</p><p>Have Fun Building!</p></body></html>" > index.html

# Expose the default httpd port
EXPOSE 80
