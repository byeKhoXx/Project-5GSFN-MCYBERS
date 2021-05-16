# our base image
FROM ruby

RUN useradd -ms /bin/bash dnsuser
USER dnsuser
WORKDIR /home/dnsuser

# copy files required for the app to run
COPY dns.rb /home/dnsuser
COPY config.yml /home/dnsuser
COPY db.yml /home/dnsuser

# tell the port number the container should expose
EXPOSE 80
EXPOSE 53


# run the application
CMD ["ruby", "dns.rb"]
