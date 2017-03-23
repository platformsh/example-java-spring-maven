import json
import base64
import os

platform_relationships = os.getenv('PLATFORM_RELATIONSHIPS')
if platform_relationships:
    relationships = json.loads(base64.b64decode(platform_relationships).decode('utf-8'))

    # Extract the relationships that we want to expose to the application.
    db_settings = relationships['database'][0]

    # Extract the existing environment variables.
    env = dict(os.environ)

    java_opts = [
        # Place any custom Java runtime settings here, with each item as its own paramter.

        # Platform.sh-specific settings.
        # Modify these as needed for the relationships your application defines.
        # For Spring Boot, many of thse names are special and defined by SpringBoot itself.
        # Consult the Spring Boot documentation for details on the proper names.
        '-Dserver.port={}'.format(env['PORT']),
        '-Dspring.datasource.url=jdbc:mysql://{}/{}'.format(db_settings['host'], db_settings['path']),
        '-Dspring.datasource.username={}'.format(db_settings['username']),
        '-Dspring.datasource.password={}'.format(db_settings['password']),
    ]

    # Modify this line to specify the name of your compiled application. It will depend
    # On the name and version listed in your pom.xml file.
    jar_file = './target/gs-spring-boot-0.1.0.jar'


    args = [
        # Add additional paramters to the application here, if needed.
    ]

    # Now kick off the Java process. This script should block as long as the Java app runs.
    command = ['java', '-jar']
    command.extend(java_opts)
    command.append(jar_file)
    command.extend(args)

    print command

    os.execvpe(command[0], command, env)
