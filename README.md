# earkweb
E-ARK integrated prototype web application

## Set up the development environment

### Checkout and install dependencies

1. Checkout project

        git clone https://github.com/eark-project/earkweb

2. Create virtual environment (python)

    Create a virtual environment (e.g. named earkweb) to install additional python packages separately from the default python installation.

        sudo pip install virtualenv
        sudo pip install virtualenvwrapper
        mkvirtualenv earkweb
        workon earkweb
        
    If the virtual environment is active, this is shown by a prefix in the console:
    
        (earkweb)user@machine:~/path/to/earkweb$
        
    If it is not active, it can be activated as follows:
    
        user@machine:~/path/to/earkweb$ workon earkweb

    And it can be deactivated again by typing:
    
        deactivate

3. Install additional libraries

        pip install Django==1.7
        pip install requests
        pip install lxml

4. Adapt settings to your local development environment

    Change path so that it detects your local development path in earkweb/earkweb/urls.py:
    
        if "Development/" ...
    
    Set the file to "assume-unchanged":
    
        git update-index --assume-unchanged earkweb/earkweb/urls.py
    
    and undo if needed:
    
        git update-index --no-assume-unchanged earkweb/earkweb/urls.py

5. Enable CAS in Django

    Note that the CAS URL setting points to the development server, therefore it is not required
    to install CAS in the development environment.

    5.1. Install mercurial if it is not available already:

        sudo apt-get install mercurial

    5.2 Get module from https://bitbucket.org/cpcc/django-cas

        hg clone https://bitbucket.org/cpcc/django-cas
    
    5.3. Install django-cas

        cd django-cas
        python setup.py install
    
### Prepare database and execute

1. Prepare database

    A local SQLite database 'db.sqlite3' will be created in the project root directory.

        python manage.py migrate
    
2. Start web application

    2.1 Start the web application from the command line using the command:

        python manage.py runserver
        
    2.2 A message similar to the one below should be shown in case of success
    
        System check identified no issues (0 silenced).
        June 18, 2015 - 08:34:56
        Django version 1.7, using settings 'earkweb.settings'
        Starting development server at http://127.0.0.1:8000/
        Quit the server with CONTROL-C.
        
    2.2 Open web browser at http://127.0.0.1:8000/

## CAS server

The development version points to CAS installed on the demo server, therefore this is not needed for
development.

### Installation

#### Prepare Apache Tomcat (enable SSL)

1. Create keystore

    keytool -genkey -alias tomcat -keyalg RSA -keystore keystore.jks

2. Activate SSL using the keystore (in conf/server.xml):

    <Connector port="8443" 
        keystoreFile="/usr/local/java/apache-tomcat-7.0.56/keystore.jks" 
        keystorePass="changeit" 
        protocol="org.apache.coyote.http11.Http11NioProtocol"
        maxThreads="150" SSLEnabled="true" scheme="https" secure="true"
        clientAuth="false" sslProtocol="TLS" />


    cp cas-server-4.0.0/modules/cas-server-webapp-4.0.0.war $TOMCAT_HOME/webapps/

#### Deployment

1. Download CAS

    http://downloads.jasig.org/cas/cas-server-4.0.0-release.tar.gz

2. Deploy CAS WAR to Apache Tomcat

    cp cas-server-4.0.0/modules/cas-server-webapp-4.0.0.war $TOMCAT_HOME/webapps/
    
### Administration

#### Add/Change user

   $CATALINA_HOME/webapps/cas/WEB-INF/deployerConfigContext.xml
   
   <bean id="primaryAuthenticationHandler"
          class="org.jasig.cas.authentication.AcceptUsersAuthenticationHandler">
        <property name="users">
            <map>
                <entry key="user" value="pwd"/>
                ...
            </map>
        </property>
    </bean>


