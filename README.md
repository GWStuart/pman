# Pman

**Pman** is a CLI password manager written in Python. It is intended to be used through the command line and also has a web version available running on my github [https://gwstuart.github.io/projects.html|here].

Would highly recommend first reading how Pman works in the [[About]] section

## Table of Contents

- [About](#about)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## About

This section is going to talk about Pman and how it works.
Essentially Pman is a stateless password manager...

## Installation

## Usage

### Basic Usage

To generate the password for an application simply type,
```
pman APPLICATION_NAME
```
You will then be prompted to enter your masterpassword which Pman will use to generate your password to the website. More information on how Pman works can be found in the [About](#about) section.

Pman also accepts a URL as the application and will automatically strip off url parameters so that it is just the website name
```
pman URL
```

### Saving Data

Users can choose to optionally save that they have credentials stored with a website by passing a `-s` flag,
```
pman APPLICATION_NAME -s
```

The user will then be prompted to optionally save additional information in the database regarding that password including a username and description.

All the data stored in the database can be viewed with the command,
```
pman -l
```

### Modifying the Password

Sometimes you may need to modify the outputted password to meet the requirements of a particular website/application. This can be easily achieved with flags. Pman support two different modified flags, one for modifying the length of the password and the other for modifying the accepted characters.

To modify the length use the `-n` flag. The following command restricts the password to 16 characters
```
pman APPLICATION_NAME -n 16
```

If a website/application doesn't accept certain characters then exclude them using the `-x` flag. The command will exclude all characters after the `-x`,
```
pman -x !@#
```

### Usage Tips

If you need to type certain characters into the bash terminal such as, !@#, put them in single brackets

## License


